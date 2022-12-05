# Field Testing Report

Overall, the testing revealed that all Wi-Fi enabled devices revealed SSID data, but not always all of the stored SSIDs within the device. I am not sure what the exact logic is to what probeframe requests are sent out, and if there may be some kind of geographic filtering occuring on the device side. It may also be that people simply didn't have any other SSIDs stored. Interestingly devices with MAC randomization would not only randomize the address partially but rather completely. So in most cases when a device vendor can't be associated with the MAC it means that the address is randomized. 

## Tests

All testing was performed on the campus facilities of Haaga-Helia in Helsinki. Each test was executed with the written agreement of the device owner. Signal strength limitation was used to avoid scanning any devices that are more than a few meters away from the network interface controller.

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



