# Initial Setup

The purpose of the project was, at least initially, to create a framework that used collected WiFi device data to generate physical traffic statistics; for example, collecting device identifying data sets from two different physical points, saving them into a database and then crossreferencing them to create numerical data on how many people commuted from point A to point B.

For the initial setup and development of software and scripts, we set out to setup a Raspberry Pi device with a connected external WiFi adapter capable of being switched to monitoring mode (in this case an Alfa AWUS1900 card). A raspberry Pi 3 was also borrowed, but later changed to a Raspberry Pi 4B for the added RAM capacity and to solve some compatability issues.

## First setup

At first, we used the Raspberry Pi 3 provided to us by the course teacher, with Debian 11 Bullseye installed on it. The Raspberry was brought to the Servula lab on Pasila campus, and given a static IP address on the lab network courtesy of the teachers. The purpose of holding the RPI at the lab environment was to allow for easy remote access for both project members at seperate times. After setting the RPI up at the lab and it's initial configuration, the Alfa card was connected, and required drivers were installed.

Along with the Alfa card drivers, the following software packages were installed:
- wget
- xz utils
- net-tools
- usbutils
- dkms
- wireless-tools
- python3-pip
- airmon-ng
- aircrack-ng
- probequest
- python3-scapy libraries

Using the command `airmon-ng start wlan1` (wlan0 was the internal wifi adapter of the RPI) successfully turned the alfa card to monitoring mode at this point. However, trying to launch probequest resulted in a collection of Scapy errors. Extensive troubleshooting by both project members could not come up with a solution to fix them, so at this point we decided to upgrade to a Raspberry Pi 4B used by Jaakko for better technical specs, and install Kali Linux on it at the same time.

## Second Setup

