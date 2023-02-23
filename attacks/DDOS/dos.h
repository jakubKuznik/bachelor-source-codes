// Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
// File:        dos.h
// Author:      Jakub Kuzník, FIT
//  

#ifndef FLOW_H 
#define FLOW_H

// normal libraries 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <sys/time.h>
#include <time.h>
#include <signal.h>

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

#define IP_SRC "192.168.88.250"
#define IP_DST "192.168.88.252"
#define MAC_SRC "1c:69:7a:08:86:1a"
#define MAC_DST "b8:27:eb:1e:08:59"

#define IP_HEADER_TOTAL_LENGHT 54

struct modbusHeader { 
  uint16_t transactionId;
  uint16_t protocolId;
  uint16_t lenght;     
  uint8_t unitId;      
};
typedef struct modbusHeader modbusHeader;

struct modbusPayload {
  uint8_t functionCode; 
  char * data;
};
typedef struct modbusPayload modbusPayload;


struct modbusPacket {
  struct ether_header ethHeader;
  struct iphdr ipHeader; 
  struct tcphdr tcpHeader;  
  modbusHeader nfheader;
  modbusPayload nfpayload;
};
typedef struct modbusPacket modbusPacket;

/**
 * @brief Function create modbus packet.
 * it uses constants from dos.h to fill eth/ip/tcp headers.
 */
void buildModbusPacket(modbusPacket mPacket);

/**
 * @brief it builds ipv4 header using. constants from dos.h 
 */
void createIpHeader(struct iphdr * ipHeader);

/**
 * @brief it builds ethernet header using. constants from dos.h 
 */
void createEthHeader(struct ether_header * ethHeader);

/**
 * @brief it converts mac address from const char "aa:aa:bb:bb:cc:cc"
 *  to unsigned char out[6] 
 */
void convertMac(unsigned char out[6], const char * macStr);

#endif 
