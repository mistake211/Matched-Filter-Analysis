# -*- coding: utf-8 -*-
"""
Compares all of the LIA signals  produced when the laser was driven by the 27khz square wave, as well as one LIA signal from when the laser was driven by an arbitrary waveform.

@author: Maxwell
"""
## import the required libraries - these are the only two needed for this example
import numpy as np
import matplotlib.pyplot as plt
                                           ## tell python to print the plot

## call the csv
DATA_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00011.csv', skip_header=5, delimiter=',')
TIME_xlsx   = DATA_xlsx[:, 0]                           ## make an array of the first column only (time in s)
SIGNAL_xlsx = DATA_xlsx[:, 1] 

DATA2_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00014.csv', skip_header=5, delimiter=',')
TIME_xlsx   = DATA_xlsx[:, 0]                           ## make an array of the first column only (time in s)
SIGNAL2_xlsx = DATA2_xlsx[:, 1]
DATA3_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00015.csv', skip_header=5, delimiter=',')
DATA4_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00018.csv', skip_header=5, delimiter=',')
DATAOFF_5_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00012.csv', skip_header=5, delimiter=',')

SIGNAL3_xlsx = DATA3_xlsx[:, 1] 
SIGNAL4_xlsx = DATA4_xlsx[:, 1] 
SIGNAL5_xlsx = DATAOFF_5_xlsx[:, 1] 




## Set up Figure
fig, ax = plt.subplots()

## plot the data
ax.plot(TIME_xlsx, SIGNAL_xlsx, label = '#11(27khz)', color = 'blue')
ax.plot(TIME_xlsx, SIGNAL2_xlsx, label = '#14(27khz)', color = 'red')   
ax.plot(TIME_xlsx, SIGNAL3_xlsx, label = '#15(27khz)', color = 'orange') 
ax.plot(TIME_xlsx, SIGNAL4_xlsx, label = '#18(27khz)', color = 'purple') 
ax.plot(TIME_xlsx, SIGNAL5_xlsx, label = '#12(Arb/OFF)', color = 'green') 
                                ## plot the data
ax.set_xlabel('Time [s]')                                  ## xlabel
ax.set_ylabel('Signal [V]')                                ## ylabel
ax.set_xlim([TIME_xlsx[0], TIME_xlsx[-1]])                           ## set the x axis limit between the first and last element of the 'time'
ax.set_ylim([-.3, 0.15]) 
ax.set_title('Raw PMT data vs. LIA Signal OFF #6') 
ax.legend()                                                 ## finalizes all legend info
plt.show()
