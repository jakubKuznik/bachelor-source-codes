// Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
// File:        sniff.c 
// Author:      Jakub Kuzník, FIT
// TODO  

#include "sniff.h"

// SIGINT signal handler
struct sigaction sigIntHandler;  
// interface where tcp streams will be sniffed
pcap_t * sniffInterface;

/**
 * @brief Sniff until you find tcp stream between:
 *   IP_SRC <---> IP_DST
 * on port: 
 *   TCP_DST_PORT
 */
modbusPacket * findModbusPacket(){
  const u_char        *frame;      // packet
  struct pcap_pkthdr  pacHeader;   // packet header
  
  // this here prevents to sniif our own malicious packet
  for (int i = 0; i < 20; i++){
    pcap_next(sniffInterface, &pacHeader); // skip one 
  } 

  // find packet with IP_SRC, IP_DST, TCP_DST_PORT
  while ((frame = pcap_next(sniffInterface, &pacHeader)) != NULL){
    if (findSpecificPakcet(frame) == true)
      break;
  }

  return createPacket(frame);
}

/**
 * @brief Create a modbus packet from *frame 
 *   // ALLOCATE ON HEAP 
 * @return modbusPacket* 
 */
modbusPacket * createPacket(const u_char *frame){
    modbusPacket * mPacket = malloc(120);
    if (mPacket == NULL){
        fprintf(stderr, "Malloc error\n");
        exit(1);
    }

    char *pt = &frame[0]; // pointer to the first element of an array 

    // can be optimalized here 
    // eth header
    memcpy(&mPacket->ethHeader, pt, ETH_HEADER_SIZE);
    pt += ETH_HEADER_SIZE;
    
    // ip header
    memcpy(&mPacket->ipHeader, pt, IP_HEADER_SIZE);
    pt += IP_HEADER_SIZE;
    
    // tcp header
    memcpy(&mPacket->tcpHeader, pt, TCP_HEADER_SIZE);
    pt += TCP_HEADER_SIZE;
  
    // Modbus TCP header
    memcpy(&mPacket->modbusH, pt, MODBUS_HEADER_SIZE);
    pt += MODBUS_HEADER_SIZE;
  
    // Modbus paylod 
    // function code 
    memcpy(&mPacket->modbusP.functionCode, pt, 1); 
    pt += 1;

    // TODO CAREFULL TCP CAN BE LONGER THAN 20B
    
    // count how big is packet.
    int dataSize = ntohs(mPacket->modbusH.lenght) -2;
    if (dataSize <= 0){
      fprintf(stderr, "Modbus parse error\n");
      exit(1);
    }
    
    // alocation
    mPacket->modbusP.data = malloc(dataSize);
    if (mPacket->modbusP.data == NULL){
      fprintf(stderr, "Malloc error\n");
      exit(1);
    }
    
    memcpy(&mPacket->modbusP.data[0], pt, dataSize);
    return mPacket;
}

/**
 * @brief find packet with: IP_SRC, IP_DST, TCP_DST_PORT 
 * @return true if packet found 
 */
bool findSpecificPakcet(const u_char *frame){
    struct ether_header *ethHeader;  // ethernet  
    struct ip           *ipHeader; 
    struct tcphdr       *tcpHeader; 
    
    // check if this is an ip packet 
    ethHeader = (struct ether_header *)frame;
    if (ntohs(ethHeader->ether_type) != ETHERTYP_IP)
      return false;

    // check if packet is tcp  
    ipHeader  = (struct ip*)(frame + ETH_HEAD);
    if (ipHeader->ip_p != TCP)
      return false;

    // check if ip addreses are ok 
    if (inet_addr(IP_SRC) != ipHeader->ip_src.s_addr
    || inet_addr(IP_DST) != ipHeader->ip_dst.s_addr)
      return false;

    tcpHeader = (struct tcphdr*)(frame + ETH_HEAD + IP_HEAD);
    // check if DST port is alright     
    if (tcpHeader->th_dport != htons(TCP_DST_PORT))
      return false;
    
    // This is a retransmitted packet
    if ((tcpHeader->th_flags & TH_ACK) && !(tcpHeader->th_flags & TH_PUSH)) 
        return false;

    return true;
}


/**
 * @brief Open interface and set *err as erro message 
 * if open fail exit(2)
 * if interface does not support ethernet frame exit(2) 
 */
pcap_t *openInt(char *err, char *name){
    

  // set promiscuous mode - all network data packets can be accessed
  // --- and viewed by all network adapters operating in this mode.
  sniffInterface = pcap_open_live(name, MAX_FRAME_SIZE, true, SNIFF_TIMEOUT, err);
  if (sniffInterface == NULL)
    goto error_interface;
    
  if(pcap_datalink(sniffInterface) != DLT_EN10MB)
    goto error_ether_frame;

  // SIGINT signal handler
  sigemptyset(&sigIntHandler.sa_mask);
  sigIntHandler.sa_handler = freeResources;
  sigIntHandler.sa_flags = 0;
    
  return sniffInterface;

error_interface:
    fprintf(stderr, "Cannot open interface\n");
    fprintf(stderr, "%s\n",err);
    exit(2);
error_ether_frame:
    fprintf(stderr, "Interface does not support Ethernet frame \n");
    exit(2);
}

/**
 * @brief Free resource after signal SIGINT  
 */
void freeResources(int sig_num){
  
  // close socket etc.
  fprintf(stderr, "[signal %d] -> Process killed\n", sig_num);
  pcap_close(sniffInterface);
  exit(1); 
}