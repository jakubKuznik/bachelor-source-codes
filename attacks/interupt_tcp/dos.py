# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: dos.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description:.

from scapy.all import * 
from pyModbusTCP.client import ModbusClient
import threading
import multiprocessing

SLAVE2 = "192.168.88.252"  # PLC2
SERVER_PORT = 502

# establish tcp connection with device 
plc2 = ModbusClient(host=SLAVE2, port=SERVER_PORT)
plc2.open()

while True:
  plc2.read_coils(4,4)
  time.sleep(2)
  print("kulo")

