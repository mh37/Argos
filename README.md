# Argos
This tool provides passive WiFi tracking and profiling based on probeframe data. This is ideal for recon and vareous other applications. 

The main goal is to be able to record and cross reference devices based on monitoring locations and the captured MAC addresses between multiple location. Due to MAC randomization, in most applications you will have to run some machine learning magic to create a unique identifier for the braodcase devices based on their signal pattern and probequest behaviour. 

Without the randomization you are pretty much limited to unique SSID broadcasts as the identifier. 


Requirements

- Python
- Scapy
