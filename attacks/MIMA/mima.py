# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: mima.py
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: 


from scapy.all import *

# Define the network interfaces to listen on and forward packets to
listen_interface = "eth0"
forward_interface = "eth1"

# Define the function that will be called for each received packet
def handle_packet(packet):
    # Modify the packet's source and destination MAC addresses to forward it to the other interface
    packet.src, packet.dst = packet.dst, packet.src
    # Send the packet out the other interface
    sendp(packet, iface=forward_interface)

# Start sniffing packets on the listen interface and call the handle_packet function for each packet received
sniff(iface=listen_interface, prn=handle_packet)



    