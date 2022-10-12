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


#plc_2 = ModbusClient()
#plc_3 = ModbusClient()
#plc_4 = ModbusClient()

# define modbus server host, port
#plc_2.host(SERVER_HOST_2)
#plc_2.port(SERVER_PORT)

#plc_3.host(SERVER_HOST_3)
#plc_3.port(SERVER_PORT)

#plc_4.host(SERVER_HOST_4)
#plc_4.port(SERVER_PORT)

##
# Will twice check if plc is reachable 
# @return true if plc is reachable 
# @return false if not 
def checkConnectivity(plc):
    if not plc.is_open():
        if not plc.is_open():
            print("Unable to connect to " + plc.host ":" + str(plc.port))
            return False
    return True


##
# create a plc instance
# return plc (ModbusClient) instance  
def initPlc(ip, port):
    plc      = ModbusClient()
    plc.host = ip
    plc.port = port
    return initPlc

## 
# call initPlc with SERVER_HOST_2-4 and SERVER_PORT 
# @return array with all the plcs4
#    array of plcs == [plc-252, plc-253, plc-254]
def initAllPlcs():
    plcs = []
    plcs.append(initPlc(SERVER_HOST_2, SERVER_PORT))
    plcs.append(initPlc(SERVER_HOST_3, SERVER_PORT))
    plcs.append(initPlc(SERVER_HOST_4, SERVER_PORT))
    return plcs


## The main function.
def main():
    # array of plcs == [plc-252, plc-253, plc-254]
    plcs = initAllPlcs()

    # Check if i can connect to every plc 
    for plc in plcs:
        if checkConnectivity(plc) == False:
            exit()
    

    print("wuui")


main()



    