# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: factory.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: 

from pyModbusTCP.client import ModbusClient
import time
import sys

SERVER_HOST_2 = "192.168.88.252"  # PLC2
SERVER_HOST_3 = "192.168.88.253"  # PLC3
SERVER_HOST_4 = "192.168.88.254"  # PLC4

# port, same for all PLCs
SERVER_PORT = 502

plc_2 = ModbusClient()
plc_3 = ModbusClient()
plc_4 = ModbusClient()

# define modbus server host, port
plc_2.host(SERVER_HOST_2)
plc_2.port(SERVER_PORT)

plc_3.host(SERVER_HOST_3)
plc_3.port(SERVER_PORT)

plc_4.host(SERVER_HOST_4)
plc_4.port(SERVER_PORT)

# The main function in which all the steps for controlling the assembly line are defined.
def start():
    print("wi")
start()
