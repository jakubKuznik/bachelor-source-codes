# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: factory.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: 

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
        self.plc = ModbusClient(host=ip, port=SERVER_PORT, debug=True)
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

    def getFactoryIo(self):
        return self.di1

    
    # TODO each input output can have function with same name as in factory io 
    def updateDi(self):
        all      = self.plc.read_coils(4, 4)
        self.di1 = all[0]
        self.di2 = all[1]
        self.di2 = all[2]
        self.di2 = all[3]
    
    
    
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
    # set all the digital outputs to 0
    def clearDo(self):
        if self.plc.is_open == True:
            # [Sorter - right, Sorter - left, Right emitter, Left emitter]
            self.plc.write_multiple_coils(0, [False, False, False, False])
            self.do1 = self.do2 = self.do3 = self.do4 = False
            time.sleep(0.1)
    
    ######### DEBUG SECTION 
    def debugDi(self):
        print(str(self.di1), str(self.di2),  str(self.di3), str(self.di4))
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
# do the program (iniinite loop) 
def doProgram(plcs):
    plcs[0].updateDi()
    plcs[0].debugDi()
    print("....")
    while plcs[0].di1 == True:
         
        print("hello world")

        # read on addres 4 read 4 bits 
        # [ IDO4, IDO5, IDO6, IDO7] 
        plcs[0].updateDi()
        plcs[0].debugDi()
        print(plcs[0]) 
        
        time.sleep(0.5)
        plcs

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



    