# About
The program sends Modbus packets via raw socket as fast as possible. TCP seq and ack numbers are made up so the slave device will find out that packets are not valid, but PLC devices are not powerful enough to filter 1Gb/s of 60B packets traffic.

# Run
## 1. customize parameters
There are constants values in headers such as src-ip, dst-ip, interface ...   
## 2. build
`make` 
## run
program needs sudo for creating raw socket. 
`sudo ./dos`


