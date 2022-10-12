#!/bin/bash

# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: tcp-server.sh 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: start tcp server on each unipi plc (listen on 0.0.0.0:502)
#   uses: /opt/unipi/tools/unipi_tcp_server 


# For pernament change of tcp server settings change /etc/default/unipi-modbus-tools and systemctl restart unipitcp


# all plcs separated by ';'
PLC=( "192.168.88.252" "192.168.88.253" "192.168.88.254" )
#PLC="192.168.88.252;192.168.88.253;192.168.88.252"  

for ip in "${PLC[@]}"; do
  #todo modify /etc/default/unipi-modbus 
  echo "Starting tcp server on: $ip"
  # todo generate ssh keys between machines 
  ssh unipi@$ip 'echo "DAEMON OPTS=--listen=0.0.0.0" | sudo tee -a /etc/default/unipi-modbus-tools > /dev/null' 
  ssh unipi@$ip 'sudo systemctl restart unipitcp'
done
