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
int findTcpStream(pcap_t *sniffInterface){
  return 0;
}

/**
 * @brief Open interface and set *err as erro message 
 * if open fail exit(2)
 * if interface does not support ethernet frame exit(2) 
 */
pcap_t *openInt(char *err, char *name){
    
    pcap_t *sniffInt; // interface where packet will be sniffed 

    // set promiscuous mode - all network data packets can be accessed
    // --- and viewed by all network adapters operating in this mode.
    sniffInt = pcap_open_live(name, MAX_FRAME_SIZE, true, SNIFF_TIMEOUT, err);
    if (sniffInt == NULL)
        goto error_interface;
    
    if(pcap_datalink(sniffInt) != DLT_EN10MB)
        goto error_ether_frame;

    // SIGINT signal handler
    sigemptyset(&sigIntHandler.sa_mask);
    sigIntHandler.sa_handler = freeResources;
    sigIntHandler.sa_flags = 0;
    
    return sniffInt;

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