# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: anomaly-detection.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: . 

#### FIELDS
# EXPORT_COUNTER, ZERO, ONE, CRC, FLOWMON_STARTUP_TIME_SEC, FLOWMON_STARTUP_TIME_MSEC, 
# FLOWMON_STARTUP_TIME_USEC, FLOWMON_STARTUP_TIME_NSEC, BYTES, PACKETS, START_SEC, 
# START_MSEC, START_USEC, START_NSEC, END_SEC, END_MSEC, END_USEC, END_NSEC, 
# INPUT_INTERFACE, QUEUE_ID, FLAG_FLUSH, L3_PROTO, L4_PROTO, BYTES_A, PACKETS_A,
# START_SEC_A, START_MSEC_A, START_USEC_A, START_NSEC_A, END_SEC_A, END_MSEC_A,
# END_USEC_A, END_NSEC_A, BYTES_B, PACKETS_B, START_SEC_B, START_MSEC_B, START_USEC_B,
# START_NSEC_B, END_SEC_B, END_MSEC_B, END_USEC_B, END_NSEC_B, L3_IPV4_SRC, 
# L3_IPV4_DST, L3_IPV6_SRC, L3_IPV6_DST, L4_TCP_FLAGS, L4_TCP_FLAGS_A, L4_TCP_FLAGS_B,
# L4_PORT_SRC, L4_PORT_DST, L4_ICMP_TYPE_CODE, FLAG_MISC, SAMPLING_RATE, 
# SAMPLING_ALGORITHM, MODBUS_UNIT_ID, MODBUS_READ_REQUESTS, MODBUS_WRITE_REQUESTS, 
# MODBUS_DIAGNOSTIC_REQUESTS, MODBUS_OTHER_REQUESTS, MODBUS_UNDEFINED_REQUESTS, 
# MODBUS_SUCCESS_RESPONSES, MODBUS_ERROR_RESPONSES

#### FIELDS EXAMPLE VALUES 
# 0, 0,1,17692676090205341778,2023-03-30 21:19:42.850106102,
# 2023-03-30 21:19:42.850106102,2023-03-30 21:19:42.850106102,
# 2023-03-30 21:19:42.850106102,3208,24,2023-03-30 21:19:43.127968463,
# 2023-03-30 21:19:43.127968463,2023-03-30 21:19:43.127968463,
# 2023-03-30 21:19:43.127968463,2023-03-30 21:19:56.990361901,
# 2023-03-30 21:19:56.990361901,2023-03-30 21:19:56.990361901,
# 2023-03-30 21:19:56.990361901,0,0,5,4,6,2592,17,
# 2023-03-30 21:19:43.127968463,2023-03-30 21:19:43.127968463,
# 2023-03-30 21:19:43.127968463,2023-03-30 21:19:43.127968463,
# 2023-03-30 21:19:56.990361901,2023-03-30 21:19:56.990361901,
# 2023-03-30 21:19:56.990361901,2023-03-30 21:19:56.990361901,
# 616,7,2023-03-30 21:19:43.209812368,2023-03-30 21:19:43.209812368,
# 2023-03-30 21:19:43.209812368,2023-03-30 21:19:43.209812368,
# 2023-03-30 21:19:56.825828077,2023-03-30 21:19:56.825828077,
# 2023-03-30 21:19:56.825828077,2023-03-30 21:19:56.825828077,
# 192.168.88.252,192.168.88.250,NIL,NIL,---AP---,---AP---,---AP---,
# 22,57708,NIL,897,0,0,NIL,NIL,NIL,NIL,NIL,NIL,NIL,NIL

import pandas as pd 

class Csv_procesor:
    
    # Constructor - It parse all csvn files to one self.csvn
    #               It parse all csva files to one self.csva
    #  @csvn list with normal comunication csv files 
    #  @csva list with malicious comunication csv files 
    def __init__(self, csvn, csva):
        # [(DataFrame, duration), (DataFrame, duration) ... (DataFrame, duration)]
        self.csva = []
        self.csvn = []

        ## parse multiple csva files 
        for csv in csva:
            self.csva.append(self.parse_csv(csv))
        
        ## parse multiple csva files 
        for csv in csvn:
            self.csvn.append(self.parse_csv(csv))
        
        print("DEBUG: CSV parsed succesfully")

    ## 
    # @csv list with csv files 
    # @return [csv, time-begin, time-end] 
    def parse_csv(self, csv_file):
        begin_time = ""
        end_time = ""

        # convert csv to pandas dataFrame 
        df = pd.read_csv(csv_file, delimiter=',')

        # delete spaces in row names 
        df = df.rename(columns=lambda x: x.replace(' ', ''))

        end_time     = pd.to_datetime(df.iloc[-1]["END_SEC"])
        begin_time   = pd.to_datetime(df.iloc[0]["START_SEC"])

        duration     = end_time - begin_time

        return (df,duration)

                 