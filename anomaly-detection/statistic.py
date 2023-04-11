# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: statistic.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: File counts statistical data from csv  

import pandas as pd 
import matplotlib.pyplot as plt

## Class hold statistic information about ipfix 
class Statistic:

  # modbus read  ---> 65B 
  # modbus write ---> 64B

  ##
  # Count basic statistic for csv. It relates everything to 5 min interval 
  def __init__(self, df, duration):

    df = self.replaceNil(df) 

    self.duration_sec = duration.total_seconds()
    print("DEBUG duration: " + str(self.duration_sec))
    ## this constant is used to count everything to 5 minut interval 300s 
    five_minutes = 300
    to_five_minutes = five_minutes / self.duration_sec

    self.packets_sum = df['PACKETS'].sum() * to_five_minutes
    self.bytes_sum = df['BYTES'].sum() * to_five_minutes
    self.avg_packet_size = self.bytes_sum / self.packets_sum
    
    self.modbus_packets_sum   = (df[(df['L4_PORT_SRC'] == 502) | (df['L4_PORT_DST'] == 502)]['PACKETS'].sum()) * to_five_minutes
    # packets sigma  
    self.modbus_packets_sigma = self.m_packet_sigma(df, self.modbus_packets_sum) 
    self.modbus_bytes_sum = (df[(df['L4_PORT_SRC'] == 502) | (df['L4_PORT_DST'] == 502)]['BYTES'].sum()) * to_five_minutes
    self.avg_modbus_packet_size = (self.modbus_bytes_sum / self.modbus_packets_sum)
    self.avg_modbus_packet_size = (self.modbus_bytes_sum / self.modbus_packets_sum)
    self.percent_of_modbus = (self.modbus_bytes_sum / self.bytes_sum) * 100
    self.avg_packets_per_sec = (self.packets_sum / five_minutes )
    self.avg_modbus_packets_per_sec = (self.modbus_packets_sum / five_minutes )
    self.avg_bytes_per_sec = (self.bytes_sum / five_minutes)
    self.avg_modbus_bytes_per_sec = (self.modbus_bytes_sum / five_minutes)
    self.modbus_read_total = (df['MODBUS_READ_REQUESTS'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_write_total = (df['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    # sigma write total 
    self.modbus_write_sigma = self.write_sigma(df, self.modbus_write_total)
    self.modbus_diagnostic_total = (df['MODBUS_DIAGNOSTIC_REQUESTS'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_other_total = (df['MODBUS_OTHER_REQUESTS'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_undefined_total = (df['MODBUS_UNDEFINED_REQUESTS'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_succ_total = (df['MODBUS_SUCCESS_RESPONSES'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_error_total = (df['MODBUS_ERROR_RESPONSES'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.bytes_250_251 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['BYTES'].sum()) * to_five_minutes
    self.bytes_250_252 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['BYTES'].sum()) * to_five_minutes
    self.bytes_250_253 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['BYTES'].sum()) * to_five_minutes
    self.bytes_250_254 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['BYTES'].sum()) * to_five_minutes
    self.packets_250_251 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['PACKETS'].sum()) * to_five_minutes
    self.packets_250_252 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['PACKETS'].sum()) * to_five_minutes
    # sigma packets 250 252 
    self.packets_250_252_sigma = self.p_250_252_sigma(df, self.packets_250_252)
    self.packets_250_253 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['PACKETS'].sum()) * to_five_minutes
    self.packets_250_254 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['PACKETS'].sum()) * to_five_minutes
    self.modbus_write_250_251 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_write_250_252 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    # sigma write 250 252  
    self.modbus_write_250_252_sigma = self.m_write_250_252_sigma(df, self.modbus_write_250_252)
    self.modbus_write_250_253 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_write_250_254 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_read_250_251 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['MODBUS_READ_REQUESTS'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_read_250_252 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['MODBUS_READ_REQUESTS'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_read_250_253 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['MODBUS_READ_REQUESTS'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_read_250_254 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['MODBUS_READ_REQUESTS'].replace('NIL', '0').astype(int).sum()) * to_five_minutes

    self.modbus_succ_total_250_251 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['MODBUS_SUCCESS_RESPONSES'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_succ_total_250_252 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['MODBUS_SUCCESS_RESPONSES'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_succ_total_250_253 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['MODBUS_SUCCESS_RESPONSES'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.modbus_succ_total_250_254 = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['MODBUS_SUCCESS_RESPONSES'].replace('NIL', '0').astype(int).sum()) * to_five_minutes

    self.modbus_commands_total     = self.modbus_read_total + self.modbus_write_total
    self.modbus_commands_total_251 = self.modbus_write_250_251 + self.modbus_read_250_251 
    self.modbus_commands_total_252 = self.modbus_write_250_252 + self.modbus_read_250_252 
    self.modbus_commands_total_253 = self.modbus_write_250_253 + self.modbus_read_250_253 
    self.modbus_commands_total_254 = self.modbus_write_250_254 + self.modbus_read_250_254 

    self.bytes_250_251_A = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['BYTES_A'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.bytes_251_250_B = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['BYTES_B'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.bytes_250_252_A = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['BYTES_A'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.bytes_252_250_B = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['BYTES_B'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.bytes_250_253_A = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['BYTES_A'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.bytes_253_250_B = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['BYTES_B'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.bytes_250_254_A = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['BYTES_A'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.bytes_254_250_B = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['BYTES_B'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.packets_250_251_A = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['PACKETS_A'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.packets_250_252_A = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['PACKETS_A'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.packets_250_253_A = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['PACKETS_A'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.packets_250_254_A = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['PACKETS_A'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.packets_250_251_B = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.251')]['PACKETS_B'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.packets_250_252_B = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.252')]['PACKETS_B'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.packets_250_253_B = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.253')]['PACKETS_B'].replace('NIL', '0').astype(int).sum()) * to_five_minutes
    self.packets_250_254_B = (df[(df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == '192.168.88.254')]['PACKETS_B'].replace('NIL', '0').astype(int).sum()) * to_five_minutes

    self.bytes_88_199 = (df[(df['L3_IPV4_SRC'] == '192.168.88.199') | (df['L3_IPV4_DST'] == '192.168.88.199')]['BYTES'].sum()) * to_five_minutes
    self.bytes_88_200 = (df[(df['L3_IPV4_SRC'] == '192.168.88.200') | (df['L3_IPV4_DST'] == '192.168.88.200')]['BYTES'].sum()) * to_five_minutes

    self.df = df

  ## standard deviation 
  #  Σ(xᵢ - μ)² / n
  # for each ipfix: 
  #   a += ((five_minutes / (end_time - start time)) * packets) - mean  
  #   n++
  # a / n 
  def m_packet_sigma(self, df, mean):
    to_five_minutes = 1
    df_filtered = df[(df['L4_PORT_SRC'] == 502) | (df['L4_PORT_DST'] == 502)]
    
    n = 0
    sum = 0
    for index, row in df_filtered.iterrows():
      write_req = row['PACKETS']
      duration  = (pd.to_datetime(row['END_SEC']) - pd.to_datetime(row['START_SEC'])).total_seconds()
      if duration == 0:
        continue
      to_five_minutes = 300 / duration
      value = write_req * to_five_minutes
      sum += (value - mean)*(value - mean)
      n += 1

    sigma = sum / n
    return mean*0.02

  ## standard deviation 
  #  Σ(xᵢ - μ)² / n
  # for each ipfix: 
  #   a += ((five_minutes / (end_time - start time)) * WRITE request) - modbus_write_total  
  #   n++
  # a / n 
  def write_sigma(self, df, mean):
    to_five_minutes = 1
    df_filtered = df[df['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int) >= 1]
    
    n = 0
    sum = 0
    for index, row in df_filtered.iterrows():
      write_req = row['MODBUS_WRITE_REQUESTS']
      duration  = (pd.to_datetime(row['END_SEC']) - pd.to_datetime(row['START_SEC'])).total_seconds()
      to_five_minutes = 300 / duration
      value = write_req * to_five_minutes
      sum += (value - mean)*(value - mean)
      n += 1

    sigma = sum / n
    return mean*0.02

  # standard deviation 
  def p_250_252_sigma(self, df, mean):
    to_five_minutes = 1
    df_filtered = df[(df['L4_PORT_SRC'] == 502) | (df['L4_PORT_DST'] == 502) 
                   & (df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == "192.168.88.252")]
    n = 0
    sum = 0
    for index, row in df_filtered.iterrows():
      write_req = row['PACKETS']
      duration  = (pd.to_datetime(row['END_SEC']) - pd.to_datetime(row['START_SEC'])).total_seconds()
      if duration == 0:
        continue
      to_five_minutes = 300 / duration
      value = write_req * to_five_minutes
      sum += (value - mean)*(value - mean)
      n += 1

    sigma = sum / n
    return mean*0.02
  
  # standard deviation 
  def m_write_250_252_sigma(self, df, mean):
    to_five_minutes = 1
    #  MODBUS_WRITE_REQUESTS
    df_filtered = df[(df['L4_PORT_SRC'] == 502) | (df['L4_PORT_DST'] == 502) 
                   & (df['L3_IPV4_SRC'] == '192.168.88.250') & (df['L3_IPV4_DST'] == "192.168.88.252")
                   & (df['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int) > 0)]
    n = 0
    sum = 0
    for index, row in df_filtered.iterrows():
      modbus_req = row['MODBUS_WRITE_REQUESTS']
      duration  = (pd.to_datetime(row['END_SEC']) - pd.to_datetime(row['START_SEC'])).total_seconds()
      if duration == 0:
        continue
      to_five_minutes = 300 / duration
      value = modbus_req * to_five_minutes
      sum += (value - mean)*(value - mean)
      n += 1

    sigma = sum / n
    return mean*0.02

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
