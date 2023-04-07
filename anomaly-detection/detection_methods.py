# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: detection_methods.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: . 

import pandas as pd 
import matplotlib.pyplot as plt
import statistic as stat

class M1:

  @staticmethod
  def m1_basic_stats(dfN, dfA):

    M1.plot_modbus_com_tot(dfN, dfA)

  @staticmethod
  def plot_packets(dfN, dfA):
    return

  @staticmethod
  def plot_modbus_com_tot(dfN, dfA):
    # Create the figure and subplots
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
    # Get the data for each pie chart
    modbus_read = [dfN.modbus_read_total, dfA.modbus_read_total]
    modbus_write = [dfN.modbus_write_total, dfA.modbus_write_total]
    modbus_success = [dfN.modbus_success_total, dfA.modbus_success_total]
    
    labels = ['Normální komunikace', 'Útok']
    
    # Format the text to show both the percentage and total number
    def format_pct_value(pct, values):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{:.1f}% ({:d})'.format(pct, val)
    
    axs[0].pie(modbus_read, autopct=lambda pct: format_pct_value(pct, modbus_read), startangle=90)
    axs[0].set_title('Modbus Read příkazy')
    axs[1].pie(modbus_write, autopct=lambda pct: format_pct_value(pct, modbus_write), startangle=90)
    axs[1].set_title('Modbus Write příkazy')
    axs[2].pie(modbus_success, autopct=lambda pct: format_pct_value(pct, modbus_success), startangle=90)
    axs[2].set_title('Modbus Úspěšné příkazy')

    fig.legend(labels, loc='lower center')
    #fig.suptitle('Statistika Modbus komunikace - Normální komunikace vs. útok injektování 10 paketů za minutu')

    # Show the chart
    plt.show()

#  @staticmethod
#  def plot_modbus_com_tot(dfN, dfA):
#    # Create the figure and subplots
#    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
#    # Get the data for each pie chart
#    modbus_read = [dfN.modbus_read_total, dfA.modbus_read_total]
#    modbus_write = [dfN.modbus_write_total, dfA.modbus_write_total]
#    modbus_success = [dfN.modbus_success_total, dfA.modbus_success_total]
    
#    labels = ['Normální komunikace', 'Útok']
    
#    axs[0].pie(modbus_read, autopct='%1.1f%%', startangle=90)
#    axs[0].set_title('Modbus Read příkazy')
#    axs[1].pie(modbus_write, autopct='%1.1f%%', startangle=90)
#    axs[1].set_title('Modbus Write příkazy')
#    axs[2].pie(modbus_success, autopct='%1.1f%%', startangle=90)
#    axs[2].set_title('Modbus Úspěšné příkazy')

#    fig.legend(labels, loc='lower center')
#    fig.suptitle('Injektování 10 paketů za minutu')

#    # Show the chart
#    plt.show()


  