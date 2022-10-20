# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: factory.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: 

from pickle import TRUE
from tkinter.tix import Tree
from pyModbusTCP.client import ModbusClient
import time

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
        self.di1 = False  # [PLC2: factory.io] [PCL3: ] [PLC4: ]
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
        self.clearDo()
        time.sleep(0.05)

    ##
    # Write nth DO and sleep
    def writeDo(self, nth ,sleep):
        if nth == 1:    self.do1 = True 
        elif nth == 2:  self.do2 = True 
        elif nth == 3:  self.do3 = True 
        elif nth == 4:  self.do4 = True 


        self.applyDo()
        time.sleep(sleep)
        self.clearDo()

    
    def getFactoryIo(self):
        return self.di1
    
    # TODO each input output can have function with same name as in factory io 
    def updateDi(self):
        all      = self.plc.read_coils(4, 4)
        self.di1 = all[0]
        self.di2 = all[1]
        self.di3 = all[2]
        self.di4 = all[3]
    
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
    # Write digital outputs
    def applyDo(self):
        self.plc.write_single_coil(0, self.do1)  # Bases emitter
        self.plc.write_single_coil(1, self.do2)  # Bases emitter
        self.plc.write_single_coil(2, self.do3)  # Bases emitter
        self.plc.write_single_coil(3, self.do4)  # Bases emitter


    ##
    # set all the digital outputs to 0
    def clearDo(self):
        if self.plc.is_open == True:
            # [Sorter - right, Sorter - left, Right emitter, Left emitter]
            self.plc.write_multiple_coils(0, [False, False, False, False])
            self.do1 = self.do2 = self.do3 = self.do4 = False
    
    ######### DEBUG SECTION 
    def debugDi(self):
        print(str(self.di1), str(self.di2),  str(self.di3), str(self.di4))
    def debugDo(self):
        print(str(self.do1), str(self.do2),  str(self.do3), str(self.do4))
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
    plcs.append(Plc(SERVER_HOST_2))
    plcs.append(Plc(SERVER_HOST_3))
    plcs.append(Plc(SERVER_HOST_4))
    return plcs

##
# do the program (infinite loop) 
def doProgram(plcs):
    plcs[0].updateDi()
    plcs[0].debugDi()
    
    PAUSE=0.05

    while plcs[0].di1 == True:
         
        # read on addres 4 read 4 bits 
        # [ IDO4, IDO5, IDO6, IDO7] 
        plcs[0].updateDi()
        time.sleep(PAUSE)

        # move roller 
        plcs[0].writeDo(1, PAUSE)

        ## diffuse sensor trigger 
        if plcs[0].di2 == True:
            print("sensor")



        plcs[0].updateDi()
        time.sleep(PAUSE)



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



    