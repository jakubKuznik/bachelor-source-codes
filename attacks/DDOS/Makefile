CC = gcc
LD = gcc

CFLAGS = -g -std=c11 -pedantic -Wall -Wextra -D_BSD_SOURCE -D_DEFAULT_SOURCE 
all: dos 

##########################################################################

dos: dos.o modbus-packet.o
	gcc $(CFLAGS) dos.o modbus-packet.o -o dos -lpcap

dos.o: dos.c dos.h 
	gcc $(CFLAGS) -c dos.c -o dos.o -lpcap

modbus-packet.o: modbus-packet.c modbus-packet.h
	gcc $(CFLAGS) -c modbus-packet.c -o modbus-packet.o -lpcap

clean:
	rm *.o dos 

run: dos 
	./dos
