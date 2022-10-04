#!/bin/bash


#a basic probe request capture using the probequet tool. Just for testing.

iwconfig
read -p "Which interface should be used?: " ifName

#systemctl stop NetworkManager
#ifconfig $ifName down
airmon-ng check kill
#iw $ifName set monitor control
airmon-ng start $ifName
probequest $ifName


#sudo ip link set wlan# up
