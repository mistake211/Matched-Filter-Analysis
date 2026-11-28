#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 12:53:12 2026

@author: max
"""

## import the required libraries - these are the only two needed for this example
import numpy as np
import matplotlib.pyplot as plt
                                           ## tell python to print the plot

## call the csv
DATA_xlsx   = np.genfromtxt('C1--flux--00000.csv', skip_header=5, delimiter=',')
TIME_xlsx   = DATA_xlsx[:, 0]                           ## make an array of the first column only (time in s)
SIGNAL_xlsx = DATA_xlsx[:, 1] 

## Set up Figure
fig, ax = plt.subplots()

## plot the data
ax.plot(TIME_xlsx, SIGNAL_xlsx, label = 'Output', color = 'blue')
ax.set_xlabel('Time [s]')                                  ## xlabel
ax.set_ylabel('Amplitude')                                ## ylabel
ax.set_xlim([0, 0.003])                           ## set the x axis limit between the first and last element of the 'time'
ax.set_ylim([-0.125, 3]) 
ax.set_title('Time Vs Amplitude (random)') 
ax.legend()                                                 ## finalizes all legend info
plt.show()