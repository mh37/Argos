Tero recommended going through two earlier projects done in an earlier run of the course, and writing synopsi on them:
https://www.lulu.com/shop/thomas-eulenberger-and-ya%C3%ABl-kermorvant-and-tom-kurenmaa-and-leo-j%C3%A4%C3%A4skel%C3%A4inen/wi-fi-penetration-testing-for-beginners/ebook/product-23646435.html?page=1&pageSize=4
https://github.com/Nikitushka/ProjectIcaros

# WiFi Penetration Testing for Dummies

A project done in spring 2018 for the Infrastructure Project course, which resulted in a book publication detailing the results of the project, running through various basic penetration methods of WiFi networks by cracking password for a lab environment network and testing capturing login information to unprotected sites once connected through packet sniffing.

The project was done purely in a lab environment, with a router/wireless access point the project group sourced for themselves, a target laptop and an attacking laptop with Kali Linux installed and an attached external wifi card capable of packet sniffing and injection.

## Cracking WEP

WEP is an older wireless encryption protocol, with a lot of vulnerabilities. The project group was able to generate the password used by their lab wireless network by capturing authentication packets from the network as another laptop connected to it, replaying captured ARP packets to generate even more traffic and packets, and then finally using a tool in Kali to generate the used password by looking for reused IV values in the encryption. The more authentication packets are captured and stored into the attacking machine, the more likely it is to be able to generate  the used password in such a way, and the ARP packets can be captured by a wifi adapter in monitoring mode even without being directly connected to the network first.

## Cracking WPA/WPA2-PSK with dictionary attack

WPA2 is a more modern encryption method that is used as a standard in Wireless security. The project group did manage to showcase how weak this encryption can still be, if a weak password is used, as it becomes vulnerable to a dictionary attack then. A wifi-adapter in monitoring mode was used to capture and store data from the four-way handshake that occurs when a client connects to the target network, and then the Aircrack -tool (installed by default on Kali Linux) can be used to run a list of pre-written, likely passwords against the data captured from the four-way handshake to generate the password, if the password exists in the pre-written list. This showcases that weak passwords that are likely already recorded in various comprehensive lists easily available to hackers are easy to crack; the hacker wont even get locked out, as they can keep running the test simply against the data that they saved on their own machine.

## Cracking AP with WPS PIN

## Man-in-the-Middle attack with Fluxion

To showcase how users can be more vulnerable than hardware, the project group employed a program called Fluxion, that creates a fake AP similiar to one of the network being attacked, and after deauthorizing clients from the target network, waits for clients to potentially attempt connecting to their fake AP instead. Upon connection to the fake AP, the program will offer a login screen similiar to what can be found from the pre-existing router (Fluxion has a large number of templates to choose from to match numerous routers and providers), intending to fool an user into thinking they have to, for example, install new firmware for their wireless netwrok, and type in the password for the network that is then captured by the attacking laptop. After receiving the password, the client is disconnected from the fake AP and the old AP is no longer deauthorized.The project group does note that this is likely not to work against any users with a modicum of technical expertise, but it is a good proof of concept for users being the weakest link in most systems.

## Post-connection attack: Sniffing login details

## Post-connection attack: Man-in-the-middle and ARP Poisoning

## Post-connection attack: Protocol downgrade attack
