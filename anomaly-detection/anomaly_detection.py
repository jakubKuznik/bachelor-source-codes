# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: anomaly_detection.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: . 
# Execution:
#      python3 anomaly_detection.py -csva a.csv -cvsn // only get basic statistic 

import argparse
import csv_procesor
import sys
import statistic
import detection_methods as dm 

## Class that contains methods for argparsing and argument validation 
class Arg_parse:
    
    def print_help(self):
        ## todo add message from -h
        print("")

    def __init__(self):
        parser = argparse.ArgumentParser()
        # Register the print_help function to be called when help is requested
        parser.register('action', 'help', self.print_help)
        parser.add_argument('-csvn', nargs="+", required=True, help='n csv files that represent normal comunication')
        parser.add_argument('-csva', nargs="+", required=True, help='n csv files that represent malicious communication')
        parser.add_argument('-m1', action="store_true", help='Start detection method m1')
        parser.add_argument('-m2', action="store_true", help='Start detection method m2')
        parser.add_argument('-m3', action="store_true", help='Start detection method m3')

        self.args = parser.parse_args()
        self.args_method_colision()
        self.check_files()
        

    ## check if methods in arguments are in colison
    def args_method_colision(self):

        # First check. Multiple statistic methods should not be combined 
        if self.args.m1 and (self.args.m2 or self.args.m3):
            eprint("Can't combine multiple statistic methods")
            exit()
        elif self.args.m2 and (self.args.m1 or self.args.m3):
            eprint("Can't combine multiple statistic methods")
            exit()
        elif self.args.m3 and (self.args.m1 or self.args.m2):
            eprint("Can't combine multiple statistic methods")
            exit()

    # check if files can be open for reading 
    def check_files(self):
        dprint(self.args.csvn)
        dprint(self.args.csva)
        
        for file in self.args.csvn:
            try:
                with open(file, 'r') as csvfile:
                    csvfile.close()
            except:
                eprint("Can't open file " + file + " for reading")
                exit()

        for file in self.args.csva:
            try:
                with open(file, 'r') as csvfile:
                    csvfile.close()
            except:
                eprint("Can't open file " + file + " for reading")
                exit()

        dprint("end")

## print to stderr used for error  
def dprint(*args, **kwargs):
    print("DEBUG: ", *args, file=sys.stderr, **kwargs)

## print to stderr used for errors  
def eprint(*args, **kwargs):
    print("ERROR: ", *args, file=sys.stderr, **kwargs)


def main():
    args = Arg_parse().args
    dprint(args)

    csv = csv_procesor.Csv_procesor(csvn=args.csvn, csva=args.csva)
    
    # init statistic class for normal and malicious communication 
    stats_csvn = statistic.Statistic(csv.csvn_df, csv.csvn_duration)
    stats_csva = statistic.Statistic(csv.csva_df, csv.csva_duration)

    # if there is no statistic method just print basic statistic info 
    if (args.m1 == False) and (args.m2 == False) and (args.m3 == False):
        print("CSVA")
        stats_csva.printStatistic()
        print("CSVN")
        stats_csvn.printStatistic()
    
    if args.m1 == True:
       dm.M1.m1_basic_stats(stats_csva, stats_csvn)


    ## if m1 
    # csv.m1()
    dprint("Program end")


if __name__ == '__main__':
    main()
    
