#!/usr/bin/python



import re, os, socket, sys, signal, threading, time, subprocess, argparse, itertools
from subprocess import Popen, PIPE

#TODO: Processing / Analyzing, Formatting / Output / Map Visualisation (wigly API call based on hotspot names)
def main():

    data = []

    print("Welcome to Argos")
    print("'''''''''''''''''''")
    print("Available network interface controllers:")
    #print(socket.if_nameindex())
    subprocess.run("iwconfig")
    selectedNIC = input("Which NIC should be used? (Type the name):")

    #putting the NIC in monitor mode
    subprocess.run(["sudo", "bettercap", "-iface", selectedNIC, "wifi.recon", "on"])
    #subprocess.run(["wifi.recon", "on"])

def print_capturedData():


#Retrieve vendor based on MAC address
def check_vendor(mac):
    with open('macvendors.txt', 'r') as f:
        for line in f:
            l = line.split('\t')
            if l[0].lower() in mac.replace(':', '') :
                return l[1].strip()
    return 'N/A'

if __name__ == '__main__':
    main()