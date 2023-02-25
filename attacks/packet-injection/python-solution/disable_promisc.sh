sudo ifconfig eno2 -promisc

sudo sysctl -w net.ipv4.conf.eno2.arp_ignore=1
sudo sysctl -w net.ipv4.conf.eno2.arp_announce=2
sudo ifconfig eno2 -multicast


sudo ip link set dev eno2 addr 1c:69:7a:08:86:1a




