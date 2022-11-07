# Argos
This tool provides passive WiFi tracking and profiling based on probeframe data. This is ideal for recon and vareous other applications. 

In my specific use-case, the purpose is to showcase how much data and information a persons WiFi capable device reveals without their knowledge.


## Requirements

- Python 
- Python Modules
  - Scapy-python3
  - Tornado
- Airmon-ng
- Wi-Fi Card that supports monitor mode

## Troubleshooting
### Channel hopping isn't working
Make sure your driver installation is correct. Incorrect installations or driver versions can cause the issues with the channel hopping. Make sure that the driver supports monitoring mode and other advanced features that you require. As example a driver like this https://github.com/aircrack-ng/rtl8812au
## Credits 
This project is a fork of https://github.com/smythtech/WifiProbeMapper, and covered under the MIT license. 

WARNING: The storage of MAC addresses is illegal in most countries and may violate your local data privacy laws. Check your local laws first.
