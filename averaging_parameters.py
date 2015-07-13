# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:17:17 2015
Reach Average Properties
@author: Solo
Script to create averaged cross-sections from a 2 files: 
1 has cross-section survey points with unique IDs (XSID) and the line file has  


The code can be extended to get hydraulic properties
"""
import os, sys
import time
import pandas as pd
import matplotlib.pyplot as plt
from pandas import *
import csv

# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 25 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
    

# Change to current working directory
os.chdir("C:\Users\Solo\Dropbox\NFIE Project\XSPoints_to_Midpoint")

# Import path to data
path_points = r"C:\Users\Solo\Dropbox\NFIE Project\\XSPoints_to_Midpoint\\testpoints.csv" 
path_lines = r"C:\Users\Solo\Dropbox\NFIE Project\\XSPoints_to_Midpoint\\testlines.csv" 
#path_midpoints = r"C:\Users\Solo\Dropbox\NFIE Project\\XSPoints_to_Midpoint\\testmidpoints.csv" 

#path_points = r"C:\Users\Solo\Dropbox\NFIE Project\\XSPoints_to_Midpoint\\XSPointsHUC.txt" 
#path_lines = r"C:\Users\Solo\Dropbox\NFIE Project\\XSPoints_to_Midpoint\\XSLineHUC.txt" 
#path_midpoints = r"C:\Users\Solo\Dropbox\NFIE Project\\XSPoints_to_Midpoint\\testmidpoints.csv" 


lines = pd.read_csv(path_lines)
points = pd.read_csv(path_points)
#midpoints = pd.read_csv(path_midpoints)


#Subset for testing

lines = pd.read_csv(path_lines)
points = pd.read_csv(path_points)
#midpoints = pd.read_csv(path_midpoints)


# Create Data Frames
df_lines = pd.DataFrame(lines)
df_points = pd.DataFrame(points)
#df_midpoints = pd.DataFrame(midpoints)

# Orint the frame column names
df_lines.columns
df_points.columns
#df_midpoints.columns

line_xsids = list(df_lines['XSID'])
line_comids = list(df_lines['COMID'])
point_xsids = list(df_points['XSID'])
len(set(point_xsids)) # we lose 2 cross-sections in the set. 
point_stations = list(df_points['Station'])
point_elevations = list(df_points['Elevation'])
point_elevations = map(int, point_elevations) # use elevations as integers

#midpoint_comids = list(df_midpoints['COMID'])


xsid, station, elevation = [], [], []
s_0s, s_2s, s_4s, s_5s, s_6s, s_8s, s_10s = [], [], [], [], [], [], []; 
d_0s, d_2s, d_4s, d_5s, d_6s, d_8s, d_10s = [], [], [], [], [], [], []; 
Ws =[]
COMIDs = []
XSIDs = []
for i in range(len(point_xsids)-1):# leave the last point for simplicity
    time.sleep(0.000000000000000001)
    print "ha"
    update_progress((i+1)/float(len(point_xsids)))
    if int(point_xsids[i]) == int(point_xsids[i+1]) or point_xsids.index(int(point_xsids[len(point_xsids)-1])) == i+1: ###########
        xsid.append(point_xsids[i])
        station.append(int(float(point_stations[i].replace(",",""))))
        elevation.append(point_elevations[i])
    else:
        pass
        XSID=point_xsids[i-1]# as key for looking up in the lines table
        index_lowest = elevation.index(min(elevation))
        station[index_lowest]
        #if len(station[0:index_lowest])%2 ==0:
        d_0 = elevation[0] - elevation[index_lowest]
        d_2 = sum(elevation[0:index_lowest/2])/len(elevation[0:index_lowest/2]) - elevation[index_lowest]
        d_4 = sum(elevation[(index_lowest/2):index_lowest])/len(elevation[(index_lowest/2):index_lowest]) - elevation[index_lowest]
        d_5 = elevation[index_lowest] - elevation[index_lowest]
        second_half = elevation[index_lowest:len(elevation)]
        l2 = len(second_half)
        try:
            d_6 = sum(second_half[0:l2/2])/(l2/2) - elevation[index_lowest]
            d_8 = sum(second_half[l2/2:])/(l2/2) - elevation[index_lowest]         
        except:
            pass
        d_10 = elevation[-1] - elevation[index_lowest]
        w = station[-1] - station[0]
        s_0 = int(w-station[-1])
        s_2 = int(s_0 + (0.2*w))    
        s_4 = int(s_0 + (0.4*w))
        s_5 = int(station[index_lowest])
        s_6 = int(s_0 + 0.6*w)
        s_8 = int(s_0+0.8*w)
        s_10 = int(station[-1])
        s_0s.append(s_0); s_2s.append(s_2);s_4s.append(s_4);s_5s.append(s_5);s_6s.append(s_6);s_8s.append(s_8);s_10s.append(s_10);
        d_0s.append(d_0); d_2s.append(d_2);d_4s.append(d_4);d_5s.append(d_5);d_6s.append(d_6);d_8s.append(d_8);d_10s.append(d_10);
        Ws.append(w)
        #if int(point_xsids[i]) == int(point_xsids[i+1]) or point_xsids.index(int(point_xsids[len(point_xsids)-1])) == i+1:
        ##############
        comid_index = line_xsids.index(XSID) # Check these two lines
        COMIDs.append(int(line_comids[comid_index].replace(",",""))) # Check these two lines         
        XSIDs.append(int(XSID))
        s_0, s_2, s_4, s_5, s_6, s_8, s_10 = [], [], [], [], [], [], []
        xsid, station, elevation, w = [], [], [], []

table = zip(COMIDs, Ws, s_0s, s_2s, s_4s, s_5s, s_6s, s_8s, s_10s, d_0s, d_2s, d_4s, d_5s, d_6s, d_8s, d_10s)
columns = ('COMIDs','Ws', 's_0s', 's_2s', 's_4s', 's_5s', 's_6s', 's_8s', 's_10s', 'd_0s', 'd_2s', 'd_4s', 'd_5s', 'd_6s', 'd_8s', 'd_10s')
df = pd.DataFrame(table, index = COMIDs, columns = columns)
averaged_df = df.groupby('COMIDs').mean().dropna()

#stacked = averaged_df.stack()
#set_comIDS = set(COMIDs)
## Melt Pandas! 
#df1_melt = pd.melt(df, id_vars='COMIDs').dropna()
## Pandas Stack!!
#df_stack = df.stack()
#pivot  = df.pivot(index=0, columns=1, values=2)
#pd.pivot_table(df, values= columns, index=['COMID'], columns=['C'])
#
#len(set(XSIDs))
#        
## Plots
#plt.figure(1)
#plt.plot(station,elevation)
#plt.figure(2)
#plt.plot([s_0,s_2,s_4,s_5,s_6,s_8,s_10],[d_0,d_2,d_4,d_5,d_6,d_8,d_10])
        
# write to CSV
file_name = 'XS_COMID_averaged3.csv'
df.to_csv(file_name, sep=',', encoding='utf-8')




# fit a line to the cross section (polyfit) to make it smooth and symmetrical

df = averaged_df
df = df.values.tolist()
for z in list([2,3,4,5,6,7]):
    print z
    for row in df: # row (each COMID) has a average width, 7 stations and 7 elevations
        print row
        width = row[0]    
        stations = row[1:8]
        elevations = row[8:15]
        x = np.array(stations)
        y = np.array(elevations)
        z = np.polyfit(x,y,5)
        p = np.poly1d(z)
        p(0.5)
        fit_stations = []
        fit_elevations = []  
        for i in range(int(max(stations))):
            plt.figure(1)    
            #plt.plot(int(i), p(int(i)),'o') 
            fit_stations.append(int(i))
            fit_elevations.append(p(int(i)))
            for y in range(int(max(elevations))):
                print y
                
    plt.plot(fit_stations, fit_elevations, 'r-')
    plt.plot(stations, elevations,'r-')


# work on the part below
def get_depth_width_curve(stations, elevations)

    return table_DW
    

            
            
            