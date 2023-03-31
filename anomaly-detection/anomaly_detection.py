# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: anomaly_detection.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: . 

import numpy
import argparse
import csv_procesor
import sys


def print_help():
    ## todo add message from -h
    print("")


def parse_args():
    parser = argparse.ArgumentParser()
    # Register the print_help function to be called when help is requested
    parser.register('action', 'help', print_help)
    parser.add_argument('-csvn', nargs="+", required=True, help='n csv files that represent normal comunication')
    parser.add_argument('-csva', nargs="+", required=True, help='n csv files that represent malicious communication')
    parser.add_argument('-m1', action="store_true", help='Start detection method m1')
    parser.add_argument('-m2', action="store_true", help='Start detection method m2')
    parser.add_argument('-m3', action="store_true", help='Start detection method m3')

    args = parser.parse_args()
    print(args)
    args_method_colision(args)
    


## check if methods in arguments are in colison
def args_method_colision(args):

    # First check. Multiple statistic methods should not be combined 
    if args.m1 and (args.m2 or args.m3):
        eprint("Can't combine multiple statistic methods")
        exit()
    elif args.m2 and (args.m1 or args.m3):
        eprint("Can't combine multiple statistic methods")
        exit()
    elif args.m3 and (args.m1 or args.m2):
        eprint("Can't combine multiple statistic methods")
        exit()


## print to stderr used for error  
def dprint(*args, **kwargs):
    print("DEBUG: ", *args, file=sys.stderr, **kwargs)

## print to stderr used for errors  
def eprint(*args, **kwargs):
    print("ERROR: ", *args, file=sys.stderr, **kwargs)


def main():
    parse_args()
    csv = csv_procesor.Csv_procesor()
    print("Program end")




if __name__ == '__main__':
    main()
    
