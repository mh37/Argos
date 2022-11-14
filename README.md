# Argos
This tool serves the purpose to showcase the amount of data a Wi-Fi enabled device might reveal about the user. It does so by capturing probe frames, extracting the SSID value, send it to Wigle to retrieve geographic information of the SSID location, and then show it on a Map with the help of the Google Maps API. 

In short this tool utilizes passive WiFi tracking and profiling based on probeframe data. You can choose to save captured data, but depending on your local laws this might be infringing on data privacy laws. 


## Requirements

- Python 
- Python Modules
  - Scapy-python3
  - Tornado
- Airmon-ng
- Wi-Fi Card that supports monitor mode
  - Realtek RTL8814AU Driver

## Troubleshooting
### Driver issues
Make sure your driver installation is correct. Incorrect installations or driver versions can cause multiple issues in terms of functionality. Make sure that the driver supports monitoring mode and other advanced features that you require. 

In my case I use the following one: https://gitlab.com/kalilinux/packages/realtek-rtl8814au-dkms you can also find a copy of it in this repository in case that this link goes down. Depending on your distro and if you face issues you can also try the following one: https://github.com/aircrack-ng/rtl8812au

## Credits 
This project is a fork of https://github.com/smythtech/WifiProbeMapper, and covered under the MIT license. 

WARNING: The storage of MAC addresses is illegal in most countries and may violate your local data privacy laws. Check your local laws first.
