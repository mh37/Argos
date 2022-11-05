#!/usr/bin/python3

import logging

from scapy.layers.dot11 import Dot11

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # Supress scapy warnings
from scapy.all import *
import argparse
import json
import hashlib
from http.client import HTTPSConnection
import urllib
from tornado import websocket, web, httpserver, ioloop

class WebSocketSever(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print("[i] Client connected")
        try:
            sniffer(self)
        except PermissionError as e:
            print("[!] Permissions insufficient. Run as root!")
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
        if (frame.haslayer(Dot11) and (frame.type == 0x0 or frame.type == 0x04)):
            try:
                probeSSID = str(frame.info)[2:-1]
                if (len(probeSSID) > 0):
                    info = {}
                    info['device'] = frame.addr2
                    info['ssid'] = probeSSID
                    if (len(self.config["whitelist"]) > 0 and (info['ssid'] not in self.config["whitelist"])):
                        return
                    if (len(self.config["blacklist"]) > 0 and (info['ssid'] in self.config["blacklist"])):
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
            dataJson = json.loads(data)
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
            self.seen.append(hashlib.md5(str(info).encode('utf-8')).hexdigest())
        except:
            print("[!] Error. Could not add SSID to History")

    def checkDuplicate(self, info):
        try:
            return (hashlib.md5(str(info).encode('utf-8')).hexdigest() in self.seen)
        except:
            print("[!] Error. Could not check if the SSID is known")
            return True


def sniffer(context):
    frameHandler = FrameHandler(context, getConfig(), params.write)
    print("[i] Monitoring for probe requests on NIC: " + params.interface + "...")
    if (params.write is not None):
        print("[#] Saving output to: " + params.write)
        print("[WARNING] The captured data falls under GDPR rules.")
    print("[i] Ctrl+c to terminate")
    sniff(iface=params.interface, prn=frameHandler.handler, store=0)
    ioloop.IOLoop.instance().stop()
    print("[!] Monitoring Stopped.")


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
            "[!] There is a whitelist and blacklist set. This might lead to some unexpected behaviour! Please use only the whitelist or only the blacklist.")
        exit(0)

    print("[i] Starting the web socket server...")
    app = web.Application([(r'/', WebSocketSever), ])

    http_server = httpserver.HTTPServer(app)
    http_server.listen(config["serverPort"])
    print("[i] Web socket ready")

    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
