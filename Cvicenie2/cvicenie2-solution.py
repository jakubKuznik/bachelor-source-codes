from pyModbusTCP.client import ModbusClient
import time
import sys

SERVER_HOST_2 = "192.168.88.252"  # PLC2
SERVER_HOST_3 = "192.168.88.253"  # PLC3
SERVER_HOST_4 = "192.168.88.254"  # PLC4

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


def start():
    if not plc_2.is_open():
        if not plc_2.open():
            print("Unable to connect to " + SERVER_HOST_2 + ":" + str(SERVER_PORT))

    if not plc_3.is_open():
        if not plc_3.open():
            print("Unable to connect to " + SERVER_HOST_3 + ":" + str(SERVER_PORT))

    if not plc_4.is_open():
        if not plc_4.open():
            print("Unable to connect to " + SERVER_HOST_4 + ":" + str(SERVER_PORT))

    if plc_2.is_open():
        plc_2.write_multiple_coils(0, [False, False, False, False])
        time.sleep(0.2)

    if plc_3.is_open():
        plc_3.write_multiple_coils(0, [False, False, False, False])
        time.sleep(0.2)

    if plc_4.is_open():
        plc_4.write_multiple_coils(0, [False, False, False, False])
        time.sleep(0.2)

    if plc_2.is_open() and plc_3.is_open() and plc_4.is_open():
        plc_2.write_single_coil(2, True)  # FACTORY I/O (Run)
        time.sleep(0.5)
        while True:
            isRunning = plc_2.read_coils(4, 1)[0]
            time.sleep(0.1)

            if not isRunning:
                break

            plc_2.write_single_coil(0, True)  # Bases emitter
            plc_2.write_single_coil(1, True)  # Lids emitter
            time.sleep(0.1)

            # [Lids conveyor 1, Bases conveyor 1, RP1 Clamp, RP2 Clamp]
            plc_4.write_multiple_coils(0, [True, True, False, False])
            time.sleep(0.1)

            # [Factory I/O (Running), Lid emitted, Base emitted, ---]
            plc_2_values = plc_2.read_coils(4, 4)
            time.sleep(0.1)

            # While sensors didn't detect anything
            while not plc_2_values[1] or not plc_2_values[2]:
                plc_2_values = plc_2.read_coils(4, 4)
                time.sleep(0.1)
                isRunning = plc_2_values[0]
                time.sleep(0.1)

                if not isRunning:
                    break

            isRunning = plc_2.read_coils(4, 1)[0]
            time.sleep(0.1)

            if not isRunning:
                break

            plc_2.write_single_coil(0, False)  # Bases emitter
            plc_2.write_single_coil(1, False)  # Lids emitter
            time.sleep(1)

            # [Lids conveyor 1, Bases conveyor 1, RP1 Clamp, RP2 Clamp]
            plc_4.write_multiple_coils(0, [False, False, True, True])
            time.sleep(0.5)

            plc_3_values = plc_3.read_coils(4, 2)
            time.sleep(0.1)

            # While sensors didn't detect anything
            while not plc_3_values[0] or not plc_3_values[1]:
                plc_3_values = plc_3.read_coils(4, 2)
                time.sleep(0.1)
                isRunning = plc_2.read_coils(4, 1)[0]
                time.sleep(0.1)

                if not isRunning:
                    break

            isRunning = plc_2.read_coils(4, 1)[0]
            time.sleep(0.1)

            if not isRunning:
                break

            # Gripper will go down, to grab lid
            plc_3.write_single_coil(1, True)
            time.sleep(1)

            # Turn ON gripper
            plc_2.write_single_coil(3, True)
            time.sleep(0.5)

            # [Lids conveyor 1, Bases conveyor 1, RP1 Clamp, RP2 Clamp]
            plc_4.write_multiple_coils(0, [False, False, False, False])
            time.sleep(0.1)

            # Gripper will go up with lid
            plc_3.write_single_coil(1, False)
            time.sleep(1)

            # Gripper will move to the middle of bases conveyor
            plc_3.write_single_coil(2, True)
            time.sleep(1)

            # Gripper will go down, to land lid on base
            plc_3.write_single_coil(1, True)
            time.sleep(1)

            # Turn OFF gripper
            plc_2.write_single_coil(3, False)
            time.sleep(0.5)

            # Gripper will go up
            plc_3.write_single_coil(1, False)
            time.sleep(1)

            # Gripper will move to the starting position
            plc_3.write_single_coil(2, False)
            time.sleep(1)

            plc_3.write_single_coil(0, True)  # RP2 Raise
            time.sleep(0.1)

            plc_4.write_single_coil(1, True)  # Bases conveyor 1
            time.sleep(0.5)

            # [RP1 Clamped, RP2 Clamped, Part leaving]
            plc_3_values = plc_3.read_coils(4, 3)
            time.sleep(0.1)

            # While Part leaving sensor didn't detect anything
            while plc_3_values[2]:
                plc_3_values = plc_3.read_coils(4, 3)
                time.sleep(0.1)

                isRunning = plc_2.read_coils(4, 1)[0]
                time.sleep(0.1)

                if not isRunning:
                    break

            isRunning = plc_2.read_coils(4, 1)[0]
            time.sleep(0.1)

            if not isRunning:
                break

            plc_3.write_single_coil(0, False)  # RP2 Raise
            time.sleep(0.1)

            time.sleep(1)

start()
