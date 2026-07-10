#!/usr/bin/python3

import logging
import argparse
import json
import re
import itertools
import hashlib
import urllib.parse
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Optional, Any, Set
from http.client import HTTPSConnection

from scapy.layers.dot11 import Dot11ProbeReq
from scapy.all import sniff
from tornado import websocket, web, httpserver, ioloop

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # Suppress scapy warnings

# Load vendors into a dictionary for faster lookup
VENDORS = {}
try:
    with open('vendors.txt', 'r') as f:
        for line in f:
            parts = line.split('\t')
            if len(parts) >= 2:
                VENDORS[parts[0].lower()] = parts[1].strip()
except FileNotFoundError:
    logger.error("vendors.txt not found. Vendor lookup will be disabled.")

#in case you need to hop through channels (2.4 and 5 GHz Europe)
channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 68, 96, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 132, 134, 136, 138, 140, 142, 144, 149, 151, 153, 155, 157, 159, 161, 165, 167, 169, 171, 173]

class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)
class WebSocketServer(websocket.WebSocketHandler):
    clients: Set['WebSocketServer'] = set()

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self):
        logger.info("Client connected")
        WebSocketSever.clients.add(self)

    def on_message(self, message: str):
        logger.info(f"Message: {message}")

    def on_close(self):
        logger.info("Connection terminated.")
        WebSocketSever.clients.remove(self)

    @classmethod
    def broadcast(cls, message: str):
        for client in cls.clients:
            try:
                client.write_message(message)
            except Exception:
                logger.exception("Error broadcasting message")

class StaticFileHandler(web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")

class ConfigHandler(web.RequestHandler):
    def get(self):
        config = getConfig()
        safe_config = {
            "googleMapsAPIKey": config.get("googleMapsAPIKey", ""),
            "defaultLat": config.get("defaultLat", "60.201790"),
            "defaultLong": config.get("defaultLong", "24.933960"),
            "defaultZoom": config.get("defaultZoom", 8),
        }
        self.write(safe_config)

class FrameHandler:
    def __init__(self, cfg: Dict[str, Any], out: Optional[str]):
        self.seen: Set[str] = set()
        self.config = cfg
        self.outFile = out
        self.executor = ThreadPoolExecutor(max_workers=5)

    def process_probe(self, info: Dict[str, Any], probeSSID: str):
        try:
            locations = self.getLocation(probeSSID)
            info['location'] = locations
            message = json.dumps(info)
            logger.info(f"Broadcasting to clients: {message}")
            ioloop.IOLoop.current().add_callback(WebSocketServer.broadcast, message)
            if self.outFile is not None:
                with open(self.outFile, 'a') as file:
                    file.write(message + "\n")
        except Exception:
            logger.exception("Error processing probe")

    def handler(self, frame):
        if (frame.haslayer(Dot11ProbeReq) and (frame.type == 0x0 or frame.type == 0x04)):
            try:
                probeSSID = str(frame.info)[2:-1]
                if (len(probeSSID) > 0):
                    info = {}
                    info['device'] = frame.addr2
                    info['ssid'] = probeSSID
                    info['vendor'] = checkVendor(frame.addr2)
                    info['rssi'] = frame.dBm_AntSignal
                    if self.config["whitelist"] and info['ssid'] not in self.config["whitelist"]:
                        logger.info(f"Probe Request for {info['ssid']} is not on the whitelist and was skipped.")
                        return
                    if self.config["blacklist"] and info['ssid'] in self.config["blacklist"]:
                        logger.info(f"Probe Request for {info['ssid']} is on the blacklist and was skipped.")
                        return
                    if params.limitSignalStrength is not None and int(info['rssi']) < int(params.limitSignalStrength):
                        logger.info(f"Skipping captured frame. Signal strength {info['rssi']} is below the set minimum of {params.limitSignalStrength}")
                        return
                    identifier = f"{info['device']}{info['ssid']}"
                    computed_hash = hashlib.sha256(identifier.encode('utf-8')).hexdigest()
                    if not self.checkDuplicate(info, computed_hash):
                        self.addSeen(info, computed_hash)
                        self.executor.submit(self.process_probe, info, probeSSID)
            except Exception:
                logger.exception("Error in frame handler")

    # API Call to WIGLE.NET to obtain geolocation of SSIDS
    def getLocation(self, ssid: str) -> List[Dict[str, float]]:
        locations = []
        try:
            conn = HTTPSConnection("api.wigle.net")
            headers = {'Authorization': 'Basic %s' % self.config["wigleAuthToken"]}
            conn.request('GET',
                         '/api/v2/network/search?onlymine=false&freenet=false&paynet=false&ssid=' + urllib.parse.quote_plus(
                             ssid), headers=headers)
            resp = conn.getresponse()
            data = str(resp.read())[2:-1]
            data = data.replace("true", "\"True\"").replace("false", "\"False\"")
            dataJson = json.loads(data, cls=LazyDecoder)
            if dataJson.get('success') == "False" and dataJson.get('error') == "too many queries today":
                logger.warning("WIGLE API LIMIT REACHED. Sending coordinates 0.0 0.0")
                return [{'lat': 0.0, 'lng': 0.0}, {'lat': 0.0, 'lng': 0.0}]
            elif dataJson.get('results'):
                for result in dataJson['results']:
                    locations.append({
                        'lat': result['trilat'],
                        'lng': result['trilong']
                    })
                return locations
        except Exception:
            logger.exception(f"Error retrieving lat and long for {ssid}")

        return locations

    def _compute_hash(self, info: Dict[str, Any]) -> str:
        identifier = f"{info['device']}{info['ssid']}"
        return hashlib.sha256(identifier.encode('utf-8')).hexdigest()

    def addSeen(self, info: Dict[str, Any], computed_hash: Optional[str] = None):
        try:
            if computed_hash is None:
                computed_hash = self._compute_hash(info)
            self.seen.add(computed_hash)
        except Exception:
            logger.exception("Error. SSID was not stored successfully")

    def checkDuplicate(self, info: Dict[str, Any], computed_hash: Optional[str] = None) -> bool:
        try:
            if computed_hash is None:
                computed_hash = self._compute_hash(info)
            return computed_hash in self.seen
        except Exception:
            logger.exception("Error. SSID duplicate check failed")
            return True

def checkVendor(mac: str) -> str:
    mac_clean = mac.replace(':', '').lower()
    # Check for OUI in VENDORS dictionary.
    # Typically OUI is first 6 characters, but can be more for some registrations.
    # The original implementation used 'in', which is a bit broad.
    # We'll try common OUI lengths or just check prefixes.
    for length in [6, 7, 9]: # Common OUI/OUI-24, OUI-28, OUI-36 lengths in hex
        prefix = mac_clean[:length]
        if prefix in VENDORS:
            return VENDORS[prefix]
    return 'N/A'

def start_sniffer(config: Dict[str, Any], interface: str, write_file: Optional[str]):
    frameHandler = FrameHandler(config, write_file)
    logger.info(f"Monitoring for probe requests on NIC: {interface}...")
    if write_file is not None:
        logger.info(f"Saving output to: {write_file}")
        logger.warning("Storing the captured data violates GDPR rules. Check your data privacy laws.")

    sniff(iface=interface, prn=frameHandler.handler, store=0)
    logger.info("Sniffer stopped.")

def hopChannel():
    for channel in itertools.cycle(channels):
        try:
            subprocess.run(["iwconfig", params.interface, "channel", str(channel)], check=False)
        except Exception:
            logger.exception("Error hopping channel")
        import time
        time.sleep(3)


def getConfig() -> Dict[str, Any]:
    try:
        with open("config.json", 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        logger.error("config.json not found.")
        # Fallback to some defaults or exit
        return {
            "serverIp": "127.0.0.1",
            "serverPort": "8888",
            "whitelist": [],
            "blacklist": []
        }


def main():
    global params
    parser = argparse.ArgumentParser(description="Argos - WiFi Probe Request Sniffer")
    parser.add_argument('-i', '--interface', help="interface to capture on")
    # Warning, storage of MAC addresses falls under GDPR regulations
    parser.add_argument('-w', '--write', help="Write data to file")
    # Limit signal strength to avoid capturing too much
    parser.add_argument('-lss', '--limitSignalStrength', help="Limit signal strength to avoid capturing too much")
    params = parser.parse_args()

    logger.info("Argos starting...")

    # Check if we received the interface as a parameter
    if not params.interface:
        subprocess.run(["iwconfig"], check=False)
        params.interface = input("Which interface should be used: ")

    # start the NIC monitoring mode with the help of airmon
    try:
        subprocess.run(["airmon-ng", "start", params.interface], check=True)
    except subprocess.CalledProcessError:
        logger.error(f"Failed to start monitoring mode on {params.interface}")

    logger.info("Loading configuration from config.json")
    config = getConfig()

    if config["whitelist"] and config["blacklist"]:
        logger.error("Please use only the whitelist or the blacklist, not both.")
        exit(1)

    logger.info("Starting the web socket server...")
    app = web.Application([
        (r'/ws', WebSocketServer),
        (r'/api/config', ConfigHandler),
        (r'/(.*)', StaticFileHandler, {"path": "public", "default_filename": "index.html"}),
    ])

    http_server = httpserver.HTTPServer(app)
    http_server.listen(config["serverPort"])
    logger.info(f"Web socket ready on port {config['serverPort']}")

    # Start sniffer in a background thread
    sniffer_thread = threading.Thread(
        target=start_sniffer,
        args=(config, params.interface, params.write),
        daemon=True
    )
    sniffer_thread.start()

    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logger.info("Stopping...")


if __name__ == '__main__':
    main()
