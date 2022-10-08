#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authors:  Maria Masarova <xmasar13>
#           Jan Pristas <xprist06>

from pyModbusTCP.client import ModbusClient
from datetime import datetime
import time
import logging
import threading


class ProductionLine:
    def __init__(self):
        self.stop_running = False

        self.SERVER_HOST_2 = "192.168.88.252"  # PLC2
        self.SERVER_HOST_3 = "192.168.88.253"  # PLC3
        self.SERVER_HOST_4 = "192.168.88.254"  # PLC4

        self.SERVER_PORT = 502

        self.LOGGING = True
        self.ON = True
        self.OFF = False

        self.plc_2 = ModbusClient()
        self.plc_3 = ModbusClient()
        self.plc_4 = ModbusClient()

        # define modbus server host, port
        self.plc_2.host(self.SERVER_HOST_2)
        self.plc_2.port(self.SERVER_PORT)

        self.plc_3.host(self.SERVER_HOST_3)
        self.plc_3.port(self.SERVER_PORT)

        self.plc_4.host(self.SERVER_HOST_4)
        self.plc_4.port(self.SERVER_PORT)

        if not self.plc_2.is_open():
            if not self.plc_2.open():
                logging.error("Unable to connect to " + self.SERVER_HOST_2 + ":" + str(self.SERVER_PORT))

        if not self.plc_3.is_open():
            if not self.plc_3.open():
                logging.error("Unable to connect to " + self.SERVER_HOST_3 + ":" + str(self.SERVER_PORT))

        if not self.plc_4.is_open():
            if not self.plc_4.open():
                logging.error("Unable to connect to " + self.SERVER_HOST_4 + ":" + str(self.SERVER_PORT))

        self.counter_left = 0
        self.counter_right = 0
        self.counter_forward = 0

        self.input_register_zero = [0,0,0,0,0,0,0,0]
        self.Vref = 0
        self.VrefInt = 1
        self.weight = 0.00

        ###########################
        #       SENSORS
        ###########################
        self.state_sent_from_left = False  # S1
        self.state_sent_from_right = False  # S2
        self.state_at_scale_entry = False  # S3
        self.state_at_scale = False  # S4
        self.state_at_scale_exit = False  # S5
        self.state_at_left_entry = False  # S6
        self.state_at_left_exit = False  # S7
        self.state_at_forward_entry = False  # S8
        self.state_at_forward_exit = False  # S9
        self.state_at_right_entry = False  # S10
        self.state_at_right_exit = False  # S11

        ###########################
        #       ACTUATORS
        ###########################
        self.state_running = False  # PLC3 - coil 0

        self.state_left_emitter = False  # PLC2 - coil 3
        self.state_right_emitter = False  # PLC2 - coil 2
        self.state_front_left_conveyor = True  # always True, doesn't have pin
        self.state_front_right_conveyor = True  # always True, doesn't have pin

        self.state_sender_left = False  # PLC3 - coil 3
        self.state_sender_right = False  # PLC3 - coil 2
        self.state_sender_front = False  # PLC4 - coil 0

        self.state_entry_conveyor = False  # PLC4 - coil 2
        self.state_load_scale = False  # PLC4 - coil 1

        self.state_sorter_left = False  # PLC2 - coil 1
        self.state_sorter_right = False  # PLC2 - coil 0
        self.state_sorter_front = False  # PLC3 - coil 0

        self.state_left_conveyor = True  # always True, doesn't have pin
        self.state_left_remover = True  # always True, doesn't have pin
        self.state_front_conveyor = True  # always True, doesn't have pin
        self.state_front_remover = True  # always True, doesn't have pin
        self.state_right_conveyor = True  # always True, doesn't have pin
        self.state_right_remover = True  # always True, doesn't have pin

        self.USE_BOTH_EMITTORS = False
        self.USE_LEFT_EMITTOR = False
        self.USE_RIGHT_EMITTOR = True

        self.plc_2_values = [False, False, False, False]
        self.plc_3_values = [False, False, False, False]
        self.plc_4_values = [False, False, False, False]

    def run_threads(self):
        plcs_thread = threading.Thread(target=self.plc_checkers)
        sender_thread = threading.Thread(target=self.sender_checking)
        weighting_thread = threading.Thread(target=self.weighting_checking)
        conveyor_thread = threading.Thread(target=self.conveyor_checking)
        sorter_thread = threading.Thread(target=self.sorter_checking)
        entry_thread = threading.Thread(target=self.entry_checking)
        exit_thread = threading.Thread(target=self.exit_checking)

        plcs_thread.start()
        sender_thread.start()
        weighting_thread.start()
        conveyor_thread.start()
        sorter_thread.start()
        entry_thread.start()
        exit_thread.start()

    def init_variables(self):
        self.counter_left = 0
        self.counter_right = 0
        self.counter_forward = 0

        self.input_register_zero = [0,0,0,0,0,0,0,0]
        self.Vref = 0
        self.VrefInt = 1
        self.weight = 0.00

        self.state_sent_from_left = False  # S1
        self.state_sent_from_right = False  # S2
        self.state_at_scale_entry = False  # S3
        self.state_at_scale = False  # S4
        self.state_at_scale_exit = False  # S5
        self.state_at_left_entry = False  # S6
        self.state_at_left_exit = False  # S7
        self.state_at_forward_entry = False  # S8
        self.state_at_forward_exit = False  # S9
        self.state_at_right_entry = False  # S10
        self.state_at_right_exit = False  # S11

        self.state_running = False  # PLC3 - coil 0
        self.state_left_emitter = False  # PLC2 - coil 3
        self.state_right_emitter = False  # PLC2 - coil 2
        self.state_front_left_conveyor = True  # always True, doesn't have pin
        self.state_front_right_conveyor = True  # always True, doesn't have pin
        self.state_sender_left = False  # PLC3 - coil 3
        self.state_sender_right = False  # PLC3 - coil 2
        self.state_sender_front = False  # PLC4 - coil 0
        self.state_entry_conveyor = False  # PLC4 - coil 2
        self.state_load_scale = False  # PLC4 - coil 1
        self.state_sorter_left = False  # PLC2 - coil 1
        self.state_sorter_right = False  # PLC2 - coil 0
        self.state_sorter_front = False  # PLC3 - coil 0
        self.state_left_conveyor = True  # always True, doesn't have pin
        self.state_left_remover = True  # always True, doesn't have pin
        self.state_front_conveyor = True  # always True, doesn't have pin
        self.state_front_remover = True  # always True, doesn't have pin
        self.state_right_conveyor = True  # always True, doesn't have pin
        self.state_right_remover = True  # always True, doesn't have pin

        self.USE_BOTH_EMITTORS = False
        self.USE_LEFT_EMITTOR = False
        self.USE_RIGHT_EMITTOR = True

        self.plc_2_values = [False, False, False, False]
        self.plc_3_values = [False, False, False, False]
        self.plc_4_values = [False, False, False, False]

    def turn_off_factory(self):
        self.plc_3.write_single_coil(1, self.OFF)
        self.state_running = False
        time.sleep(0.2)

    def turning_on_off_left_emitter(self, on_off):
        self.state_left_emitter = on_off

    def turning_on_off_right_emitter(self, on_off):
        self.state_right_emitter = on_off

    def turning_on_off_entry_conveyor(self, on_off):
        self.state_entry_conveyor = on_off

    def turning_on_off_load_scale(self, on_off):
        self.state_load_scale = on_off

    def start(self):
        self.state_running = True
        self.state_sender_front = True

    def plc_checkers(self):
        input_register_thousand = self.plc_2.read_input_registers(1000, 10)
        input_register_zero = self.plc_2.read_input_registers(0, 8)
        time.sleep(0.2)
        self.Vref = input_register_thousand[9]
        self.VrefInt = input_register_zero[5]

        while True:
            if self.stop_running:
                self.turn_off_factory()
                return

            self.plc_2_values = self.plc_2.read_coils(4, 4)
            self.plc_3_values = self.plc_3.read_coils(4, 4)
            self.plc_4_values = self.plc_4.read_coils(4, 4)
            time.sleep(0.125)

            self.state_at_scale = self.plc_2_values[1]
            if self.state_at_scale and not self.state_load_scale:
                self.input_register_zero = self.plc_2.read_input_registers(0, 8)

            # [Sorter - right, Sorter - left, Right emitter, Left emitter]
            self.plc_2.write_multiple_coils(0, [self.state_sorter_right, self.state_sorter_left, self.state_right_emitter, self.state_left_emitter])
            time.sleep(0.125)

            # [Sorter - front, Factory I/O (Run), Sender - right, Sender - left]
            self.plc_3.write_multiple_coils(0, [self.state_sorter_front, self.state_running, self.state_sender_right, self.state_sender_left])
            time.sleep(0.125)

            # [Sender - front, Load scale, Entry conveyor, ---]
            self.plc_4.write_multiple_coils(0, [self.state_sender_front, self.state_load_scale, self.state_entry_conveyor, False])
            time.sleep(0.125)

    def sender_checking(self):
        while True:
            if self.stop_running:
                return

            sent_from = self.plc_4_values if self.plc_4_values is not None else [False, False, False, False]
            sent_from_left = sent_from[2]
            sent_from_right = sent_from[3]

            if sent_from_left:
                self.state_sent_from_left = True
            else:
                self.state_sent_from_left = False

            if sent_from_right:
                self.state_sent_from_right = True
            else:
                self.state_sent_from_right = False

            if self.state_sent_from_right or self.state_sent_from_left:
                # self.state_sender_front = False
                self.state_sender_right = False
                self.state_sender_left = False
                time.sleep(0.25)
                # self.state_sender_front = True

                if self.state_sent_from_left:
                    self.state_sender_right = True
                else:
                    self.state_sender_left = True

                self.state_entry_conveyor = True
                time.sleep(1)
            time.sleep(0.1)

    def conveyor_checking(self):
        while True:
            if self.stop_running:
                return

            at_scale_entry = self.plc_2_values if self.plc_2_values is not None else [True, False, False, False]
            if not at_scale_entry[0]:
                self.state_at_scale_entry = True
            else:
                self.state_at_scale_entry = False

            if self.state_at_scale_entry:
                self.state_load_scale = True
                # self.state_sender_front = False
                # self.state_sender_right = False
                # self.state_sender_left = False
                time.sleep(0.5)

                self.state_entry_conveyor = False

            time.sleep(0.1)

    def weighting_checking(self):
        while True:
            if self.stop_running:
                return

            at_scale = self.plc_2_values if self.plc_2_values is not None else [False, False, False, False]
            if at_scale[1]:
                self.state_at_scale = True
            else:
                self.state_at_scale = False

            if self.state_at_scale:
                self.state_load_scale = False
                time.sleep(1.5)

                VAI = self.input_register_zero[3]  # weight in volts
                self.weight = (3.3 * (self.Vref / self.VrefInt)) * 3 * (VAI / 4096) * 4

                time.sleep(0.2)
                self.state_load_scale = True
                time.sleep(1)

            time.sleep(0.1)

    def sorter_checking(self):
        while True:
            if self.stop_running:
                return

            at_scale = self.plc_2_values if self.plc_2_values is not None else [False, False, False, False]
            if at_scale[2]:
                self.state_at_scale_exit = True
            else:
                self.state_at_scale_exit = False

            if self.state_at_scale_exit:
                self.state_entry_conveyor = True
                if self.weight < 5:
                    self.state_sorter_left = True
                    self.state_sorter_front = True
                    self.counter_left += 1
                elif self.weight > 10:
                    self.state_sorter_right = True
                    self.state_sorter_front = True
                    self.counter_right += 1
                else:
                    self.state_sorter_front = True
                    self.counter_forward += 1
                time.sleep(1.2)

            time.sleep(0.1)

    def entry_checking(self):
        while True:
            if self.stop_running:
                return

            entries = self.plc_3_values if self.plc_3_values is not None else [False, False, False, False]
            at_left_entry = entries[0]
            at_forward_entry = entries[1]
            at_right_entry = entries[2]

            if at_left_entry:
                self.state_at_left_entry = True
            else:
                self.state_at_left_entry = False

            if at_forward_entry:
                self.state_at_forward_entry = True
            else:
                self.state_at_forward_entry = False

            if at_right_entry:
                self.state_at_right_entry = True
            else:
                self.state_at_right_entry = False

            if self.state_at_left_entry or self.state_at_forward_entry or self.state_at_right_entry:
                self.state_sorter_front = False

                if self.state_at_left_entry:
                    self.state_sorter_left = False
                if self.state_at_right_entry:
                    self.state_sorter_right = False

                time.sleep(1)
            time.sleep(0.1)

    def exit_checking(self):
        while True:
            if self.stop_running:
                return

            entries = self.plc_3_values if self.plc_3_values is not None else [True, True, True, True]
            exits = self.plc_4_values if self.plc_4_values is not None else [True, True, True, True]
            at_left_exit = entries[3]
            at_forward_exit = exits[0]
            at_right_exit = exits[1]

            if not at_left_exit:
                self.state_at_left_exit = True
                time.sleep(0.5)
            else:
                self.state_at_left_exit = False

            if not at_forward_exit:
                self.state_at_forward_exit = True
                time.sleep(0.5)
            else:
                self.state_at_forward_exit = False

            if not at_right_exit:
                self.state_at_right_exit = True
                time.sleep(0.5)
            else:
                self.state_at_right_exit = False

            time.sleep(0.1)

