# Argos
This tool serves the purpose to showcase the amount of data a Wi-Fi enabled device might reveal about the user. It does so by capturing probe request frames, extracting the SSID value, send it to Wigle to retrieve geographic information of the SSID location, and then show it on a Map with the help of the Google Maps API. 

In short this tool utilizes passive WiFi tracking and profiling based on probe request frames. You can choose to save captured data, but depending on your local laws this might be infringing on data privacy laws. 

Probe requests are usually sent by the clients on all channels, still this tool will be hopping through different all channels to cover the full spectrum of the 2.4GHz and 5GHz frequencies. 


## Requirements

- Python 
- Python Modules
  - Scapy-python3
  - Tornado
- Airmon-ng
- Wi-Fi Card that supports monitor mode
  - Realtek RTL8814AU Driver

## FAQ and Troubleshooting
### Driver issues
Make sure your driver installation is correct. Incorrect installations or driver versions can cause multiple issues in terms of functionality. Make sure that the driver supports monitoring mode and other advanced features that you require. 

In my case I use the following one: https://gitlab.com/kalilinux/packages/realtek-rtl8814au-dkms you can also find a copy of it in this repository in case that this link goes down. Depending on your distro and if you face issues you can also try the following one: https://github.com/aircrack-ng/rtl8812au

### The web interface or the map feature doesn't work
Check that the config file has the correct parameters and API keys Wigle and Google Maps

## Credits 
This project is a fork of https://github.com/smythtech/WifiProbeMapper, and covered under the MIT license. 

WARNING: The storage of MAC addresses is illegal in most countries and may violate your local data privacy laws. Check your local laws first.
