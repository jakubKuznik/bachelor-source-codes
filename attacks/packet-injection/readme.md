# About 
Program sniffs tcp comunication between master and slave. It injects packets
into this communication. Communication we are looking for is defined in header files. 

# Run 
## 1. set constants (you should act as a master device)
`#define IP_SRC "192.168.88.250"`\
`#define IP_DST "192.168.88.252"` \
`#define MAC_SRC "1c:69:7a:08:86:1a"`\
`#define MAC_DST "b8:27:eb:1e:08:59"`\
`#define TCP_DST_PORT 502`\
`#define OUT_INTERFACE "eno2"`
## 2. build
`make`
## 3. execution 
`./inject 10 .... means 10 packets/min` \
`./inject 0  .... means full speed `

