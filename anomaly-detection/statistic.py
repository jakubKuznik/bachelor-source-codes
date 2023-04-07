# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: statistic.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: . 

import pandas as pd 

class Statistic:
  
  ##
  # Count basic statistic for csv. It relates everything to 5 min interval 
  def __init__(self, df, duration):

    df = self.replaceNil(df) 

    self.duration_sec = duration.total_seconds()
    ## this constant is used to count everything to 5 minut interval 300s 
    five_minutes = 300
    to_five_minutes = five_minutes / self.duration_sec

    self.packets_sum = df['PACKETS'].sum() * to_five_minutes
    self.bytes_sum = df['BYTES'].sum() * to_five_minutes
    self.avg_packet_size = self.bytes_sum / self.packets_sum
    
    self.modbus_packets_sum = df[(df['L4_PORT_SRC'] == 502) | (df['L4_PORT_DST'] == 502)]['PACKETS'].sum() * to_five_minutes
    self.modbus_bytes_sum = df[(df['L4_PORT_SRC'] == 502) | (df['L4_PORT_DST'] == 502)]['BYTES'].sum() * to_five_minutes
    self.avg_modbus_packet_size = self.modbus_bytes_sum / self.modbus_packets_sum
    self.avg_modbus_packet_size = self.modbus_bytes_sum / self.modbus_packets_sum
    self.percent_of_modbus = self.modbus_bytes_sum / self.bytes_sum * 100
    self.avg_packets_per_sec = self.packets_sum / five_minutes 
    self.avg_modbus_packets_per_sec = self.modbus_packets_sum / five_minutes 
    self.avg_bytes_per_sec = self.bytes_sum / five_minutes
    self.avg_modbus_bytes_per_sec = self.modbus_bytes_sum / five_minutes
    self.modbus_read_total = df['MODBUS_READ_REQUESTS'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.modbus_write_total = df['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.modbus_diagnostic_total = df['MODBUS_DIAGNOSTIC_REQUESTS'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.modbus_other_total = df['MODBUS_OTHER_REQUESTS'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.modbus_undefined_total = df['MODBUS_UNDEFINED_REQUESTS'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.modbus_success_total = df['MODBUS_SUCCESS_RESPONSES'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.modbus_error_total = df['MODBUS_ERROR_RESPONSES'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.bytes_250_251 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['BYTES'].sum() * to_five_minutes
    self.bytes_250_252 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['BYTES'].sum() * to_five_minutes
    self.bytes_250_253 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['BYTES'].sum() * to_five_minutes
    self.bytes_250_254 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['BYTES'].sum() * to_five_minutes
    self.packets_250_251 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['PACKETS'].sum() * to_five_minutes
    self.packets_250_252 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['PACKETS'].sum() * to_five_minutes
    self.packets_250_253 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['PACKETS'].sum() * to_five_minutes
    self.packets_250_254 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['PACKETS'].sum() * to_five_minutes
    self.modbus_write_250_251 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.modbus_write_250_252 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.modbus_write_250_253 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.modbus_write_250_254 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.modbus_read_250_251 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['MODBUS_READ_REQUESTS'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.modbus_read_250_252 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['MODBUS_READ_REQUESTS'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.modbus_read_250_253 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['MODBUS_READ_REQUESTS'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.modbus_read_250_254 = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['MODBUS_READ_REQUESTS'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.bytes_250_251_A = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['BYTES_A'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.bytes_251_250_B = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['BYTES_B'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.bytes_250_252_A = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['BYTES_A'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.bytes_252_250_B = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['BYTES_B'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.bytes_250_253_A = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['BYTES_A'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.bytes_253_250_B = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['BYTES_B'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.bytes_250_254_A = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['BYTES_A'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.bytes_254_250_B = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['BYTES_B'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.packets_250_251_A = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['PACKETS_A'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.packets_251_250_B = df[(df['L3_IPV4_SRC'] == '192.168.88.251') & (df['L3_IPV4_DST'] == '192.168.88.250')]['PACKETS_B'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.packets_250_252_A = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['PACKETS_A'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.packets_252_250_B = df[(df['L3_IPV4_SRC'] == '192.168.88.252') & (df['L3_IPV4_DST'] == '192.168.88.250')]['PACKETS_B'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.packets_250_253_A = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['PACKETS_A'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.packets_253_250_B = df[(df['L3_IPV4_SRC'] == '192.168.88.253') & (df['L3_IPV4_DST'] == '192.168.88.250')]['PACKETS_B'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.packets_250_254_A = df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['PACKETS_A'].replace('NIL', '0').astype(int).sum() * to_five_minutes
    self.packets_254_250_B = df[(df['L3_IPV4_SRC'] == '192.168.88.254') & (df['L3_IPV4_DST'] == '192.168.88.250')]['PACKETS_B'].replace('NIL', '0').astype(int).sum() * to_five_minutes

    self.bytes_88_199 = df[(df['L3_IPV4_SRC'] == '192.168.88.199') | (df['L3_IPV4_DST'] == '192.168.88.199')]['BYTES'].sum() * to_five_minutes
    self.bytes_88_200 = df[(df['L3_IPV4_SRC'] == '192.168.88.200') | (df['L3_IPV4_DST'] == '192.168.88.200')]['BYTES'].sum() * to_five_minutes
    
  @staticmethod
  def m1_basic_stats(dfN, dfA):
    print("hihi")
  
  ## replace nils for specific columns in df 
  def replaceNil(self, df):
    change_list = ['BYTES', 'L4_PORT_SRC', 'L4_PORT_DST', 'PACKETS', 'BYTES_A', 'PACKETS_A', 'BYTES_B', 'PACKETS_B',
    'MODBUS_READ_REQUESTS', 'MODBUS_WRITE_REQUESTS', 'MODBUS_DIAGNOSTIC_REQUESTS', 'MODBUS_OTHER_REQUESTS',  
    'MODBUS_UNDEFINED_REQUESTS', 'MODBUS_SUCCESS_RESPONSES', 'MODBUS_ERROR_RESPONSES']

    for node in change_list:
      df[node] = df[node].replace('nil', '0')
      df[node] = df[node].replace('NIL', '0')
      df[node] = df[node].astype(int)
    
    return df

  ## print statistic 
  def printStatistic(self):
    print("STATISTIC: Everything has been averaged into 5-minute intervals.")
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
    print("Number of Modbus Write requests between stations .250 <-> .251: " + str(self.modbus_write_250_251))
    print("Number of Modbus Write requests between stations .250 <-> .252: " + str(self.modbus_write_250_252))
    print("Number of Modbus Write requests between stations .250 <-> .253: " + str(self.modbus_write_250_253))
    print("Number of Modbus Write requests between stations .250 <-> .254: " + str(self.modbus_write_250_254))
    print("Number of Modbus Read requests between stations .250 <-> .251: " + str(self.modbus_read_250_251))
    print("Number of Modbus Read requests between stations .250 <-> .252: " + str(self.modbus_read_250_252))
    print("Number of Modbus Read requests between stations .250 <-> .253: " + str(self.modbus_read_250_253))
    print("Number of Modbus Read requests between stations .250 <-> .254: " + str(self.modbus_read_250_254))
    print("Number of bytes transferred from .250 to .251: " + str(self.bytes_250_251_A))
    print("Number of bytes transferred from .251 to .250: " + str(self.bytes_251_250_B))
    print("Number of bytes transferred from .250 to .252: " + str(self.bytes_250_252_A))
    print("Number of bytes transferred from .252 to .250: " + str(self.bytes_252_250_B))
    print("Number of bytes transferred from .250 to .253: " + str(self.bytes_250_253_A))
    print("Number of bytes transferred from .253 to .250: " + str(self.bytes_253_250_B))
    print("Number of bytes transferred from .250 to .254: " + str(self.bytes_250_254_A))
    print("Number of bytes transferred from .254 to .250: " + str(self.bytes_254_250_B))
    print("Number of packets transferred from .250 to .251: " + str(self.packets_250_251_A))
    print("Number of packets transferred from .251 to .250: " + str(self.packets_251_250_B))
    print("Number of packets transferred from .250 to .252: " + str(self.packets_250_252_A))
    print("Number of packets transferred from .252 to .250: " + str(self.packets_252_250_B))
    print("Number of packets transferred from .250 to .253: " + str(self.packets_250_253_A))
    print("Number of packets transferred from .253 to .250: " + str(self.packets_253_250_B))
    print("Number of packets transferred from .250 to .254: " + str(self.packets_250_254_A))
    print("Number of packets transferred from .254 to .250: " + str(self.packets_254_250_B))
    print("Total number of Modbus Read requests: " + str(self.modbus_read_total))
    print("Total number of Modbus Write requests: " + str(self.modbus_write_total))
    print("Total number of Modbus Diagnostic requests: " + str(self.modbus_diagnostic_total))
    print("Total number of Modbus Other requests: " + str(self.modbus_other_total))
    print("Total number of Modbus Undefined requests: " + str(self.modbus_undefined_total))
    print("Total number of Modbus Success responses: " + str(self.modbus_success_total))
    print("Total number of Modbus Error responses: " + str(self.modbus_error_total))
