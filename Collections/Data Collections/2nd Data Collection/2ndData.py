# -*- coding: utf-8 -*-
"""
Compares the LIA and PMT signals from a given file. For this 2nd collection, files run from #00001 to #00010.

INPUTS:
  none explicit
OUTPUTS: 
  none explicit

@author: Maxwell Flanagan
"""
## import the required libraries - these are the only two needed for this example
import numpy as np
import matplotlib.pyplot as plt
                                           ## tell python to print the plot

## call the csv. To change csv's, change the number at the end. Ex. file #8 is C1--LIAAdvancedLab--00008. #10 is instead 00010, as the number of digits total must be preserved
DATA_xlsx   = np.genfromtxt('C1--LIAAdvancedLab--00008.csv', skip_header=5, delimiter=',')
TIME_xlsx   = DATA_xlsx[:, 0]                           ## make an array of the first column only (time in s)
SIGNAL_xlsx = DATA_xlsx[:, 1] 

## When changing csv's, make sure to update both DATA_xlsx and DATA2_xlsx so they have the same file number
DATA2_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00008.csv', skip_header=5, delimiter=',')
TIME_xlsx   = DATA_xlsx[:, 0]                           ## make an array of the first column only (time in s)
SIGNAL2_xlsx = DATA2_xlsx[:, 1] + 0.1
                 ##offset the 2nd datas signal to better show them together



## Set up Figure
fig, ax = plt.subplots()

## plot the data
ax.plot(TIME_xlsx, SIGNAL_xlsx, label = '#1', color = 'blue')
ax.plot(TIME_xlsx, SIGNAL2_xlsx, label = '#2', color = 'red')   
                              ## plot the data
ax.set_xlabel('Time [s]')                                  ## xlabel
ax.set_ylabel('Signal [V]')                                ## ylabel
ax.set_xlim([TIME_xlsx[0], TIME_xlsx[-1]])                           ## set the x axis limit between the first and last element of the 'time'
ax.set_ylim([-0.125, 0.5]) 
ax.set_title('PMT data vs. LIA Signal 1.2mW 2nd Gen') 
ax.legend()                                                 ## finalizes all legend info
plt.show()
