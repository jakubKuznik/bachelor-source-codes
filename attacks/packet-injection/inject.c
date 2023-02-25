// Solution for BACHELOR’S THESIS: atack generation on industrial modbus network
// File:        inject.c
// Author:      Jakub Kuzník, FIT
// Program will ... 

#include "inject.h"


int main(void){
  // Modbus TCP packet
  modbusPacket mPacket;
  char packetRawForm[PACKET_SIZE];
  // raw sockete for sending packets
  int rawSocket;  
  pcap_t * sniffInterface = NULL;
  char error_message[PCAP_ERRBUF_SIZE];

  srand(time(NULL)); // rand nums init.

  // this function will create raw socket.
  // if there is an error it will exit() program 
  rawSocket = createRawSocket();

  // open interface for sniffing // exit program if error 
  // global variable in sniff.c
  sniffInterface = openInt(error_message, OUT_INTERFACE);


  // close sniffing interface 
  pcap_close(sniffInterface);
  return 0;

error3:
  //fprintf(stderr, "ERROR send() %d Sending data failed \n", ret);
  return 2;
}

/**
 * @brief Set the Raw Socket object
 * @return socket or exit program  
 */
int createRawSocket(){

  int rawSocket = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
  if (rawSocket < 0){
    fprintf(stderr, "Error can't create raw socket\n");
    exit(1);
  }

  // get index of network interface named "eno2"
  int ifIndex = if_nametoindex(OUT_INTERFACE);
  if (ifIndex == 0) {
    fprintf(stderr, "Can't get network interface index");
    exit(1);
  }

  // bind socket to network interface
  struct sockaddr_ll sa;
  memset(&sa, 0, sizeof(sa));
  sa.sll_family = AF_PACKET;
  sa.sll_protocol = htons(ETH_P_ALL);
  sa.sll_ifindex = ifIndex; 
  if (bind(rawSocket, (struct sockaddr*)&sa, sizeof(sa)) < 0) {
    fprintf(stderr, "Can't bind socket to interface");
    exit(1);
  }

  return rawSocket;
}
