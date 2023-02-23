// Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
// File:        dos.c
// Author:      Jakub Kuzník, FIT
//  

// Execution:

#include "dos.h"



int main(int argc, char *argv[]) {

    modbusPacket mPacket = buildModbusPacket();
    
    return 0;
}

/**
 * @brief Function create modbus packet.
 * it uses constants from dos.h to fill eth/ip/tcp headers.
 * 
 * @return modbusPacket  
 */
modbusPacket buildModbusPacket(){
    printf("hi") ;
}
