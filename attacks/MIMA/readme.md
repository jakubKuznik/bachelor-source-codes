# About
This is MIMA that uses `arpspoof` tool for arp cache poisoning.
`mima.py` program redirects packets to their true recipients by changing the packets' destination MAC. It also modifies each n-th Modbus packet data part. 
Program can be easily modified for whatever MIMA attack. 

# Run
## 1. Arp cache poisoning 
`sudo arp-spoofing.sh`
## 2. Attack 
`sudo python3 ./mima.py`

## Debug on attacked devices
# linux:
`arp -a -i eno2`

# windows:
`arp -a`
 
