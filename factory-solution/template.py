# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: factory.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: Template for projetcs. 

from pickle import TRUE
from pyModbusTCP.client import ModbusClient
import time
import numpy

SERVER_HOST_1 = "192.168.88.251"  # PLC2
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
    def __init__(self, ip):
        # Modbus device 
        self.plc = ModbusClient(host=ip, port=SERVER_PORT)
        self.plc.open() # open tcp connection 
     
        # digital inputs 
        self.di0 = False  # [PLC2: factory.io] [PCL3: ] [PLC4: ]
        self.di1 = False
        self.di2 = False
        self.di3 = False
        
        # digital outputs 
        self.do0 = False
        self.do1 = False
        self.do2 = False
        self.do3 = False
        
        # analoginputs outputs 
        self.ao0 = 0.0
        self.ai0 = 0.0

        # clear Digital outputs  
        self.clearDo()
        time.sleep(0.05)

    ##
    # Write nth DO and sleep
    # @value True or False 
    def writeDo(self, nth ,sleep, value):
        if nth == 0:    self.do0 = value 
        elif nth == 1:  self.do1 = value 
        elif nth == 2:  self.do2 = value
        elif nth == 3:  self.do3 = value

        self.applyDo()
        time.sleep(sleep)
        self.clearDo()
    
    ##
    # Write nth DO and sleep
    def writeDoNoClear(self, nth ,sleep, value):
        if nth == 0:    self.do0 = value 
        elif nth == 1:  self.do1 = value
        elif nth == 2:  self.do2 = value
        elif nth == 3:  self.do3 = value

        self.applyDo()
        time.sleep(sleep)

    ##
    # @array = [True, True, False, False]
    def writeMultipleDo(self, array, sleep):
        self.do0 = array[0]
        self.do1 = array[1]
        self.do2 = array[2]
        self.do3 = array[3]
        self.applyDo()
        time.sleep(sleep)
        self.clearDo()
    
    ##
    # @array = [True, True, False, False]
    def writeMultipleDoNoClear(self, array, sleep):
        self.do0 = array[0]
        self.do1 = array[1]
        self.do2 = array[2]
        self.do3 = array[3]
        self.applyDo()
        time.sleep(sleep)
    
    ##
    # update all Digital inputs 
    def updateDi(self):
        all      = self.plc.read_coils(4, 4)
        self.di0 = all[0]
        self.di1 = all[1]
        self.di2 = all[2]
        self.di3 = all[3]
    
    ##
    # Will twice check if plc is reachable 
    # @return true if plc is reachable 
    # return false if not 
    def checkConectivity(self):
        while self.plc.is_open == False:
            print(self.plc.is_open)
        if not self.plc.is_open:
            if not self.plc.is_open:
                print("Unable to connect to " + str(self.plc.host) + ":" + str(self.plc.port))
                print(self.plc)
                return False
        return True

    ##
    # Write all digital outputs.
    def applyDo(self):
        self.plc.write_single_coil(0, self.do0)  
        self.plc.write_single_coil(1, self.do1)  
        self.plc.write_single_coil(2, self.do2)  
        self.plc.write_single_coil(3, self.do3)  

    ##
    # Set all digital outputs to 0.
    def clearDo(self):
        if self.plc.is_open == True:
            # [Sorter - right, Sorter - left, Right emitter, Left emitter]
            self.plc.write_multiple_coils(0, [False, False, False, False])
            self.do0 = self.do1 = self.do2 = self.do3 = False
    
    ######### DEBUG SECTION 
    def debugDi(self):
        print(str(self.di0), str(self.di1),  str(self.di2), str(self.di3))
    def debugDo(self):
        print(str(self.do0), str(self.do1),  str(self.do2), str(self.do3))
    #######################

    ##
    # destructor 
    def __del__(self):
        print("end tcp sessions")
        self.plc.close() # end tcp connection 

## 
# call initPlc with SERVER_HOST_2-4 and SERVER_PORT 
# @return array with all the plcs4
#    array of plcs == [plc-252, plc-253, plc-254]
def initAllPlcs():
    plcs = []
    plcs.append(Plc(SERVER_HOST_1))
    plcs.append(Plc(SERVER_HOST_2))
    plcs.append(Plc(SERVER_HOST_3))
    plcs.append(Plc(SERVER_HOST_4))
    plcs[0].writeMultipleDoNoClear([False, False, False, False], 0)
    plcs[1].writeMultipleDoNoClear([False, False, False, False], 0)
    plcs[2].writeMultipleDoNoClear([False, False, False, False], 0)
    plcs[3].writeMultipleDoNoClear([False, False, False, False], 0)
    return plcs

##
# do the program (infinite loop) 
def doProgram(plcs):
    PAUSE_SHORT=0.2
    PAUSE=0.5
    PAUSE_LONG=1
    PAUSE_LONGEST=1.1

    ## Progam not enabled 
    plcs[1].updateDi()
    while plcs[1].di3 == True:
        plcs[1].updateDi()

    # while factory io is running 
    plcs[2].updateDi()
    while plcs[2].di0 == True:
        plcs[2].updateDi()


## The main function.
def main():
    
    # array of plcs == [plc-2, plc-3, plc-4]
    # array with instances of Plc class
    plcs = initAllPlcs()
    
    # check if all plcs are reachable  
    for plc in plcs:
        if plc.checkConectivity() == False:
            print("Can't connect to PLC")
            exit()

    doProgram(plcs)
    print("Program end")


# call main 
main()



    
