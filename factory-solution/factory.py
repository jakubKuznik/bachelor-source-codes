# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: factory.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: 

from asyncore import read
from turtle import clear
from pyModbusTCP.client import ModbusClient
import time
import sys

SERVER_HOST_2 = "192.168.88.252"  # PLC2
SERVER_HOST_3 = "192.168.88.253"  # PLC3
SERVER_HOST_4 = "192.168.88.254"  # PLC4

# port, same for all PLCs
SERVER_PORT = 502


##
# Class Plc represents one "UniPi Neuron S103" PLC
#  user should get all the information about plc from here 
#
#  ----|-------|------|-----|-------|----- 
#  -  DI1     DI2    DI3   DI4     Ai0   -
#  -                                     - 
#  -         UniPi Neuron S103           ------ETH----- 
#  -                                     -
#  -  DO1     DO2    DO3   DO4     Ao0   -
#  ----|--------|-----|------|------|------
#
class Plc:
    def __init__(self, ip, port):
        # Modbus device 
        self.plc      = ModbusClient()
        self.plc.host = ip
        self.plc.port = port
        
        # digital inputs 
        self.di1 = False
        self.di2 = False
        self.di3 = False
        self.di4 = False
        
        # digital outputs 
        self.do1 = False
        self.do2 = False
        self.do3 = False
        self.do4 = False
        
        # analoginputs outputs 
        self.ao0 = 0.0
        self.ai0 = 0.0

        # clear Digital outputs  
        self.clearDo(self)

    ##
    # Will twice check if plc is reachable 
    # @return true if plc is reachable 
    # return false if not 
    def checkConnectivity(self):
        if not self.plc.is_open():
            if not self.plc.is_open():
                print("Unable to connect to " + str(self.plc.host) ":" + str(self.plc.port))
                return False
        return True
    

    ##
    # set all the digital outputs to 0
    def clearDo(self):
        if self.plc.is_open():
            # plc_2.write_single_coil(0, False)  # Sorter - right
            # plc_2.write_single_coil(1, False)  # Sorter - left
            # plc_2.write_single_coil(2, False)  # Right emitter
           # plc_2.write_single_coil(3, False)  # Left emitter

            # [Sorter - right, Sorter - left, Right emitter, Left emitter]
            self.plc.write_multiple_coils(0, [False, False, False, False])
            self.do1 = self.do2 = self.do3 = self.do4 = False
            time.sleep(0.1)


    def updateDi():
        #TODO
        isRunning = plc_2.read_coils(4, 1)[0]

        print(" ")
    
    def updateDi():
        #TODO
        print(" ")


## 
# call initPlc with SERVER_HOST_2-4 and SERVER_PORT 
# @return array with all the plcs4
#    array of plcs == [plc-252, plc-253, plc-254]
def initAllPlcs():
    plcs = []
    plcs.append(Plc(SERVER_HOST_2, SERVER_PORT))
    plcs.append(Plc(SERVER_HOST_3, SERVER_PORT))
    plcs.append(Plc(SERVER_HOST_4, SERVER_PORT))
    return plcs

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
    # array with instances of Plc class
    plcs = initAllPlcs()
    
    # check if all plcs are reachable  
    for plc in plcs:
        if plc.checkConectivity() == False:
            exit()

    doProgram(plcs)




    print("Program end")


main()



    