# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: anomaly_detection.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: . 

import numpy
import argparse
import csv_procesor


def print_help():
    print("")


def parse_args():
    parser = argparse.ArgumentParser()
    # Register the print_help function to be called when help is requested
    parser.register('action', 'help', print_help)
    parser.add_argument('-csv', type=str, required=True, help='Input file name')

    args = parser.parse_args()

def main():
    parse_args()
    csv = csv_procesor.Csv_procesor()
    print("Program end")




if __name__ == '__main__':
    main()
    
