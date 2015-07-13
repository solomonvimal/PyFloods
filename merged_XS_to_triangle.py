# -*- coding: utf-8 -*-
"""
Created on Thu Jul 09 17:32:35 2015
Convert merged cross-sections to simplified triangles where the outer banks points are higher than the centerpoint. 
Crude method of doing it, beware! 
@author: Solomon Vimal
"""
import os
from numpy import genfromtxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

############# 
# Get the HEC-RAS model dataframe and get the column names
hec_path = "C:\Users\Solo\Dropbox\NFIE\NFIE Project\XSPoints_to_Midpoint\\XS_COMID_averaged.csv"
HEC_df = pd.read_csv(hec_path)
connectivity_data_location = r'C:\\Users\\Solo\\Dropbox\\NFIE\\NFIE Project\\XSPoints_to_Midpoint\\connectivity_file_merged_converted'
connectivity_data = genfromtxt(connectivity_data_location, delimiter = '\t')
cols = HEC_df.columns.tolist()
cols_changed = cols[0:2]+[cols[2]]+[cols[9]]+\
               [cols[3]]+[cols[10]]+[cols[4]]+\
               [cols[11]]+[cols[5]]+[cols[12]]+\
               [cols[6]]+[cols[13]]+[cols[7]]+[cols[14]]+\
               [cols[8]]+[cols[15]]
#Station Elevation column names as per SPRNT connectivity file               
columns_S_E = cols_changed[2:]          

# Connectivity column names
connectivity_df_columns = ['COMIDs','FromNode','ToNode','Divergence','Length(km)(to meter)',
               'Mean Annual Flow (ft^3/s to M^3/s)','Slope','Latitude',
               'Longtitude','Shape Flag']+columns_S_E     

#Reorder HEC_df column names as per SPRNT connectivity file
HEC_df2 = HEC_df[cols_changed]
HEC_df2 = HEC_df2.set_index("COMIDs")

# Check new columns
HEC_df2.columns
             
# Create connectivity dataframe               
connectivity_df = pd.DataFrame(connectivity_data[0:,0:],
                  columns = connectivity_df_columns,
                  index = [connectivity_data[0:,0]])
                  
#Triangular cross-section columns
new_connectivity_df_columns =  ['COMIDs','FromNode','ToNode','Divergence','Length(km)(to meter)',
                                'Mean Annual Flow (ft^3/s to M^3/s)','Slope','Latitude',
                                'Longtitude','Shape Flag','s_0s','d_0s','s_5s','d_5s','s_10s','d_10s']
new_connectivity_df = connectivity_df.loc[:,new_connectivity_df_columns].copy()
connectivity_df.loc(:,new_connectivity_df.columns)

#df = connectivity_df.copy() # 7 Stations
df = new_connectivity_df.copy() # Triangular - 3 stations
both_banks_low = df.ix[(  (df['d_0s']) < (df['d_5s']) ) & ((df['d_10s']) < (df['d_5s'])   ) ]# | (df['d_10s'] > (df['d_5s'])] #< 5)& (df['d_8s'] <10)] #| (df['column3'] == 'c'] # Hill - 21687440.0
one_bank_low = df.ix[(  (df['d_0s']) < (df['d_5s']) ) | ((df['d_10s']) < (df['d_5s'])   ) ]
length_one_bank = list(one_bank_low.ix[:,'Length(km)(to meter)'])

bad_comids = [x for x in map(int,list(one_bank_low.index)) if x in list(df.index)]

bad_XS = new_connectivity_df.ix[bad_comids]

triangle_data =  new_connectivity_df.ix[bad_comids, "s_0s":"d_10s"]

# Work on the part below
triangle_data[:]

df = new_connectivity_df.copy()

for i in  bad_comids:
    if df.loc[i, "d_0s"] < df.loc[i, "d_5s"] < df.loc[i, "d_10s"]:
        print('left lowest bank')
        mid = df.loc[i, "d_5s"]         
        df.loc[i, "d_5s"] = df.loc[i, "d_0s"]
        df.loc[i, "d_0s"] = mid
                      
    if df.loc[i, "d_0s"] > df.loc[i, "d_5s"] > df.loc[i, "d_10s"]:
        print('concave cross-section')
        mid = df.loc[i, "d_5s"]
        df.loc[i,"d_5s"] = df.loc[i, "d_10s"] 
        df.loc[i, "d_10s"] = mid
        # Replace the mid point with the minimum and the bank points with the diff between max and min
    if df.loc[i, "d_0s"] < df.loc[i, "d_5s"] > df.loc[i, "d_10s"]:
        print('right lowest bank')
        mx = max(df.loc[i, "d_0s"],df.loc[i, "d_5s"],df.loc[i, "d_10s"])
        mn = min(df.loc[i, "d_0s"],df.loc[i, "d_5s"],df.loc[i, "d_10s"])
        df.loc[i, "s_0s":"d_10s"] = mx-mn
        df.loc[i, "s_0s":"d_10s"] = mn
        df.loc[i, "s_0s":"d_10s"] = mx-mn
    if  df.loc[i, "d_0s"] == df.loc[i, "d_5s"] or df.loc[i, "d_5s"] == df.loc[i, "d_10s"]:
        df.loc[i, "d_0s"]  = df.loc[i, "d_0s"] + 0.1
        df.loc[i, "d_10s"]  = df.loc[i, "d_10s"] + 0.1 #i = 21687628 # has mid and left bank equal length


###### Check again
both_banks_low = df.ix[(  (df['d_0s']) < (df['d_5s']) ) & ((df['d_10s']) < (df['d_5s'])   ) ]# | (df['d_10s'] > (df['d_5s'])] #< 5)& (df['d_8s'] <10)] #| (df['column3'] == 'c'] # Hill - 21687440.0
one_bank_low = df.ix[(  (df['d_0s']) < (df['d_5s']) ) | ((df['d_10s']) < (df['d_5s'])   ) ]
os.chdir('C:\\Users\\Solo\\Dropbox\\NFIE\\NFIE Project')


### Use this df to plot in the XSPlot script

# write unconfined COMIDs to a csv file
unconfined_comids = one_bank_low.loc[:,'COMIDs'].apply(int)
unconfined_comids.to_csv('unconfined_COMIDs', header=False, index=False, sep=',', encoding='utf-8')

for binwidth in [500, 300, 200, 100, 50,  25]:
    ax = plt.figure(1)  
    print(binwidth)
    ax = plt.subplot()
    plt.hist(length_one_bank, bins=range(int(min(length_one_bank)), 5000, binwidth), label = str(binwidth)) 
    plt.title('Histogram of lengths where cross-sections are unconfined at banks', size= 35)#, weight = 'light')  
    plt.xlabel('Length (meter)', size=25)
    plt.ylabel('Number of cross-sections', size=25)
    plt.rcParams['ytick.labelsize'] = 25
    plt.rcParams['xtick.labelsize'] = 25
    leg = ax.legend(prop={'size': 25})
    leg.set_title('Bin size (meter)', prop={'size': 25, 'weight': 'heavy'})
    

import os
os.chdir('C:\\Users\\Solo\\Dropbox\\NFIE')
# Write to CSV
df.to_csv('SPRNT_triangular_XS', header=False, index=False,sep='\t', encoding='utf-8')



############         Plots   ############################


stations = map(int,df.ix[:,['s_0s','s_5s','s_10s']].stack())
elevations = map(float,df.ix[:,['d_0s','d_5s','d_10s']].stack())
COMIDs = df.ix[:,'COMIDs':].stack()
try: 
    widths = map(int,df.ix[:,'Ws'])
except:
    widths = map(sub, map(int,df.ix[:,'s_10s']), map(int,df.ix[:,'s_0s']))
    pass        
    
plt.figure(1)
for i in range(len(stations)/3):
    if widths[i] < 700:
        plt.subplot(331)
        st = stations[i*3], stations[i*3+1], stations[i*3+2]#, stations[i*3+3], stations[i*3+4], stations[i*3+5], stations[i*3+6]
        st = map(int, st)
        el = elevations[i*3], elevations[i*3+1], elevations[i*3+2]#, elevations[i*3+3], elevations[i*3+4], elevations[i*3+5], elevations[i*3+6]
        plt.plot(st,el)
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = int((max(st)-1)/2)
        plt.xticks(np.arange(min(st), max(st)+1 , spacing))

    elif widths[i] < 1000:
        plt.subplot(332)
        st = stations[i*3], stations[i*3+1], stations[i*3+2]#, stations[i*3+3], stations[i*3+4], stations[i*3+5], stations[i*3+6]
        st = map(int, st)
        el = elevations[i*3], elevations[i*3+1], elevations[i*3+2]#, elevations[i*3+3], elevations[i*3+4], elevations[i*3+5], elevations[i*3+6]
        plt.plot(st,el)
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = int((max(st)-1)/2)
        plt.xticks(np.arange(min(st), max(st)+1 , spacing))
        
    elif widths[i] < 1300:
        plt.subplot(333)
        st = stations[i*3], stations[i*3+1], stations[i*3+2]#, stations[i*3+3], stations[i*3+4], stations[i*3+5], stations[i*3+6]
        st = map(int, st)
        el = elevations[i*3], elevations[i*3+1], elevations[i*3+2]#, elevations[i*3+3], elevations[i*3+4], elevations[i*3+5], elevations[i*3+6]
        plt.plot(st,el)        
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = int((max(st)-1)/2)
        plt.xticks(np.arange(min(st), max(st)+1 , spacing))
                
    elif widths[i] < 1600:
        plt.subplot(334)
        st = stations[i*3], stations[i*3+1], stations[i*3+2]#, stations[i*3+3], stations[i*3+4], stations[i*3+5], stations[i*3+6]
        st = map(int, st)
        el = elevations[i*3], elevations[i*3+1], elevations[i*3+2]#, elevations[i*3+3], elevations[i*3+4], elevations[i*3+5], elevations[i*3+6]
        plt.plot(st,el) 
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = int((max(st)-1)/2)
        plt.xticks(np.arange(min(st), max(st)+1 , spacing))
                
    elif widths[i] < 2500:
        plt.subplot(335)
        st = stations[i*3], stations[i*3+1], stations[i*3+2]#, stations[i*3+3], stations[i*3+4], stations[i*3+5], stations[i*3+6]
        st = map(int, st)
        el = elevations[i*3], elevations[i*3+1], elevations[i*3+2]#, elevations[i*3+3], elevations[i*3+4], elevations[i*3+5], elevations[i*3+6]
        plt.plot(st,el)         
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = int((max(st)-1)/2)
        plt.xticks(np.arange(min(st), max(st)+1 , spacing))
                
    elif widths[i] < 3500:
        plt.subplot(336)
        st = stations[i*3], stations[i*3+1], stations[i*3+2]#, stations[i*3+3], stations[i*3+4], stations[i*3+5], stations[i*3+6]
        st = map(int, st)
        el = elevations[i*3], elevations[i*3+1], elevations[i*3+2]#, elevations[i*3+3], elevations[i*3+4], elevations[i*3+5], elevations[i*3+6]
        plt.plot(st,el)  
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = int((max(st)-1)/2)
        plt.xticks(np.arange(min(st), max(st)+1 , spacing))
                
    elif widths[i] < 7000:
        plt.subplot(337)
        st = stations[i*3], stations[i*3+1], stations[i*3+2]#, stations[i*3+3], stations[i*3+4], stations[i*3+5], stations[i*3+6]
        st = map(int, st)
        el = elevations[i*3], elevations[i*3+1], elevations[i*3+2]#, elevations[i*3+3], elevations[i*3+4], elevations[i*3+5], elevations[i*3+6]
        plt.plot(st,el) 
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = int((max(st)-1)/2)
        plt.xticks(np.arange(min(st), max(st)+1 , spacing))
                
    elif widths[i] <9000: 
        plt.subplot(338)
        st = stations[i*3], stations[i*3+1], stations[i*3+2]#, stations[i*3+3], stations[i*3+4], stations[i*3+5], stations[i*3+6]
        st = map(int, st)
        el = elevations[i*3], elevations[i*3+1], elevations[i*3+2]#, elevations[i*3+3], elevations[i*3+4], elevations[i*3+5], elevations[i*3+6]
        plt.plot(st,el)  
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = int((max(st)-1)/2)
        plt.xticks(np.arange(min(st), max(st)+1 , spacing))
               
    else: 
        plt.subplot(339)
        st = stations[i*3], stations[i*3+1], stations[i*3+2]#, stations[i*3+3], stations[i*3+4], stations[i*3+5], stations[i*3+6]
        st = map(int, st)
        el = elevations[i*3], elevations[i*3+1], elevations[i*3+2]#, elevations[i*3+3], elevations[i*3+4], elevations[i*3+5], elevations[i*3+6]
        plt.plot(st,el)          
        plt.xlabel('Width in feet', size=25)
        plt.ylabel('Depth in feet', size=25)
        spacing = int((max(st)-1)/2)
        plt.xticks(np.arange(min(st), max(st)+1 , spacing))
                
        
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
#Other things
#(df['d_0s']>40) | (df['d_0s'] <50) | (df['d_4s'] > 50)
