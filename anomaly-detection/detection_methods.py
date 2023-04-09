# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: detection_methods.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: . 

import pandas as pd 
import matplotlib.pyplot as plt
import statistic as stat

import numpy as np
from scipy.stats import norm

class M2:
  @staticmethod
  def m2_3sigma(dfN, dfA):
    mean = dfN.modbus_write_total
    sigma = dfN.modbus_write_sigma # Σ(xᵢ - μ)² / n
    #dispersion = sigma * sigma 
    #significance_level = 0.05 # 5% chance of rejecting 
    #upper_bound = mean + (3 * sigma)
    #lower_bound = mean - (3 * sigma)
    
    print("DEBUG: 3 sigma test")
    print("DEBUG: mean deviation: " + str(sigma))
    #print("DEBUG: dispersion:     " + str(dispersion))
    #print("DEBUG: signifi level:  " + str(significance_level))
    #print("DEBUG: upper bound:    " + str(upper_bound))
    #print("DEBUG: 3 lower bound:  " + str(lower_bound))

    M2.plot_write(mean, sigma, dfA.modbus_write_total)


    mean2 = dfN.modbus_packets_sum
    sigma2 = dfN.modbus_packets_sigma # Σ(xᵢ - μ)² / n
    #dispersion2 = sigma2 * sigma2 
    #significance_level2 = 0.05 # 5% chance of rejecting 
    #upper_bound2 = mean + (3 * sigma)
    #lower_bound2 = mean - (3 * sigma)
    M2.plot_packets(mean2, sigma2, dfA.modbus_packets_sum)

    return
  
  @staticmethod 
  def plot_packets(mean, sigma, anomaly):

    # Create an array of x-values for the plot
    x = np.linspace(mean - 4*sigma, mean + 4*sigma, 1000)

    # Calculate the normal distribution values for the x-values
    y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / sigma)**2)

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(x, y)

        # Add vertical lines for 1, 2, and 3 standard deviations
    stds = [1, 2, 3]
    colors = ['r', 'g', 'b']
    labels = ['1σ', '2σ', '3σ']
    for std, color, label in zip(stds, colors, labels):
      x_left = mean - std*sigma
      x_right = mean + std*sigma
      ax.axvline(x_left, color=color, linestyle='--')
      ax.axvline(x_right, color=color, linestyle='--')
      ax.text(x_left, 1.05, label, transform=ax.get_xaxis_transform(), color=color, ha='center')
    
    ax.scatter(anomaly, 0, marker='x', color='red')
    ax.set_xlabel('Modbus pakety (5min)')
    ax.set_ylabel('Pravděpodobnost')
    plt.show()

  @staticmethod 
  def plot_write(mean, sigma, anomaly):

    # Create an array of x-values for the plot
    x = np.linspace(mean - 4*sigma, mean + 4*sigma, 1000)

    # Calculate the normal distribution values for the x-values
    y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / sigma)**2)

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(x, y)

        # Add vertical lines for 1, 2, and 3 standard deviations
    stds = [1, 2, 3]
    colors = ['r', 'g', 'b']
    labels = ['1σ', '2σ', '3σ']
    for std, color, label in zip(stds, colors, labels):
      x_left = mean - std*sigma
      x_right = mean + std*sigma
      ax.axvline(x_left, color=color, linestyle='--')
      ax.axvline(x_right, color=color, linestyle='--')
      ax.text(x_left, 1.05, label, transform=ax.get_xaxis_transform(), color=color, ha='center')
    
    ax.scatter(anomaly, 0, marker='x', color='red')
    ax.set_xlabel('Modbus Write příkazy (5min)')
    ax.set_ylabel('Pravděpodobnost')
    plt.show()

class M1:

  @staticmethod
  def m1_basic_stats(dfN, dfA):

    M1.plot_modbus_com_tot(dfN, dfA)
    M1.plot_packets(dfN, dfA)    
    M1.plot_detail_252(dfN, dfA)    

  # @staticmethod 
  # todo check other connections for tcp 

  # @staticmethod
  # todo request vs succes ratio 


  @staticmethod
  def plot_detail_252(dfN, dfA):
    # Create the figure and subplots
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    
    # Get the data for each pie chart
    write = [dfN.modbus_write_250_252 , dfA.modbus_write_250_252]
    read  = [dfN.modbus_read_250_252, dfA.modbus_read_250_252]
    
    labels = ['Normální komunikace', 'Útok']
    
    axs[0].pie(write, autopct=lambda pct: M1.format_pct_value(pct, write), startangle=90)
    axs[0].set_title('Počet write příkazů na zařízení .252')
    axs[1].pie(read, autopct=lambda pct: M1.format_pct_value(pct, read), startangle=90)
    axs[1].set_title('Počet read příkazů na zařízení .252')

    fig.legend(labels, loc='lower center')
    plt.show()

  ## it display number of packets trasmitted between each station 
  @staticmethod
  def plot_packets(dfN, dfA):
    
    # Create the figure and subplots
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
    # Get the data for each pie chart
    # p_250_251 = [dfN.packets_250_251, dfA.packets_250_251]
    p_250_252 = [dfN.packets_250_252, dfA.packets_250_252]
    p_250_253 = [dfN.packets_250_253, dfA.packets_250_253]
    p_250_254 = [dfN.packets_250_254, dfA.packets_250_254]
    
    
    labels = ['Normální komunikace', 'Útok']
    
    #axs[0].pie(p_250_251, autopct=lambda pct: M1.format_pct_value(pct, p_250_251), startangle=90)
    #axs[0].set_title('Pakety mezi .251 a .252')
    axs[0].pie(p_250_252, autopct=lambda pct: M1.format_pct_value(pct, p_250_252), startangle=90)
    axs[0].set_title('Počet paketů mezi .250 a .252')
    axs[1].pie(p_250_253, autopct=lambda pct: M1.format_pct_value(pct, p_250_253), startangle=90)
    axs[1].set_title('Počet paketů .250 a .253')
    axs[2].pie(p_250_254, autopct=lambda pct: M1.format_pct_value(pct, p_250_254), startangle=90)
    axs[2].set_title('Počet paketů .250 a .254')

    fig.legend(labels, loc='lower center')
    plt.show()
    
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
    
    axs[0].pie(modbus_read, autopct=lambda pct: M1.format_pct_value(pct, modbus_read), startangle=90)
    axs[0].set_title('Modbus Read příkazy')
    axs[1].pie(modbus_write, autopct=lambda pct: M1.format_pct_value(pct, modbus_write), startangle=90)
    axs[1].set_title('Modbus Write příkazy')
    axs[2].pie(modbus_success, autopct=lambda pct: M1.format_pct_value(pct, modbus_success), startangle=90)
    axs[2].set_title('Modbus Úspěšné příkazy')

    fig.legend(labels, loc='lower center')
    #fig.suptitle('Statistika Modbus komunikace - Normální komunikace vs. útok injektování 10 paketů za minutu')
    plt.show()
    return
    
    
  # Format the text to show both the percentage and total number
  @staticmethod
  def format_pct_value(pct, values):
    total = sum(values)
    val = int(round(pct*total/100.0))
    return '{:.1f}% ({:d})'.format(pct, val)


  