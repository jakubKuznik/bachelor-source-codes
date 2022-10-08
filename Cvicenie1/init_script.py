from pyModbusTCP.client import ModbusClient
import time

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
        # plc_2.write_single_coil(0, False)  # Sorter - right
        # plc_2.write_single_coil(1, False)  # Sorter - left
        # plc_2.write_single_coil(2, False)  # Right emitter
        # plc_2.write_single_coil(3, False)  # Left emitter

        # [Sorter - right, Sorter - left, Right emitter, Left emitter]
        plc_2.write_multiple_coils(0, [False, False, False, False])
        time.sleep(0.1)

    if plc_3.is_open():
        # plc_3.write_single_coil(0, False)  # Sorter - front
        # plc_3.write_single_coil(1, False)  # Factory I/O (Run)
        # plc_3.write_single_coil(2, False)  # Sender - right
        # plc_3.write_single_coil(3, False)  # Sender - left

        # [Sorter - front, Factory I/O (Run), Sender - right, Sender - left]
        plc_3.write_multiple_coils(0, [False, False, False, False])
        time.sleep(0.1)

    if plc_4.is_open():
        # plc_4.write_single_coil(0, False)  # Sender - front
        # plc_4.write_single_coil(1, False)  # Load scale
        # plc_4.write_single_coil(2, False)  # Entry conveyor

        # [Sender - front, Load scale, Entry conveyor, ---]
        plc_4.write_multiple_coils(0, [False, False, False, False])
        time.sleep(0.1)

