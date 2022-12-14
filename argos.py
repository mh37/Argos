#!/usr/bin/python3

import logging

from scapy.layers.dot11 import Dot11ProbeReq

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # Supress scapy warnings
from scapy.all import *
import argparse
import json
import re
import itertools
import hashlib
from http.client import HTTPSConnection
import urllib
from tornado import websocket, web, httpserver, ioloop

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
class WebSocketSever(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print("[i] Client connected")
        try:
            sniffer(self)
        except PermissionError as e:
            print("[!] Run as root!")
            ioloop.IOLoop.instance().stop()

    def on_message(self, message):
        print("[i] Message: " + str(message))

    def on_close(self):
        print("[!] Connection terminated.")

class FrameHandler:
    callback = None
    seen = None
    config = None
    outFile = None

    def __init__(self, cb, cfg, out):
        self.callback = cb
        self.seen = []
        self.config = cfg
        self.outFile = out

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
                    if (len(self.config["whitelist"]) > 0 and (info['ssid'] not in self.config["whitelist"])):
                        print("Probe Request for " + info['ssid'] + " is not on the whitelist and was skipped.")
                        return
                    if (len(self.config["blacklist"]) > 0 and (info['ssid'] in self.config["blacklist"])):
                        print("Probe Request for " + info['ssid'] + " is on the blacklist and was skipped.")
                        return
                    if ((params.limitSignalStrength is not None) and (int(info['rssi']) < int(params.limitSignalStrength))):
                        print("Skipping captured frame. Signal strength" + info['rssi'] + "is below the set minimum of " + params.limitSignalStrength)
                        return
                    if (self.checkDuplicate(info) == False):
                        self.addSeen(info)
                        locations = self.getLocation(probeSSID)
                        info['location'] = locations
                        print("[+] To client: " + json.dumps(info))
                        self.callback.write_message(json.dumps(info))
                        if (self.outFile is not None):
                            with open(self.outFile, 'a') as file:
                                file.write(json.dumps(info) + "\n")
            except Exception as e:
                pass  # Ignore exceptions

    # API Call to WIGLE.NET to obtain geolocation of SSIDS
    def getLocation(self, ssid):
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
            if (dataJson['success'] == "False" and dataJson['error'] == "too many queries today"):
                print("[!] WIGLE API LIMIT REACHED. Sending  coordinates 0.0 0.0")
                locations.append({})
                locations[len(locations) - 1]['lat'] = 0.0
                locations[len(locations) - 1]['lng'] = 0.0
                locations.append({})
                locations[len(locations) - 1]['lat'] = 0.0
                locations[len(locations) - 1]['lng'] = 0.0
            elif (dataJson['results'] and len(dataJson['results']) > 0):
                for r in range(len(dataJson['results'])):
                    locations.append({})
                    locations[len(locations) - 1]['lat'] = dataJson['results'][r]['trilat']
                    locations[len(locations) - 1]['lng'] = dataJson['results'][r]['trilong']
                return locations
        except Exception as e:
            print("[!] Error retrieving lat and long for " + ssid)
            print(e)
            print("Response: " + data)

        return locations

    def addSeen(self, info):
        try:
            self.seen.append(hashlib.md5(str(info["device"] +info["ssid"]).encode('utf-8')).hexdigest())
        except:
            print("[!] Error. SSID was not stored successfully")

    def checkDuplicate(self, info):
        try:
            return (hashlib.md5(str(info["device"] +info["ssid"]).encode('utf-8')).hexdigest() in self.seen)
        except:
            print("[!] Error. SSID duplicate check failed")
            return True

def checkVendor(mac):
        with open('vendors.txt','r') as f:
            for line in f:
                l = line.split('\t')
                if l[0].lower() in mac.replace(':','') :
                    return l[1].strip()
        return 'N/A'

def sniffer(context):
    frameHandler = FrameHandler(context, getConfig(), params.write)
    print("[i] Monitoring for probe requests on NIC: " + params.interface + "...")
    if (params.write is not None):
        print("[#] Saving output to: " + params.write)
        print("[WARNING] Storing the captured data violates GDPR rules. Check your data privacy laws.")
    print("[i] Ctrl+c to terminate")
    sniff(iface=params.interface, prn=frameHandler.handler, store=0)

    # FOR TESTING ONLY, start a thread to hop between channels. Should theoretically not be required for probe requests since they are sent on all channels
    # threading.Thread(target=hopChannel).start()

    ioloop.IOLoop.instance().stop()
    print("[!] Monitoring Stopped.")
    # restart network manager service / not needed for airmon-ng 
    # os.system("sudo service NetworkManager restart")

def hopChannel():
    for channel in itertools.cycle(channels):
        try:
            os.system("sudo iwconfig " + params.interface + " channel " + channel)
        except Exception as e:
            pass
        time.sleep(3)


def getConfig():
    file = open("config.js", 'r')
    configData = file.read().split("var config = ")[1]
    config = json.loads(configData)
    return config


def main():
    global params
    parser = argparse.ArgumentParser(description="DESCRIPTION")
    parser.add_argument('-i', '--interface', help="interface to capture on")
    # Warning, storage of MAC addresses falls under GDPR regulations
    parser.add_argument('-w', '--write', help="Write data to file")
    # Limit signal strength to avoid capturing too much
    parser.add_argument('-lss', '--limitSignalStrength', help="Limit signal strength to avoid capturing too much")
    params = parser.parse_args()

    print("Argos")
    print("'''''''''''''")
    # Check if we recieved the interface as a parameter
    if (not params.interface):
        os.system("iwconfig")
        params.interface = input("Which interface should be used: ")

    # start the NIC monitoring mode with the help of airmon
    os.system("airmon-ng start " + params.interface)

    print("[i] Loading configuration from config.js")
    config = getConfig()

    if (len(config["whitelist"]) > 0 and len(config["blacklist"]) > 0):
        print(
            "[!] Please use only the whitelist or the blacklist, not both.")
        exit(0)

    print("[i] Starting the web socket server...")
    app = web.Application([(r'/', WebSocketSever), ])

    http_server = httpserver.HTTPServer(app)
    http_server.listen(config["serverPort"])
    print("[i] Web socket ready")

    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
