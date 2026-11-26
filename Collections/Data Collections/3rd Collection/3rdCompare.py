# -*- coding: utf-8 -*-
"""
Compares the PMT (C1) signal to the LIA (C2). Files are numbered #0 - 10. The power ended up being too low on the laser, and only the first files with the highest power revealed any signal with the LIA. MFA showed nothing on any.
"""
## import the required libraries - these are the only two needed for this example
import numpy as np
import matplotlib.pyplot as plt
                                           ## tell python to print the plot

## call the csv
DATA_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00001.csv', skip_header=5, delimiter=',')
TIME_xlsx   = DATA_xlsx[:, 0]                           ## make an array of the first column only (time in s)
SIGNAL_xlsx = DATA_xlsx[:, 1] 

DATA2_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00002.csv', skip_header=5, delimiter=',')
TIME_xlsx   = DATA_xlsx[:, 0]                           ## make an array of the first column only (time in s)
SIGNAL2_xlsx = DATA2_xlsx[:, 1]
DATA3_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00003.csv', skip_header=5, delimiter=',')
DATA4_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00004.csv', skip_header=5, delimiter=',')
DATAOFF_5_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00005.csv', skip_header=5, delimiter=',')
DATAOFF_6_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00006.csv', skip_header=5, delimiter=',')
DATA7_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00007.csv', skip_header=5, delimiter=',')
DATA8_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00008.csv', skip_header=5, delimiter=',')
DATA9_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00009.csv', skip_header=5, delimiter=',')
DATA10_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00010.csv', skip_header=5, delimiter=',')
SIGNAL3_xlsx = DATA3_xlsx[:, 1] 
SIGNAL4_xlsx = DATA4_xlsx[:, 1] 
SIGNAL5_xlsx = DATAOFF_5_xlsx[:, 1] 
SIGNAL6_xlsx = DATAOFF_6_xlsx[:, 1] 
SIGNAL7_xlsx = DATA7_xlsx[:, 1] 
SIGNAL8_xlsx = DATA8_xlsx[:, 1] 
SIGNAL9_xlsx = DATA9_xlsx[:, 1] 
SIGNAL10_xlsx = DATA10_xlsx[:, 1] 


## Set up Figure
fig, ax = plt.subplots()

## plot the data
ax.plot(TIME_xlsx, SIGNAL_xlsx, label = '#1', color = 'blue')
ax.plot(TIME_xlsx, SIGNAL2_xlsx, label = '#2', color = 'red')   
ax.plot(TIME_xlsx, SIGNAL3_xlsx, label = '#3', color = 'orange') 
ax.plot(TIME_xlsx, SIGNAL4_xlsx, label = '#4', color = 'purple') 
ax.plot(TIME_xlsx, SIGNAL5_xlsx, label = '#5', color = 'green') 
ax.plot(TIME_xlsx, SIGNAL6_xlsx, label = '#6', color = 'pink') 
ax.plot(TIME_xlsx, SIGNAL7_xlsx, label = '#7', color = 'violet') 
ax.plot(TIME_xlsx, SIGNAL8_xlsx, label = '#8', color = 'cyan') 
ax.plot(TIME_xlsx, SIGNAL9_xlsx, label = '#9', color = 'yellow') 
ax.plot(TIME_xlsx, SIGNAL10_xlsx, label = '#10', color = 'magenta')                                ## plot the data
ax.set_xlabel('Time [s]')                                  ## xlabel
ax.set_ylabel('Signal [V]')                                ## ylabel
ax.set_xlim([TIME_xlsx[0], TIME_xlsx[-1]])                           ## set the x axis limit between the first and last element of the 'time'
ax.set_ylim([-.3, 0.65]) 
ax.set_title('Raw PMT data vs. LIA Signal OFF #6') 
ax.legend()                                                 ## finalizes all legend info
plt.show()
