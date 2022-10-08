# This file belongs to TRACTOR project.
# 
# File name: cv2.py
# Authors: Mária Masárová   <xmasar13>
#          Ján Pristaš      <xprist06>
# Description: Assembly line control script.

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

################################################
# 1. Add host and port to PLC3 and PLC4 - TODO #
################################################



# The main function in which all the steps for controlling the assembly line are defined.
def start():
    # check for connections
    if not plc_2.is_open():
        if not plc_2.open():
            print("Unable to connect to " + SERVER_HOST_2 + ":" + str(SERVER_PORT))

    if not plc_3.is_open():
        if not plc_3.open():
            print("Unable to connect to " + SERVER_HOST_3 + ":" + str(SERVER_PORT))

    if not plc_4.is_open():
        if not plc_4.open():
            print("Unable to connect to " + SERVER_HOST_4 + ":" + str(SERVER_PORT))

    # initialize all values to 0 (False)
    if plc_2.is_open():
        plc_2.write_multiple_coils(0, [False, False, False, False])
        time.sleep(0.2)

    ######################################
    # 2. Initialize PLC3 and PLC4 - TODO #
    ######################################





    # if we have connections with all PLCs
    if plc_2.is_open() and plc_3.is_open() and plc_4.is_open():
        # start assembly line in Factory I/O program
        plc_2.write_single_coil(2, True)  # FACTORY I/O (Run) actuator
        time.sleep(0.5)

        # repeat until the user stops the line
        while True:
            # check if still running
            isRunning = plc_2.read_coils(4, 1)[0]
            time.sleep(0.1)

            if not isRunning:
                break

            ###################################
            # 3. Turn on both emittors - TODO # 
            ###################################


            time.sleep(0.1)

            # turn on both conveyors
            # [Lids conveyor 1, Bases conveyor 1, RP1 Clamp, RP2 Clamp]
            plc_4.write_multiple_coils(0, [True, True, False, False])
            time.sleep(0.1)

            ##########################
            # 4. Read sensors - TODO #
            ##########################
            # [Factory I/O (Running), Lid emitted, Base emitted, ---]


            time.sleep(0.1)

            # while sensors didn't detect anything
            while not plc_2_values[1] or not plc_2_values[2]:
                plc_2_values = plc_2.read_coils(4, 4)
                time.sleep(0.1)

                # check if still running
                isRunning = plc_2_values[0]
                time.sleep(0.1)

                if not isRunning:
                    break

            # check if still running
            isRunning = plc_2.read_coils(4, 1)[0]
            time.sleep(0.1)

            if not isRunning:
                break

            ####################################
            # 5. Turn off both emittors - TODO # 
            ####################################


            time.sleep(1)

            # turn off both conveyors and turn on both clamps
            # [Lids conveyor 1, Bases conveyor 1, RP1 Clamp, RP2 Clamp]
            plc_4.write_multiple_coils(0, [False, False, True, True])
            time.sleep(0.5)

            # read first two sensors
            # [Right Positioner 1 (Clamped), Right Positioner 2 (Clamped), Part leaving, ---]
            # (4, 2) means that it will read from adress 4, and will read two values
            # so in plc_3_values are values of sensors RP1 (Clamped) and RP2 (Clamped)
            plc_3_values = plc_3.read_coils(4, 2)
            time.sleep(0.1)

            # while sensors didn't detect anything
            while not plc_3_values[0] or not plc_3_values[1]:
                plc_3_values = plc_3.read_coils(4, 2)
                time.sleep(0.1)

                # check if still running
                isRunning = plc_2.read_coils(4, 1)[0]
                time.sleep(0.1)

                if not isRunning:
                    break

            # check if still running
            isRunning = plc_2.read_coils(4, 1)[0]
            time.sleep(0.1)

            if not isRunning:
                break

            ################################################################
            # 6. In this section you have to synchronize the assemly part  #
            # of the line. At first, gripper has to grab the lid, than put #
            # it on top of base. Final product can be moved forward only   #
            # after both parts are assemled.                               # 
            ################################################################

            # Gripper will go down, to grab lid
            # TODO ...
            
            time.sleep(1)

            # Turn ON gripper
            plc_2.write_single_coil(3, True)
            time.sleep(0.5)

            # turn off both conveyors and turn off both clamps
            # [Lids conveyor 1, Bases conveyor 1, RP1 Clamp, RP2 Clamp]
            plc_4.write_multiple_coils(0, [False, False, False, False])
            time.sleep(0.1)

            # Gripper will go up with lid
            # TODO ...
            
            time.sleep(1)

            # Gripper will move to the middle of bases conveyor
            # TODO ...
            
            time.sleep(1)

            # Gripper will go down, to land lid on base
            # TODO ...
            
            time.sleep(1)

            # Turn OFF gripper
            plc_2.write_single_coil(3, False)
            time.sleep(0.5)

            # Gripper will go up
            # TODO ...
            
            time.sleep(1)

            # Gripper will move to the starting position
            # TODO ...
            
            time.sleep(1)


            # Raise RP2 and turn on bases conveyor 1 
            # to move final product to the remover
            # TODO ...

            time.sleep(0.1)

            # TODO ...

            time.sleep(0.5)

            # [RP1 Clamped, RP2 Clamped, Part leaving]
            plc_3_values = plc_3.read_coils(4, 3)
            time.sleep(0.1)

            # while Part leaving sensor didn't detect anything
            while plc_3_values[2]:
                plc_3_values = plc_3.read_coils(4, 3)
                time.sleep(0.1)

                # check if still running
                isRunning = plc_2.read_coils(4, 1)[0]
                time.sleep(0.1)

                if not isRunning:
                    break

            # check if still running
            isRunning = plc_2.read_coils(4, 1)[0]
            time.sleep(0.1)

            if not isRunning:
                break

            # turn off RP2 Raise
            plc_3.write_single_coil(0, False)  # RP2 Raise
            time.sleep(0.1)

            time.sleep(1)

start()
