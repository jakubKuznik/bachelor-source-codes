# About 
Program sniffs tcp comunication between master and slave. It injects packets
into this communication. Communication we are looking for is defined in header files. 

# Constants
```#define IP\_SRC "192.168.88.250"
#define IP\_DST "192.168.88.252"
#define MAC\_SRC "1c:69:7a:08:86:1a"
#define MAC\_DST "b8:27:eb:1e:08:59"
#define TCP\_DST\_PORT 502
#define OUT\_INTERFACE "eno2"```

# Run 
## 1. set constants above (you should have same ip as master device)
## 2. build
`make`
## 3. execution 
`./inject 10 .... means 10 packets/min` 
`./inject 0  .... means full speed `

