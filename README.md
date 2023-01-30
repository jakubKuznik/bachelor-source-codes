# bachelor-source-codes

## Run program  
### 1. Setup PLCs 
### 2. Start Factory I/0 
### 3. Connect to PLCs via Factory I/0
### 4. Configure ip
`sudo ip add add 192.168.88.199/24 dev eno2`
`sudo ip route add 192.168.88.0/24 dev eno2`
### 5a. Run automatic warehouse  
python3 factory-solution/warehouse.py
### 5b. Run automatic warehouse  
python3 factory-solution/assembly.py
`
