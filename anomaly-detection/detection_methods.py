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
    
    # Create the figure and subplots
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
    # Get the data for each pie chart
    modbus_read = [dfN.modbus_read_total, dfA.modbus_read_total]
    modbus_write = [dfN.modbus_write_total, dfA.modbus_write_total]
    modbus_success = [dfN.modbus_success_total, dfA.modbus_success_total]
    
    labels = ['Node', 'Anomaly']
    
    axs[0].pie(modbus_read, autopct='%1.1f%%', startangle=90)
    axs[0].set_title('Modbus Read Total')
    axs[1].pie(modbus_write, autopct='%1.1f%%', startangle=90)
    axs[1].set_title('Modbus Write Total')
    axs[2].pie(modbus_success, autopct='%1.1f%%', startangle=90)
    axs[2].set_title('Modbus Success Total')

    fig.legend(labels, loc='lower center')
    fig.suptitle('Modbus Statistics')

    # Show the chart
    plt.show()

  