CC = gcc
LD = gcc

CFLAGS = -g -std=c11 -pedantic -Wall -Wextra -D_BSD_SOURCE -D_DEFAULT_SOURCE 
all: dos 

##########################################################################

dos: dos.o 
	gcc $(CFLAGS) dos.o -o dos -lpcap

dos.o: dos.c dos.h 
	gcc $(CFLAGS) -c dos.c -o dos.o -lpcap

clean:
	rm *.o dos 

run: dos 
	./dos
