# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: anomaly_detection.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: . 
# Execution:
#      python3 anomaly_detection.py -csva a.csv a1.csv -cvsn b.csv  # basic stats
#      python3 anomaly_detection.py -csva a.csv -cvsn b.csv -m1     # advanced statistic 
#      python3 anomaly_detection.py -csva a.csv -cvsn b.csv -m2     # 3-sigma  
#      python3 anomaly_detection.py -csva a.csv -cvsn b.csv -m3     # T-test  

import argparse
import csv_procesor
import sys
import statistic
import detection_methods as dm 

## Class that contains methods for argparsing and argument validation 
class Arg_parse:
    
    def print_help(self):
        print("Program implements 3 detections methods. If there is no method, it will print basic statistic.")
        print("--------------------------------------------------------")
        print("Examples:")
        print("   python3 anomaly_detection.py -csva a.csv a1.csv -cvsn b.csv  # basic stats")
        print("   python3 anomaly_detection.py -csva a.csv -cvsn b.csv -m1     # advanced statistic ")
        print("   python3 anomaly_detection.py -csva a.csv -cvsn b.csv -m2     # 3-sigma ")
        print("   python3 anomaly_detection.py -csva a.csv -cvsn b.csv -m3     # T-test ")
        print("--------------------------------------------------------")
        print("-csvn 1.csv 2.csv ... n.csv")
        print("     List with Modbus TCP IPFIX csvs that represent normall comunication")
        print("-csva 1.csv 2.csv ... n.csv")
        print("     List with Modbus TCP IPFIX cvss that will be investigated (compared to normal)")
        print("-m1")
        print("     Advanced statistic")
        print("-m2")
        print("     3-sigma")
        print("-m3")
        print("     T-test")
        print("--------------------------------------------------------")

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
       dm.M1.m1_basic_stats(stats_csvn, stats_csva)
    elif args.m2 == True:
       dm.M2.m2_3sigma(stats_csvn, stats_csva)
    elif args.m3 == True:
       dm.M3.m3_t_test(stats_csvn, stats_csva)


    ## if m1 
    # csv.m1()
    dprint("Program end")


if __name__ == '__main__':
    main()
    
