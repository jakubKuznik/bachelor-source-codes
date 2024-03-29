// Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
// File:        dos.h
// Author:      Jakub Kuzník, FIT
//  

#ifndef DOS_H 
#define DOS_H 

#include "manual-modbus-packet.h"

// normal libraries 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <sys/time.h>
#include <time.h>
#include <signal.h>
#include <unistd.h>

// network libraries
#include <arpa/inet.h>
#include <netinet/if_ether.h> //ethernet and arp frame 
#include <netinet/ip_icmp.h>
#include <netinet/ip6.h>
#include <netinet/if_ether.h>
#include <netinet/ether.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netdb.h>
#include <pcap/pcap.h>
#include <net/if.h>
#include <linux/if_packet.h>
#include <sys/socket.h>

#define OUT_INTERFACE "eno2"

/**
 * @brief Set the Raw Socket object
 * @return socket or exit program  
 */
int createRawSocket();

#endif 
