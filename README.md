# Argos

This tool serves the purpose to showcase the amount of data a Wi-Fi enabled device might reveal about the user. It does so by capturing probe request frames, extracting the SSID value, send it to Wigle to retrieve geographic information of the SSID location, and then show it on a Map with the help of the Google Maps API.

In short this tool utilizes passive WiFi tracking and profiling based on probe request frames. You can choose to save captured data, but depending on your local laws this might be infringing on data privacy laws.

## Arguments / Parameters

The tool currently supports the following arguments:

Network Interface: ```-i```
Write data to a certain location: ```-w```
Limit signal strength range: ```-lss```

As example, the following command will run the tool on NIC wlan1 and only capture probe requests that have a signal strength of -50 or higher.

```sudo python3 ./argos.py -i wlan1 -lss '-50'```

It is important to use the lss parameter if you want to limit the range of what you are scanning. This may be crucial depending on your environment and legal restrictions. 

## Ethics

This tool was only used in controlled environments under strict ethic guidelines, and with the explicit permission of the device owners and the owner of the physical facility and infrastructure. All report data and test results which are published here have been anonymized. While the tool itself works of passive data, it easy to violate privacy and data protection laws by capturing something that wasn't inteded to be captured. Any usage of this tool should be limited to controlled environments and with extensive permissions of all involved parties.

## Screenshots

Below you can an example of the tool in action. We are filtering here by signal strenght to cherry pick a target out of a location with many devices.

In this example, we managed to isolate three devices (MAC addresses) that have an identical signal strenght, and map the captured SSIDs through Wigle to a residential address, a cafe, and a local university. The rest could't be assigned to coordinates but is still of high value information. As example the device that pinged for the before mentioned locations was also sending a probe request for an SSID that was called IPhone (First Name of the person). Now we know that the person is using an IPhone, what their name and address is, where they might buy their coffee, and where they go to school.

![Web UI](https://github.com/mh37/Argos/blob/Development/Reports/Pictures/argos-webUI.png?raw=true)

## Hardware Used

- An old laptop with Kali Linux
  - Or a Raspberry Pi for more long term or low profile recording.
- Alfa AC1900 WiFi Adapter (highly recommended for optimal performance)
  - Also works on some Intel AC WiFi cards which are common on modern laptops but your milage may vary. It worked when I tested it on a Intel AC 9560
  - I heard that with a modified driver you can also run the wireless NIC of some Raspberry Pi models in monitoring mode. But I did not test this.

![Web UI](https://github.com/mh37/Argos/blob/Development/Reports/Pictures/setup.jpg?raw=true)

## Requirements

- Python3
- Python Modules
  - Scapy-python3
  - Tornado
- Airmon-ng
- Wi-Fi Card that supports monitor mode
  - Realtek RTL8814AU Driver

## Core Functionality

- Web Interface (so we can access the tool even if we are not near our monitoring device)
- Scan for probe requests
- Ignore duplicate requests
- Utilize Blacklist and Whitelist for SSIDs
- Obtain coordinates based on SSID names
- Show SSID location as markers on Google Maps
- Dynamic filtering of output data (Signal strength, SSID, MAC, Vendor)
- Saving of recorded data (WARNING: This may be illegal in your country)

## Limitations

- limited amount of API calls with Wigle free tier
- Vendor List is lacking
- some devices are a lot more careful with their probe requests
- MAC randomization make it a lot harder to fingerprint devices, especially for long term tracking. Nevertheless, it doesn't make it impossible. For more information check out [Why MAC Address Randomization is not Enough:
  An Analysis of Wi-Fi Network Discovery Mechanisms](https://papers.mathyvanhoef.com/asiaccs2016.pdfhttps:/)

## API integrations

Currently, the script is dependent on two API integrations. One is Wigle, a war-driving database which is used to obtain coordinates of SSIDs. The other one is Google Maps to visualize the coordinates obtained by Wigle as map markers.

One big drawback here is that the free tier of the Wigle API access has a very limited amount of calls per day, which can be an issue if you need to send a lot of requests. You might want to utilize a different API for more intensive use, but as a proof of concept Wigle will do just fine.

## Probe Requests

Probe requests that we capture contain the signal strength (RSSI), MAC-Address of the client and the SSID name the client is probing for. We can use the first part of the MAC address to also match this with a vendor.

According to IEEE 802.11-2012 the probe request frame body can contain the data listed below. This standard is outdated, but I do not have access to IEEE 802.11-2020 which is the newest specification. If you do you should find the information on page 843, and I gladly update it here if you can send it to me.

### Mandatory

- SSID
- Supported rates

### Optional

- Extended supported rates
- Request information
- DSS parameter set
- Supported Operating classes
- HT capabilities
- 20/40 BSS coexistence
- Extended capabilities
- SSID list
- Channel Usage
- Interworking
- Mesh ID

Most of these values are optional and require specific flags to be true on the client side to be included in the probe request. As example the SSID List property will require dot11MgmtOptionSSIDListActivated to be set to true. So most of the time you will not encounter such information.

## Pending Features and Improvements

- Device fingerprinting with the help of machine learning
- Support multiple APIs for SSID coordinates
- Support multiple Map APIs

## FAQ and Troubleshooting

### Driver issues

Make sure your driver installation is correct. Incorrect installations or driver versions can cause multiple issues in terms of functionality. Make sure that the driver supports monitoring mode and other advanced features that you require.

In my case I use [this one](https://gitlab.com/kalilinux/packages/realtek-rtl8814au-dkms) you can also find a copy of it in this repository in case that this link goes down. Depending on your distro and if you face issues you can also try the driver from [aircrack-ng](https://github.com/aircrack-ng/rtl8812au)

### The web interface or the map feature doesn't work

Check that the config file has the correct parameters and API keys Wigle and Google Maps

## Credits

The list with MAC addresses and vendor identities is a direct copy of this [Vendor List](https://gist.github.com/aallan/b4bb86db86079509e6159810ae9bd3e4)

The initial base of this project was forked from [WifiProbeMapper](https://github.com/smythtech/WifiProbeMapperhttps:/).

WARNING: The storage of MAC addresses is illegal in most countries and may violate your local data privacy laws. Check your local laws first.
