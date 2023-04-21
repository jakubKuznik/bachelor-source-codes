# Solution for BACHELOR’S THESIS: atack generation on industrial modbus network 
# File name: detection_methods.py 
# Authors: Jakub Kuzník <xkuzni04>
# institution: VUT FIT 
# Description: File implements 3 statistical methods  

import pandas as pd 
import matplotlib.pyplot as plt
from scipy.stats import ttest_1samp

import numpy as np
from scipy.stats import norm
import seaborn as sns

import warnings
warnings.filterwarnings("ignore", message="The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.")
## class M3 implements t-test 
class M3:
  @staticmethod
  def m3_t_test(dfN, dfA):
    print("DEBUG: t-test")
    sliced_comunication = M3.slice_stats(dfA)
    # todo t-test rozdelime utok na x 60 sekundovych intervalu a provedeme t-test
    write_req     = M3.get_write_request(sliced_comunication)
    write_req_252 = M3.get_write_request_252(sliced_comunication) 

    M3.t_test(write_req, dfN.modbus_write_total * 0.2, "T test write packtes")
    M3.t_test(write_req_252, dfN.modbus_write_250_252 * 0.2, "T test write packets 252")

  @staticmethod 
  def t_test(values, mean, text):
    t_stat, p_val = ttest_1samp(values, mean)
    print("---------------------------------------")
    print(text)
    print("mean:", mean)
    print("tested values:", values)
    print("t-statistic:", t_stat)
    print("p-value:", p_val)
    if p_val < 0.05:
        print("The t-test has a statistically significant difference")
    else:
        print("The t-test does not have a statistically significant difference")
    print("---------------------------------------")


  @staticmethod
  # return list of modbus write commands per 60sec  
  def get_write_request(slices):
    out = []
    for s in slices:
      out.append((s['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int).sum()))
    return out
  
  @staticmethod
  # return list of modbus write commands per 60sec  
  def get_write_request_252(slices):
    out = []
    for s in slices:
      temp = (s[(s['L3_IPV4_SRC'] == '192.168.88.250') & (s['L3_IPV4_DST'] == '192.168.88.252')])
      out.append((temp['MODBUS_WRITE_REQUESTS'].replace('NIL', '0').astype(int).sum()))
    return out
  
  @staticmethod
  ## method slices pandas into one minute chunks and return list with these chunks 
  def slice_stats(dfA):
    dfA.df = dfA.df.sort_values(by='START_SEC')
    starttime    = pd.to_datetime(dfA.df.iloc[0]["START_SEC"])
    slices_total = int(dfA.duration_sec // 60)
    ## sliced pandas dataframe 
    slices        = []
    # one slice of data frame (0min, 1min)
    slice = pd.DataFrame()
    time_block_end = starttime + pd.Timedelta(seconds=60)
    n = 0 # current slice 
    
    for index, row in dfA.df.iterrows():
        curr_time = pd.to_datetime(row['START_SEC'])
        # end of block 
        if curr_time > time_block_end:
            slices.append(slice)
            slice = pd.DataFrame()
            n += 1 
            if n == slices_total: # if last block 
                break
            # start new slice 
            time_block_end += pd.Timedelta(seconds=60)
        slice = slice.append(row)
        # slice = pd.concat([slice, row], axis=1) FUTURE PANDAS VERSION
    
    return slices

## class M2 implements and plot 3-sigma rule detection
class M2:
  @staticmethod
  def m2_3sigma(dfN, dfA):
    print("DEBUG: 3 sigma test")

    # 3 sigma test on total modbus packets  
    mean1    = dfN.modbus_packets_sum
    sigma1   = dfN.modbus_packets_sigma # Σ(xᵢ - μ)² / n
    anomaly1 = dfA.modbus_packets_sum
    M2.plot_result(mean1, sigma1, anomaly1, "Modbus pakety (5min)", "Pravděpodobnost")
    
    # 3 sigma test on total modbus writes  
    mean2    = dfN.modbus_write_total
    sigma2   = dfN.modbus_write_sigma # Σ(xᵢ - μ)² / n
    anomaly2 = dfA.modbus_write_total
    M2.plot_result(mean2, sigma2, anomaly2, "Modbus Write příkazy (5min)", "Pravděpodobnost")
    
    # 3 sigma test on total modbus packets between master <-> .252
    mean3    = dfN.packets_250_252
    sigma3   = dfN.packets_250_252_sigma # Σ(xᵢ - μ)² / n
    anomaly3 = dfA.packets_250_252
    M2.plot_result(mean3, sigma3, anomaly3, "Modbus pakety na zařízení .252 (5min)", "Pravděpodobnost")
    
    # 3 sigma test on total modbus writes between master <-> .252
    mean4    = dfN.modbus_write_250_252
    sigma4   = dfN.modbus_write_250_252_sigma # Σ(xᵢ - μ)² / n
    anomaly4 = dfA.modbus_write_250_252 
    M2.plot_result(mean4, sigma4, anomaly4, "Modbus Write příkazy na zařízení .252 (5min)", "Pravděpodobnost")
    
    return

  @staticmethod
  def plot_result(mean, sigma, anomaly, x_desc, y_desc):
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
    ax.set_xlabel(x_desc)
    ax.set_ylabel(y_desc)

    plt.show()

## class M2 plot basic statistic comparation 
class M1:

  @staticmethod
  def m1_basic_stats(dfN, dfA):

    M1.plot_modbus_com_tot(dfN, dfA)
    #M1.plot_packets(dfN, dfA)    
    #M1.plot_detail_252(dfN, dfA)    
    #M1.plot_succ_ratio(dfA)

  @staticmethod
  def format_pct_value(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%".format(pct)
  
  @staticmethod
  def plot_succ_ratio(dfA):
    # Create the figure and subplots
    fig, ax   = plt.subplots(figsize=(1, 1))
    fig2, ax2 = plt.subplots(figsize=(1, 1))

    # Get the data
    total_commands = dfA.modbus_commands_total
    succ_commands  = dfA.modbus_succ_total

    total_commands_252 = dfA.modbus_commands_total_252
    successful_commands_250_252 = dfA.modbus_succ_total_250_252

    if succ_commands > total_commands: 
      succ_commands = total_commands
    if successful_commands_250_252 > total_commands_252:
      successful_commands_250_252 = total_commands_252

    # Calculate the ratios
    ratio1 = successful_commands_250_252 / total_commands_252
    ratio2 = (total_commands_252 - successful_commands_250_252) / total_commands_252

    ratio3 = succ_commands / total_commands
    ratio4 = (total_commands - succ_commands) / total_commands

    # Create the bar plot
    ax.barh(0, successful_commands_250_252, height=0.5)
    ax.barh(0, total_commands_252 - successful_commands_250_252, left=successful_commands_250_252, height=0.5, color='orange')
    
    # Create the bar plot
    ax2.barh(0, succ_commands, height=0.5)
    ax2.barh(0, total_commands - succ_commands, left=succ_commands, height=0.5, color='orange')

    # Set the x and y limits
    ax.set_xlim([0, total_commands_252])
    ax.set_ylim([-0.25, 0.25])
    
    # Set the x and y limits
    ax2.set_xlim([0, total_commands])
    ax2.set_ylim([-0.25, 0.25])

    # Set the tick labels and title
    ax.set_yticks([])
    ax.set_title('Počet úspěšných a neúspěšných Modbus příkazů s zařízením .252')
    
    # Set the tick labels and title
    ax2.set_yticks([])
    ax2.set_title('Počet úspěšných a neúspěšných Modbus příkazů')

    # Add the percentage labels
    ax.text(successful_commands_250_252/2, 0, M1.format_pct_value(ratio1*100, [successful_commands_250_252, total_commands_252 - successful_commands_250_252]), ha='center', va='center', color='white')
    ax.text(successful_commands_250_252 + (total_commands_252 - successful_commands_250_252)/2, 0, M1.format_pct_value(ratio2*100, [total_commands_252 - successful_commands_250_252, successful_commands_250_252]), ha='center', va='center', color='white')
    ax2.text(succ_commands/2, 0, M1.format_pct_value(ratio3*100, [succ_commands, total_commands - succ_commands]), ha='center', va='center', color='white')
    ax2.text(succ_commands + (total_commands - succ_commands)/2, 0, M1.format_pct_value(ratio4*100, [total_commands - succ_commands, succ_commands]), ha='center', va='center', color='white')

    plt.show()

  @staticmethod
  ## It plots ratio between write/read commands  
  def plot_detail_252(dfN, dfA):
    # Create the figure and subplots
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    
    # Get the data for each pie chart
    write = [dfN.modbus_write_250_252 , dfA.modbus_write_250_252]
    read  = [dfN.modbus_read_250_252, dfA.modbus_read_250_252]
    
    #labels = ['Normální komunikace', 'Útok']
    labels = ['Normální komunikace', 'Testovaná komunikace']
    
    axs[0].pie(write, autopct=lambda pct: M1.format_pct_value(pct, write), startangle=90)
    axs[0].set_title('Počet write příkazů na zařízení .252')
    axs[1].pie(read, autopct=lambda pct: M1.format_pct_value(pct, read), startangle=90)
    axs[1].set_title('Počet read příkazů na zařízení .252')

    fig.legend(labels, loc='lower center')
    plt.show()

  @staticmethod
  ## it plots number of packets trasmitted between each station 
  def plot_packets(dfN, dfA):

    # Create the figure and subplots
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
    # Get the data for each pie chart
    # p_250_251 = [dfN.packets_250_251, dfA.packets_250_251]
    p_250_252 = [dfN.packets_250_252, dfA.packets_250_252]
    p_250_253 = [dfN.packets_250_253, dfA.packets_250_253]
    p_250_254 = [dfN.packets_250_254, dfA.packets_250_254]
    
    labels = ['Normální komunikace', 'Testovaná komunikace']
    #labels = ['Normální komunikace', 'Útok']
    
    axs[0].pie(p_250_252, autopct=lambda pct: M1.format_pct_value(pct, p_250_252), startangle=90)
    axs[0].set_title('Počet paketů mezi .250 a .252')
    axs[1].pie(p_250_253, autopct=lambda pct: M1.format_pct_value(pct, p_250_253), startangle=90)
    axs[1].set_title('Počet paketů mezi .250 a .253')
    axs[2].pie(p_250_254, autopct=lambda pct: M1.format_pct_value(pct, p_250_254), startangle=90)
    axs[2].set_title('Počet paketů mezi .250 a .254')

    fig.legend(labels, loc='lower center')
    plt.show()

    # Get the data for each bar chart
    #modbus_read = [dfN.modbus_read_total, dfA.modbus_read_total]
    #modbus_write = [dfN.modbus_write_total, dfA.modbus_write_total]
    #modbus_success = [dfN.modbus_succ_total, dfA.modbus_succ_total]
  @staticmethod
  def plot_modbus_com_tot(dfN, dfA):
    # Create the figure and subplots
    fig, axs = plt.subplots(1, 3, figsize=(6, 2))

    ## subplot 1 
    # Create a pandas DataFrame to use for the bar chart
    df = pd.DataFrame({' ': ['Normal', 'Test'], '  ': [dfN.modbus_read_total, dfA.modbus_read_total]})
    # Create the bar chart using seaborn
    sns.barplot(x=' ', y='  ', data=df, ax=axs[0])
    axs[0].set_title('Modbus read příkazy', fontsize=10)
    
    ## subplot 2 
    # Create a pandas DataFrame to use for the bar chart
    df = pd.DataFrame({' ': ['Normal', 'Test'], '  ': [dfN.modbus_write_total, dfA.modbus_write_total]})
    # Create the bar chart using seaborn
    sns.barplot(x=' ', y='  ', data=df, ax=axs[1])
    axs[1].set_title('Modbus write příkazy', fontsize=10)

    ## subplot 3 
    # Create a pandas DataFrame to use for the bar chart
    df = pd.DataFrame({' ': ['Normal', 'Test'], '  ': [dfN.modbus_succ_total, dfA.modbus_succ_total]})
    # Create the bar chart using seaborn
    sns.barplot(x=' ', y='  ', data=df, ax=axs[2])
    axs[2].set_title('Modbus write příkazy', fontsize=10)

    plt.subplots_adjust(wspace=0.5)
    plt.show() 



  @staticmethod
  def pie_plot_modbus_com_tot(dfN, dfA):
    # Create the figure and subplots
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
    # Get the data for each pie chart
    modbus_read = [dfN.modbus_read_total, dfA.modbus_read_total]
    modbus_write = [dfN.modbus_write_total, dfA.modbus_write_total]
    modbus_success = [dfN.modbus_succ_total, dfA.modbus_succ_total]
    
    labels = ['Normální komunikace', 'Testovaná komunikace']
    #labels = ['Normální komunikace', 'Útok']
    
    axs[0].pie(modbus_read, autopct=lambda pct: M1.format_pct_value(pct, modbus_read), startangle=90)
    axs[0].set_title('Modbus Read příkazy')
    axs[1].pie(modbus_write, autopct=lambda pct: M1.format_pct_value(pct, modbus_write), startangle=90)
    axs[1].set_title('Modbus Write příkazy')
    axs[2].pie(modbus_success, autopct=lambda pct: M1.format_pct_value(pct, modbus_success), startangle=90)
    axs[2].set_title('Modbus Úspěšné příkazy')

    fig.legend(labels, loc='lower center')
    plt.show()
    
  # Format the text to show both the percentage and total number
  @staticmethod
  def format_pct_value(pct, values):
    total = sum(values)
    val = int(round(pct*total/100.0))
    return '{:.1f}% ({:d})'.format(pct, val)


  