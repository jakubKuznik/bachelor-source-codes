# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: statistic.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: . 

import pandas as pd 
import csv_procesor
import datetime

class Statistic:
  
  ##
  # Count basic statistic for csv. It relates everything to 5 min interval 
  # @csvc is in format: 
  #  [(DataFrame, duration), (DataFrame, duration) ... (DataFrame, duration)]
  def __init__(self, df, duration):

    self.duration_sec = duration.total_seconds()
    ## constant so we count everything to 5 min interval 

    print("tu")
    print(df, duration)
    print(self.duration_sec)

    ## todo 
    # al1 - al10 master: 200
    # wh1 - wh10 master: 250  

    self.packets_sum = df['PACKETS'].sum()
    self.bytes_sum = df['BYTES'].sum()
    self.avg_packet_size = self.bytes_sum / self.packets_sum
    self.modbus_packets_sum = df[(df['L4_PORT_SRC'] == 502) | (df['L4_PORT_DST'] == 502)]['PACKETS'].sum()
    self.modbus_bytes_sum = df[(df['L4_PORT_SRC'] == 502) | (df['L4_PORT_DST'] == 502)]['BYTES'].sum()
    self.avg_modbus_packet_size = self.modbus_bytes_sum / self.modbus_packets_sum
    self.avg_modbus_packet_size = self.modbus_bytes_sum / self.modbus_packets_sum
    self.percent_of_modbus = self.modbus_bytes_sum / self.bytes_sum * 100
    self.avg_packets_per_sec = self.packets_sum / self.duration_sec
    self.avg_modbus_packets_per_sec = self.modbus_packets_sum / self.duration_sec 
    self.avg_bytes_per_sec = self.bytes_sum / self.duration_sec
    self.avg_modbus_bytes_per_sec = self.modbus_bytes_sum / self.duration_sec
    self.bytes_250_251 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['BYTES'].sum()
    self.bytes_250_252 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['BYTES'].sum()
    self.bytes_250_253 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['BYTES'].sum()
    self.bytes_250_254 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['BYTES'].sum()
    self.packets_250_251 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['PACKETS'].sum()
    self.packets_250_252 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['PACKETS'].sum()
    self.packets_250_253 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['PACKETS'].sum()
    self.packets_250_254 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['PACKETS'].sum()

    self.bytes_88_199 = df[(df['L3_IPV4_SRC'] == '192.168.88.199') | (df['L3_IPV4_DST'] == '192.168.88.199')]['BYTES'].sum()
    self.bytes_88_200 = df[(df['L3_IPV4_SRC'] == '192.168.88.200') | (df['L3_IPV4_DST'] == '192.168.88.200')]['BYTES'].sum()


    print("Total bytes sent or received by 192.168.88.199: " + str(self.bytes_88_199))
    print("Total bytes sent or received by 192.168.88.200: " + str(self.bytes_88_200))   
    print("packet sum: "+ str(self.packets_sum))
    print("byte sum: "+ str(self.bytes_sum))
    print("average packet size: "+ str(self.avg_packet_size))
    print("Modbus packet sum: "+ str(self.modbus_packets_sum))
    print("Modbus byte sum: "+ str(self.modbus_bytes_sum))
    print("average Modbus packet size: "+ str(self.avg_modbus_packet_size))
    print("percent of Modbus: "+ str(self.percent_of_modbus))
    print("average packets per second: "+ str(self.avg_packets_per_sec))
    print("average Modbus packets per second: "+ str(self.avg_modbus_packets_per_sec))
    print("average bytes per second: "+ str(self.avg_bytes_per_sec))
    print("average Modbus bytes per second: "+ str(self.avg_modbus_bytes_per_sec))
    print("Number of bytes transferred between stations .250 <-> .251: " + str(self.bytes_250_251))
    print("Number of bytes transferred between stations .250 <-> .252: " + str(self.bytes_250_252))
    print("Number of bytes transferred between stations .250 <-> .253: " + str(self.bytes_250_253))
    print("Number of bytes transferred between stations .250 <-> .254: " + str(self.bytes_250_254))
    print("Number of packets transferred between stations .250 <-> .251: " + str(self.packets_250_251))
    print("Number of packets transferred between stations .250 <-> .252: " + str(self.packets_250_252))
    print("Number of packets transferred between stations .250 <-> .253: " + str(self.packets_250_253))
    print("Number of packets transferred between stations .250 <-> .254: " + str(self.packets_250_254))

    # todo .200 -> 250 there may be problem with data 


# Print the results

    # self.csv_processor = csv_processor    
    # self.total_packet_transimted = csv_processor
            ## todo begin time 
            ## todo end time 
            
            # Celkové procento síťové komunikace tvořené pakety Modbus TCP 
            # Průměrný počet přenesených paketů za sekundu 
            # Průměrný počet přenesených paketů Modbus TCP za sekundu 
            # Průměrný počet přenesených bajtů za sekundu 
            # Průměrný počet přenesených bajtů protokolu Modbus TCP za sekundu 
            # Počet přenesených bajtů mezi stanicemi .250 \textless-> .251 
            # Počet přenesených bajtů mezi stanicemi .250 \textless-> .252 
            # Počet přenesených bajtů mezi stanicemi .250 \textless-> .253 
            # Počet přenesených bajtů mezi stanicemi .250 \textless-> .254 
            # Počet přenesených paketů mezi stanicemi .250 \textless-> .251 
            # Počet přenesených paketů mezi stanicemi .250 \textless-> .252 
            # Počet přenesených paketů mezi stanicemi .250 \textless-> .253 
            # Počet přenesených paketů mezi stanicemi .250 \textless-> .254 
            # Počet Modbus Read/Write dotazů mezi stanicemi .250 \textless-> .251 
            # Počet Modbus Read/Write dotazů mezi stanicemi .250 \textless-> .252 
            # Počet Modbus Read/Write dotazů mezi stanicemi .250 \textless-> .253 
            # Počet Modbus Read/Write dotazů mezi stanicemi .250 \textless-> .254 
            # Celkový Počet Modbus Read dotazů 
            # Celkový Počet Modbus Write dotazů  
            # Celkový Počet Modbus Diagnostických dotazů 
            # Celkový Počet Modbus úspěšných odpovědí 
            # Celkový Počet Modbus neúspěšných odpovědí 
            # Celkový Počet Modbus dotazů jiného typu 
