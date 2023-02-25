// Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
// File:        modbus-packet.h 
// Author:      Jakub Kuzník, FIT
// TODO  

#ifndef SNIFF_H  
#define SNIFF_H

#include "modbus-packet.h"

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

#define ETHERTYP_IP 0x0800
#define ETH_HEAD 14
// this can differ but in our example all packets are having 20B ip header 
#define IP_HEAD 20 
#define TCP 6

/**
 * @brief Sniff until you find tcp stream between:
 *   IP_SRC <---> IP_DST
 * on port: 
 *   TCP_DST_PORT
 */
modbusPacket * findModbusPacket();

/**
 * @brief Create a modbus packet from *frame 
 *   // ALLOCATE ON HEAP 
 * @return modbusPacket* 
 */
modbusPacket * createPacket(const u_char *frame);

/**
 * @brief find packet with: IP_SRC, IP_DST, TCP_DST_PORT 
 * @return true if packet found 
 */
bool findSpecificPakcet(const u_char *frame);

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

