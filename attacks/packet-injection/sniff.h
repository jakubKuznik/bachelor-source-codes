// Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
// File:        modbus-packet.h 
// Author:      Jakub Kuzník, FIT
// TODO  

#ifndef SNIFF_H  
#define SNIFF_H

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

// for pcap_open_live
#define SNIFF_TIMEOUT 10
#define MAX_FRAME_SIZE 1518


/**
 * @brief Sniff until you find tcp stream between:
 *   IP_SRC <---> IP_DST
 * on port: 
 *   TCP_DST_PORT
 */
int findTcpStream();


/**
 * @brief Open interface and set *err as erro message 
 * if open fail exit(2)
 * if interface does not support ethernet frame exit(2) 
 */
pcap_t *openInt(char *err, char *name);

/**
 * @brief Free resource after signal SIGINT  
 */
void freeResources(int sig_num);


#endif

