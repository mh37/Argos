#!/usr/bin/python

#This file is purely for temporary testing purposes, Will be removed later.

import re, os, socket, sys, signal, threading, time, subprocess, argparse, itertools


def main():

    print("Welcome to Argos")
    print("'''''''''''''''''''")
    print("Available network interface controllers:")
    print(socket.if_nameindex())
    selectedNIC = input("Which NIC should be used? (Type the name):")

    os.system("airmon-ng check kill")
    os.system("airmon-ng start " + selectedNIC)
    os.system("probequest " + selectedNIC + "mon")


if __name__ == '__main__':
    main()