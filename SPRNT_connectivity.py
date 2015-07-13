# -*- coding: utf-8 -*-
"""
Created on Tue Jul 07 09:46:45 2015

@author: Solo
This script takes the HEC-RAS dataframe, reorders the columns 
to SPRNT (CSV) file format that pre-processing needs. 

The reordered dataframe (of 2028 XSs) is then merged (overwritten) 
on the cross-sections extracted from DEM (~5000 XSs)

The HEC-RAS and LiDAR derived cross-sections are plotted in 9subplots per plot
"""
#########
file_name = r'connectivity_file_merged'
############
import os
from numpy import genfromtxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

HEC_df = pd.read_csv("C:\\Users\\Solo\\Dropbox\\NFIE Project\\XSPoints_to_Midpoint\\XS_COMID_averaged.csv")

connectivity_data_location = "C:\Users\Solo\\Dropbox\\Justin\\New_Connect_SPRINT.csv"
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
connectivity_df["COMIDs"]= map(int,connectivity_df["COMIDs"])
connectivity_df["FromNode"]= map(int,connectivity_df["FromNode"])
connectivity_df["ToNode"]= map(int,connectivity_df["ToNode"])

connectivity_df_not_overwritten = connectivity_df.copy() ##### COPYING IS IMPORTANT!!!!!!

HEC_RAS_comids = list(HEC_df2.index)

# manually select the NA values in CONN by sorting them and save it in a location and read it.
#manual_list = list(genfromtxt(r"C:\\Users\\Solo\\Dropbox\\NFIE Project\\XSPoints_to_Midpoint\\These_cross_sections_dont_have_data_from_DEM_NA", delimiter = '\t'))
#HEC_RAS_comids = list(set(HEC_RAS_comids) - set(manual_list))
#select the COMIDs in HEC that are not in connectivity file
x=[]
selected_comids = [x for x in HEC_RAS_comids if x in list(connectivity_df.index)]

# Select data overwriting region in the two dataframes
# WORK ON THE PART BELOW

conn = connectivity_df.ix[selected_comids,"s_0s":"d_10s"] 
hec = HEC_df2.loc[selected_comids,"s_0s":"d_10s"]
hec=hec*0.3048

# Overwrite the selected L.H.S columns XSs with HEC-RAS XSs
connectivity_df.loc[selected_comids,"s_0s":"d_10s"] = hec

#
connectivity_df_overwritten = connectivity_df.copy() # .copy() is important

# Check for a few selected columns before and after the merge was made
# Selected COMID
check_comid = 21676030 #21684220
HEC_df2.ix[check_comid,"s_0s":"d_10s"]
connectivity_df.ix[check_comid,"s_0s":"d_10s"]
#Before merging - should be different
connectivity_df_not_overwritten.ix[check_comid,"s_0s":"d_10s"]

import os
os.chdir('C:\\Users\\Solo\\Dropbox\\NFIE')
# Write to CSV
connectivity_df_overwritten.to_csv(file_name+'converted', header=False, index=False,sep='\t', encoding='utf-8')


# Plots for comparison of cross-sections
stations = map(int,hec.ix[:,['s_0s','s_2s','s_4s','s_5s','s_6s','s_8s','s_10s']].stack())
elevations = map(int,hec.ix[:,['d_0s','d_2s','d_4s','d_5s','d_6s','d_8s','d_10s']].stack())
stations2 = map(int,conn.ix[:,['s_0s','s_2s','s_4s','s_5s','s_6s','s_8s','s_10s']].stack())
elevations2 = map(int,conn.ix[:,['d_0s','d_2s','d_4s','d_5s','d_6s','d_8s','d_10s']].stack())

for i in range(1,90):  #len(stations)/7):
    st = stations[i*7], stations[i*7+1], stations[i*7+2], stations[i*7+3], stations[i*7+4], stations[i*7+5], stations[i*7+6]
    st = map(int, st)
    el = elevations[i*7], elevations[i*7+1], elevations[i*7+2], elevations[i*7+3], elevations[i*7+4], elevations[i*7+5], elevations[i*7+6]
    st2 = stations2[i*7], stations2[i*7+1], stations2[i*7+2], stations2[i*7+3], stations2[i*7+4], stations2[i*7+5], stations2[i*7+6]
    st2 = map(int, st2)
    el2 = elevations2[i*7], elevations2[i*7+1], elevations2[i*7+2], elevations2[i*7+3], elevations2[i*7+4], elevations2[i*7+5], elevations2[i*7+6]
    if i/9 != 0:
        if i < 9:
           p = i 
        else:
            p = i%9
            f = i/9
        plt.figure(f)
        plt.subplot(int(str('33')+str(p)))
        plt.plot(st,el)
        plt.plot(st2,el2)
        #plt.xlabel('Stations', size=25)
        #plt.ylabel('Depth in feet', size=25)
        #spacing = max(st)/2
        #plt.xticks(np.arange(min(st), max(st)+1, spacing))
    else:
        pass