# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: statistic.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: . 

import pandas as pd 
import csv_procesor

class Statistic:
  
  ##
  # Count basic statistic for csv. It relates everything to 5 min interval 
  # @csvc is in format: 
  #  [(DataFrame, duration), (DataFrame, duration) ... (DataFrame, duration)]
  def __init__(self, df, duration):
    print("tu")


    # assuming your DataFrame is called "df"
    # Celkový počet přenesených paketů (PACKETS sum)
    # packets_sum = df['PACKETS'].sum()

    # # Celkový počet přenesených bajtů  (BYTES sum)
    # bytes_sum = df['BYTES'].sum()

    # # Průměrná velikost paketů
    # avg_packet_size = bytes_sum / packets_sum

    # # Celkový počet přenesených paketů Modbus TCP (if L4_SRC or L4 dst is 502)
    # modbus_packets_sum = df[(df['L4_PORT_SRC'] == 502) | (df['L4_PORT_DST'] == 502)]['PACKETS'].sum()

    # # Celkový počet přenesených bajtů Modbus TCP  (if L4_SRC or L4 dst is 502)
    # modbus_bytes_sum = df[(df['L4_PORT_SRC'] == 502) | (df['L4_PORT_DST'] == 502)]['BYTES'].sum()

    # # Průměrná velikost paketu Modbus TCP
    # if modbus_packets_sum > 0:
      # avg_modbus_packet_size = modbus_bytes_sum / modbus_packets_sum
    # else:
      # avg_modbus_packet_size = 0

    # self.csv_processor = csv_processor    
    # self.total_packet_transimted = csv_processor
            ## todo begin time 
            ## todo end time 
            
            # Celkový počet přenesených paketů 
            # Celkový počet přenesených bajtů  
            # Prmůěrná velikost paketů & 61,22B 
            # Celkový počet přenesených paketů Modbus TCP 
            # Celkový počet přenesených bajtů Modbus TCP 
            # Průměrná velikost paketu Modbus TCP 
            # Medián délky trvání IPFIX záznamu 
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
