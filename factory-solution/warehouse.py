# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: factory.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: Solution for automatic warehouse. 

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

# TODO i should handle tcp RST flags 


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


# class represents warehouse 9x6
# [0,0] [0,1] ... [0,8]
# [1,0] [1,1] ... [1,8]
#   .     .    .    .
#   .     .    .    .
# [5,0] [5,1] ... [5,8]
class Warehouse:
    
    def __init__(self):
        self.matrix = numpy.full((6, 9), False)

    def printMatrix(self):
        print(self.matrix)

    # Will find free space in warehouse 
    # @return matrix cordinates (0,0) or -1 if warehouse is full
    def findFree(self):
        for y in range(0,6):
            for x in range(0,9):
                if self.matrix[y,x] == False:
                    return y, x 
        return -1

    ## Calculate index of first free warehouse cell
    # (0,0) == 110 110
    # (0,1)
    def calcIndex(self):
        # if warehouse is full 
        if self.findFree() == -1:
            return -1

        position = 0
        wareSize = 54 # (0,0) will be on 54 
                      # (6,9) will be on  1
        rowLenght = 9

        a = 0       # temp variable 
        row = 0     
        column = 0
        print("free: " + str(self.findFree()))
        # transform matrix cordinates to two number 
        for i in self.findFree():
            if a == 0:
                row = i
            else:
                column = i
            a = a+1

        position = wareSize - rowLenght*row - column
        return position

        
    ## default   == 000 000
    ## (1,1)     == 000 001  left down 
    ## (6,1)     == 000 111
    ## (7,1)     == 001 000
    ## (8,1)     == 001 001
    ## (1,1)     == 001 010
    ## (8,6)     == 110 101
    ## (9,6)     == 110 110  right up 
    # LSB plcs[2].writeDoNoClear(0, PAUSE, True) 
    #     plcs[2].writeDoNoClear(1, PAUSE, True)
    #     plcs[2].writeDoNoClear(2, PAUSE, True)
    #     plcs[2].writeDoNoClear(3, PAUSE, True)
    #     plcs[3].writeDoNoClear(0, PAUSE, True)
    # MSB plcs[3].writeDoNoClear(1, PAUSE, True) 
    def moveToEmpty(self, plcs):
        
        index = self.calcIndex()
        print("index: " + str(index))

        # Full warehouse 
        if index == -1:
            return -1
        
        ## Set cell to not empty  
        free = self.findFree()
        self.matrix.itemset(free, True)

        PAUSE = 0

        # set everything to 0
        plcs[2].writeMultipleDoNoClear([False, False, False, False], 0)
        plcs[3].writeMultipleDoNoClear([False, False, False, False], 0)

        # bitMasks, convert index to digital outputs 
        if index & 32 == 32:
            plcs[3].writeDoNoClear(1, PAUSE, True) # MSB
        if index & 16 == 16:
            plcs[3].writeDoNoClear(0, PAUSE, True)
        if index & 8 == 8:
            plcs[2].writeDoNoClear(3, PAUSE, True)
        if index & 4 == 4:
            plcs[2].writeDoNoClear(2, PAUSE, True)
        if index & 2 == 2:
            plcs[2].writeDoNoClear(1, PAUSE, True)
        if index & 1 == 1:
            plcs[2].writeDoNoClear(0, PAUSE, True) # LSB 
        time.sleep(7)

    ## Move lifter to base position 
    def zeroPosition(self, plcs):
        PAUSE = 0.05
        # set everything to 0
        # DEFAULT pos is on 55
        plcs[2].writeDoNoClear(0, PAUSE, True)
        plcs[2].writeDoNoClear(1, PAUSE, True)
        plcs[2].writeDoNoClear(2, PAUSE, False)
        plcs[2].writeDoNoClear(3, PAUSE, True)
        plcs[3].writeDoNoClear(0, PAUSE, True)
        plcs[3].writeDoNoClear(1, PAUSE, True)
        
        
        # FORK LIFT DOWN 
        plcs[0].writeDoNoClear(1, PAUSE, False)  
        time.sleep(7)


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
    PAUSE_SHORTEST=0.1
    PAUSE_SHORT=0.2
    PAUSE=0.5
    PAUSE_LONG=1
    PAUSE_LONGEST=1.1

    ## Progam not enabled 
    plcs[1].updateDi()
    while plcs[1].di3 == True:
        plcs[1].updateDi()

    # MATRIX 6x9
    ware = Warehouse()
    ware.printMatrix() 

    # while factory io is running 
    plcs[2].updateDi()
    while plcs[2].di0 == True:

        # Move roller till item reach gripper  
        plcs[2].updateDi()
        plcs[2].debugDi()
        while plcs[2].di1 == False:
            #do0 First entry roller do1 second entry roller 
            plcs[1].writeMultipleDo([True, True, True, True], PAUSE_SHORTEST) 
            plcs[2].updateDi()
        
        plcs[0].writeDoNoClear(0, PAUSE_LONG, True)   # FORK INPUT
        plcs[0].writeDoNoClear(1, PAUSE_LONG, True)   # FORK LIFT UP
        plcs[0].writeDoNoClear(0, PAUSE_LONG, False)  # FORK INPUT BACK 

        ware.printMatrix() 
        ware.moveToEmpty(plcs)
            
        plcs[0].writeDoNoClear(2, PAUSE_LONG, True)   # FORK OUTPUT 
        plcs[0].writeDoNoClear(1, PAUSE_LONG, False)  # FORK LIFT DOWN 
        plcs[0].writeDoNoClear(2, PAUSE_LONG, False)  # FORK OUTPUT BACK 

        ware.zeroPosition(plcs)


    plcs[1].updateDi()


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



    
