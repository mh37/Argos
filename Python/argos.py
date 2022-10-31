#!/usr/bin/python

import re, os, socket, sys, signal, threading, time, subprocess, argparse, itertools
from subprocess import Popen, PIPE


def main():
    # TODO: Processing / Analyzing, Formatting / Output / Map Visualisation (wigly API call based on hotspot names)
    data = []

    print("Welcome to Argos")
    print("'''''''''''''''''''")
    print("Available network interface controllers:")
    #print(socket.if_nameindex())
    subprocess.run("iwconfig")
    selectedNIC = input("Which NIC should be used? (Type the name):")

    #start monitoring on the selected NIC
    #subprocess.run(["sudo", "bettercap", "-iface", selectedNIC], input="wifi.recon on")
    proc = Popen(["sudo", "bettercap", "-iface", selectedNIC], stdin=PIPE, stdout=PIPE, shell=True)
    output = proc.communicate(b"wifi.recon on\n")[0]  # send 1 to test.exe
    print(output)

if __name__ == '__main__':
    main()