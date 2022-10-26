#!/usr/bin/python

#This file is purely for temporary testing purposes, Will be removed later.

import re, os, socket, sys, signal, threading, time, subprocess, argparse, itertools
from subprocess import Popen, PIPE


def main():

    print("Welcome to Argos")
    print("'''''''''''''''''''")
    print("Available network interface controllers:")
    print(socket.if_nameindex())
    #subprocess.run("iwconfig")
    selectedNIC = input("Which NIC should be used? (Type the name):")

    #putting the NIC in monitor mode
    subprocess.run(["sudo bettercap -iface ", selectedNIC])


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