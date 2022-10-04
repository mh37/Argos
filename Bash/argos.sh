#!/bin/bash


#Lets do the same in bash

ifconfig
read -p "Which interface should be used?: " ifName
ifconfig $ifName down
iwconfig $ifName mode monitor
ifconfig $ifName up
probequest $ifName

