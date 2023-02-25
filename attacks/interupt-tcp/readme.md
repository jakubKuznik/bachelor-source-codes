# About
If we have the same IP address as the master device and we will try to establish a new TCP connection it kills the existing one.

# Run  
## 1. Set master ip addres on your interface
`sudo ip add add 192.168.88.250/24 dev eno2` 
## 4. Run the attacking script
`python3 interupt-tcp.py`


