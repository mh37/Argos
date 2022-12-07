# Field Testing Report

Overall, the testing revealed that all Wi-Fi enabled devices revealed SSID data, but not always all of the stored SSIDs within the device.

Currently it remains a unknow to me why some devices only send requests for the current location, while others indiscriminately send out every SSID they know.

Interestingly devices with MAC randomization would not only randomize the address partially but rather completely. So in most cases when a device vendor can't be associated with the MAC it means that the address is randomized. 

Most participants were quite shocked by the outcome and the fact that their device reveals passively so much about them without their knowledge. Some of the participants proceeded to immediately delete all the stored Wi-Fi networks from their device. 

## Tests

All testing was performed on the campus facilities of Haaga-Helia in Helsinki. Each test was executed with the written agreement of the device owner. Signal strength limitation was used to avoid scanning any devices that are more than a few meters away from the network interface controller. All participants were asked to turn on the Wi-Fi on their devices. 

Additionally, I blacklisted SSIDs that are hosted at the test location since they are of no signifficant value to me in this specific test scope and it helps to greatly limit the amount of API calls. I will still mention the appearance of the blacklisted SSIDs in the tests but I am not running any geolocation on them since I know where they are.

### Test 1

>**Date / Time:**
>1.12.2022 / 16:16
>
>**Device/s:**
>Galaxy S20
>
>**Results:**
>I identified five SSIDs belonging to the device owner. The phone sent probe requests out twice under two different MAC addresses. It was possible to crossreference four of the SSIDs with accurate geographical coordinates, two of the requests with SSIDs belonging to the University where the testing was done.
> 

### Test 2

>**Date / Time:**
>1.12.2022 / 17:00
>
>**Device/s:**
>Xiaomi Mi 11 
>
>**Results:**
>I identified four SSIDs belonging to the device owner. It was possible to crossreference three of the SSIDs with accurate geographical coordinates. One showing the home address, the school Wi-Fi, and the Helsinki Hospital.    
>

### Test 3

>**Date / Time:**
>5.12.2022 / 12:35
>
>**Device/s:**
>Google Pixel 6 
>
>**Results:**
>I identified one SSIDs belonging to the device owner. It was possible to crossreference it with the school, but I wasn't able to capture any other SSIDs off this device. The device settings showed that there are 8 more networks saved but nothing else was visible through scanning. 
>

### Test 4

>**Date / Time:**
>5.12.2022 / 13:03
>
>**Device/s:**
>Macbook & iPhone
>
>**Results:**
>I identified four SSIDs belonging to the device owner. One was the school Wi-Fi, one their home Wi-Fi, and one was a public library, and one was the SSID of the free Wi-Fi of trains in Finland. I capture all the SSIDs from both devices. 


### Test 5

>**Date / Time:**
>5.12.2022 / 15:42
>
>**Device/s:**
>Samsung S9+
>
>**Results:**
>I identified six SSIDs belonging to the device owner. Two for University access points (one in the current location), one from their student exchange university in Canada, one from a hotel in Toronto, one from their ex-partners home address, and one from their student apartment, and one from an airport. All locations were able to be mapped by geolocation.  
>

### Test 6

>**Date / Time:**
>7.12.2022 / 14:36
>
>**Device/s:**
>iPhone 8 & Lenovo Thinkpad (Win 11)
>
>**Results:**
>For this participant I only managed to capture probe requests for the school Wi-Fi, no probe requests for other SSIDs were identified. 
>
