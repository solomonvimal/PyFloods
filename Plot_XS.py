# -*- coding: utf-8 -*-
"""
Created on Wed Jul 01 17:11:40 2015

PLotting all the cross-sections (sorted by width) and histogram of widths

@author: Solo
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from operator import sub
os.chdir("C:\Users\Solo\Dropbox\NFIE Project\XSPoints_to_Midpoint")

# plotting all cross-sections:
##### import csv as df
data = pd.read_csv('XS_COMID_averaged.csv')
# Averaged cross-section plotting
#averaged_df = pd.DataFrame(data) 
# df = averaged_df.copy()

# plotting for triangular cross-sections
df = df.copy()


stations = map(int,df.ix[:,'s_0s':'s_10s'].stack())
elevations = map(float,df.ix[:,'d_0s':'d_10s'].stack())
COMIDs = df.ix[:,'COMIDs':].stack()
try: 
    widths = map(int,df.ix[:,'Ws'])
except:
    widths = map(sub, map(int,df.ix[:,'s_10s']), map(int,df.ix[:,'s_0s']))
    pass        
    
plt.figure(1)
for i in range(len(stations)/7):
    if widths[i] < 700:
        plt.subplot(331)
        st = stations[i*7], stations[i*7+1], stations[i*7+2], stations[i*7+3], stations[i*7+4], stations[i*7+5], stations[i*7+6]
        st = map(int, st)
        el = elevations[i*7], elevations[i*7+1], elevations[i*7+2], elevations[i*7+3], elevations[i*7+4], elevations[i*7+5], elevations[i*7+6]
        plt.plot(st,el)
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        #spacing = max(st)/2
        plt.xticks(np.arange(min(st), max(st)+1)) #, spacing))

    elif widths[i] < 1000:
        plt.subplot(332)
        st = stations[i*7], stations[i*7+1], stations[i*7+2], stations[i*7+3], stations[i*7+4], stations[i*7+5], stations[i*7+6]
        st = map(int, st)
        el = elevations[i*7], elevations[i*7+1], elevations[i*7+2], elevations[i*7+3], elevations[i*7+4], elevations[i*7+5], elevations[i*7+6]
        plt.plot(st,el)
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        #spacing = max(st)/2
        plt.xticks(np.arange(min(st), max(st)+1)) #), spacing))
        
    elif widths[i] < 1300:
        plt.subplot(333)
        st = stations[i*7], stations[i*7+1], stations[i*7+2], stations[i*7+3], stations[i*7+4], stations[i*7+5], stations[i*7+6]
        st = map(int, st)
        el = elevations[i*7], elevations[i*7+1], elevations[i*7+2], elevations[i*7+3], elevations[i*7+4], elevations[i*7+5], elevations[i*7+6]
        plt.plot(st,el)        
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = max(st)/2
        plt.xticks(np.arange(min(st), max(st)+1, spacing))
        
    elif widths[i] < 1600:
        plt.subplot(334)
        st = stations[i*7], stations[i*7+1], stations[i*7+2], stations[i*7+3], stations[i*7+4], stations[i*7+5], stations[i*7+6]
        st = map(int, st)
        el = elevations[i*7], elevations[i*7+1], elevations[i*7+2], elevations[i*7+3], elevations[i*7+4], elevations[i*7+5], elevations[i*7+6]
        plt.plot(st,el) 
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = max(st)/2
        plt.xticks(np.arange(min(st), max(st)+1, spacing))
        
    elif widths[i] < 2500:
        plt.subplot(335)
        st = stations[i*7], stations[i*7+1], stations[i*7+2], stations[i*7+3], stations[i*7+4], stations[i*7+5], stations[i*7+6]
        st = map(int, st)
        el = elevations[i*7], elevations[i*7+1], elevations[i*7+2], elevations[i*7+3], elevations[i*7+4], elevations[i*7+5], elevations[i*7+6]
        plt.plot(st,el)         
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = max(st)/2
        plt.xticks(np.arange(min(st), max(st)+1, spacing))
        
    elif widths[i] < 3500:
        plt.subplot(336)
        st = stations[i*7], stations[i*7+1], stations[i*7+2], stations[i*7+3], stations[i*7+4], stations[i*7+5], stations[i*7+6]
        st = map(int, st)
        el = elevations[i*7], elevations[i*7+1], elevations[i*7+2], elevations[i*7+3], elevations[i*7+4], elevations[i*7+5], elevations[i*7+6]
        plt.plot(st,el)  
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = max(st)/2
        plt.xticks(np.arange(min(st), max(st)+1, spacing))
        
    elif widths[i] < 7000:
        plt.subplot(337)
        st = stations[i*7], stations[i*7+1], stations[i*7+2], stations[i*7+3], stations[i*7+4], stations[i*7+5], stations[i*7+6]
        st = map(int, st)
        el = elevations[i*7], elevations[i*7+1], elevations[i*7+2], elevations[i*7+3], elevations[i*7+4], elevations[i*7+5], elevations[i*7+6]
        plt.plot(st,el) 
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = max(st)/2
        plt.xticks(np.arange(min(st), max(st)+1, spacing))
        
    elif widths[i] <9000: 
        plt.subplot(338)
        st = stations[i*7], stations[i*7+1], stations[i*7+2], stations[i*7+3], stations[i*7+4], stations[i*7+5], stations[i*7+6]
        st = map(int, st)
        el = elevations[i*7], elevations[i*7+1], elevations[i*7+2], elevations[i*7+3], elevations[i*7+4], elevations[i*7+5], elevations[i*7+6]
        plt.plot(st,el)  
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = max(st)/2
        plt.xticks(np.arange(min(st), max(st)+1, spacing))
        
    else: 
        plt.subplot(339)
        st = stations[i*7], stations[i*7+1], stations[i*7+2], stations[i*7+3], stations[i*7+4], stations[i*7+5], stations[i*7+6]
        st = map(int, st)
        el = elevations[i*7], elevations[i*7+1], elevations[i*7+2], elevations[i*7+3], elevations[i*7+4], elevations[i*7+5], elevations[i*7+6]
        plt.plot(st,el)          
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = max(st)/2
        plt.xticks(np.arange(min(st), max(st)+1, spacing))
        
1+1 
        
for binwidth in [500, 300, 200, 100, 50,  25]:
    ax = plt.figure(9)  
    print(binwidth)
    ax = plt.subplot()
    plt.hist(widths, bins=range(min(widths), 5000, binwidth), label = str(binwidth)) 
    plt.title('Histogram of Width', size= 35, weight = 'heavy')  
    plt.xlabel('Width in feet', size=25)
    plt.ylabel('Number of cross-sections', size=25)
    plt.rcParams['ytick.labelsize'] = 25
    leg = ax.legend(prop={'size': 25})
    leg.set_title('Bin Width (in feet)', prop={'size': 25, 'weight': 'heavy'})
