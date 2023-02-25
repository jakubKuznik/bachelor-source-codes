CC = gcc
LD = gcc

CFLAGS = -g -std=c11 -pedantic -Wall -Wextra -D_BSD_SOURCE -D_DEFAULT_SOURCE 
all: inject 

##########################################################################

inject: inject.o modbus-packet.o
	gcc $(CFLAGS) inject.o modbus-packet.o -o inject -lpcap

inject.o: inject.c inject.h 
	gcc $(CFLAGS) -c inject.c -o inject.o -lpcap

modbus-packet.o: modbus-packet.c modbus-packet.h
	gcc $(CFLAGS) -c modbus-packet.c -o modbus-packet.o -lpcap

clean:
	rm *.o inject 

run: dos 
	./inject
