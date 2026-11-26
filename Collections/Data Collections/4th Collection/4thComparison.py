# -*- coding: utf-8 -*-
"""
compares the LIA and PMT signals of csvs from the 4th data collection. C1 is PMT, C2 is LIA. #11, 14, 15, and 18 had a laser driven at 27khz. #12, 13, 16, and 17 were driven by an arbitrary waveform. Laser power for this test was measured before the fiber, meaning the actual power delivered to the plasma was much lower. #11 and 12 had a laser power of 198mW, 13 and 14 has 40mW, 15 and 16 has 151mW, and 17 and 18 had 100mW.
"""
## import the required libraries - these are the only two needed for this example
import numpy as np
import matplotlib.pyplot as plt
                                           ## tell python to print the plot

## call the csv
DATA_xlsx   = np.genfromtxt('C1--LIAAdvancedLab--00012.csv', skip_header=5, delimiter=',')
TIME_xlsx   = DATA_xlsx[:, 0]                           ## make an array of the first column only (time in s)
SIGNAL_xlsx = DATA_xlsx[:, 1] 

DATA2_xlsx   = np.genfromtxt('C2--LIAAdvancedLab--00012.csv', skip_header=5, delimiter=',')
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
ax.set_title('PMT vs LIA @ran 4th Gen')
ax.legend()                                                 ## finalizes all legend info
plt.show()
