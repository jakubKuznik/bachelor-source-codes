CC = gcc
LD = gcc

CFLAGS = -O2 -g -std=c11 -pedantic -Wall -Wextra -D_BSD_SOURCE -D_DEFAULT_SOURCE 
all: replay

##########################################################################

replay: replay.o modbus-packet.o sniff.o
	gcc $(CFLAGS) replay.o modbus-packet.o sniff.o -o replay -lpcap -lz

replay.o: replay.c replay.h 
	gcc $(CFLAGS) -c replay.c -o replay.o -lpcap -lz

modbus-packet.o: modbus-packet.c modbus-packet.h
	gcc $(CFLAGS) -c modbus-packet.c -o modbus-packet.o -lpcap -lz

sniff.o: sniff.c sniff.h
	gcc $(CFLAGS) -c sniff.c -o sniff.o -lpcap -lz

clean:
	rm *.o replay

run: dos 
	./replay
