# -*- coding: utf-8 -*-
"""
This code compares the C1 and C2 channels of an oscilliscopes output. C1 is the raw PMT data from CHEWIE during Laser Induced Fluorescense. C2 is the signal from a Lock in Amplifier that is given that PMT signal and performs LIA on it. C2 is artificially offset by 0.1V to better show the two signals. 

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

## call the csv
DATA_xlsx   = np.genfromtxt('C1--LIAAdvancedLab--00002.csv', skip_header=5, delimiter=',')
TIME_xlsx   = DATA_xlsx[:, 0]                           ## make an array of the first column only (time in s)
SIGNAL_xlsx = DATA_xlsx[:, 1] 

DATA2_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00002.csv', skip_header=5, delimiter=',')
TIME_xlsx   = DATA_xlsx[:, 0]                           ## make an array of the first column only (time in s)
SIGNAL2_xlsx = DATA2_xlsx[:, 1] + 0.1             ##offset the 2nd datas signal to better show them together
                                         


## Set up Figure
fig, ax = plt.subplots()

## plot the data
ax.plot(TIME_xlsx, SIGNAL_xlsx, label = 'PMT', color = 'blue')
ax.plot(TIME_xlsx, SIGNAL2_xlsx, label = 'LIA', color = 'red')                                  ## plot the data
ax.set_xlabel('Time [s]')                                  ## xlabel
ax.set_ylabel('Signal [V]')                                ## ylabel
ax.set_xlim([TIME_xlsx[0], TIME_xlsx[-1]])                           ## set the x axis limit between the first and last element of the 'time'
ax.set_ylim([-0.125, 0.5]) 
ax.set_title('PMT vs LIA  #2 1st Gen')
ax.legend()                                                 ## finalizes all legend info
plt.show()
