# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: factory.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: 

from asyncore import read
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


#TODO
class PLC:
    def __init__(self):
        self.do1 = False
        self.do2 = False
        self.do3 = False
        self.do4 = False
        
        self.di1 = False
        self.di2 = False
        self.di3 = False
        self.di4 = False

        self.ai0 = 0.0
        self.ai1 = 0.0
    

    def updateDi():
        #TODO
        print(" ")
    
    def updateDi():
        #TODO
        print(" ")

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

##
# set all the coils of the plc to 0
def clearCoils(plc):
    if plc.is_open():
        # plc_2.write_single_coil(0, False)  # Sorter - right
        # plc_2.write_single_coil(1, False)  # Sorter - left
        # plc_2.write_single_coil(2, False)  # Right emitter
        # plc_2.write_single_coil(3, False)  # Left emitter

        # [Sorter - right, Sorter - left, Right emitter, Left emitter]
        plc.write_multiple_coils(0, [False, False, False, False])
        time.sleep(0.1)

##
# do the program (iniinite loop) 
def doProgram(plcs):
    while True: 
        print("hello world")

        # read on addres 4 read 4 bits 
        # [ IDO4, IDO5, IDO6, IDO7] 
        print(plcs[0].read_coils(4, 4))
        
        time.sleep(0.5)

## The main function.
def main():

    # array of plcs == [plc-2, plc-3, plc-4]
    plcs = initAllPlcs()

    # Check if i can connect to every plc 
    for plc in plcs:
        if checkConnectivity(plc) == False:
            exit()
    
    # clear coils 
    for plc in plcs:
        clearCoils(plc)


    # TODO MAYBE SOME CLASS FOR PLC WHERE ALL THE PORTS WILL HAVE SOME NAME 
    #       I COULD INSTANTCIATE PLC THEN..
    doProgram(plcs)




    print("wuui")


main()



    