# -*- coding: utf-8 -*-
"""
Created on Tue May 26 19:20:11 2015
Entrenchment Ratio
@author: Solo
"""

import win32com.client
import inspect
import os
import numpy as np
import matplotlib.pyplot as plt
from numpy import matrix
import pickle 
import glob

# Import Controller as an object handle
RC4 = win32com.client.Dispatch("RAS41.HECRASCONTROLLER") # not case sensitive
RC = win32com.client.Dispatch("RAS500.HECRASCONTROLLER") # HEC-RAS Version 5 (Beta)

###############     Global Parameters/Variables: Code/ID for the output feature    ####################

RiverID = 1; ReachID = 1; ProfileNo = 1;
AvgVelID = 23; # Average Velocity
TopWidthID = 62;  # Pg 249 - Breaking the RAS Code
TopWidthLID = 63; # including ineffective flow areas (actual top width is available!)
TopWidthCID = 64;
TopWidthRID = 65;
TopWidthID = 62;
MinSectionElevationID = 136;
ChannelStationLeftID = 158; # Channel Stations
ChannelStationRightID =  159;
ChannelCenterStationID = 161;
LOBElevID = 197;
ROBElevID = 198;
HydRadXSID = 208; # Hydarulic Radius = Area/Width
HydRadLID = 209;
HydRadCID = 210;
HydRadRID = 211;
MinChElStationID = 255;
LStationID = 263; # Left Station of XS
RStationID = 264; # Right Station of XS

QTotalID = 9; # Total flow in cross section
MaxChDepthID = 4; # Max Channel Depth
AvgVelID = 23; # Average Velocity


###############################################################################


# Set working directory to where the HEC-RAS files are located:
os.getcwd()
# os.chdir("C:\Users\solo\Dropbox\Python\HEC-RAS_Models")  ## This has to be adjusted to your directory of Dropbox

os.chdir("C:\Users\solo\Dropbox\Python\HEC-RAS_Models\extracted")
projectfiles = glob.glob("*.prj")

BigXSPointX = []
EntRatio = []
BigER  = []
BigER2  = []
BigXS  = []
EntrenchmentRatios = {}
XS_ERs = {}
RatingCurves = {}
for idx, ras_file in enumerate(projectfiles):
    print idx, ras_file
    RC.Project_Open('C:\Users\solo\Dropbox\Python\HEC-RAS_Models\extracted\\' + ras_file) 
    NumRS =  RC.Schematic_XSCount(); # Number of nodes HEC-RAS will populate: not sure -> verify this
    StrNodeType = "" ############  XS node type
    # StrRS[i] = RC.Geometry.NodeRS(RiverID,ReachID, i) # River Station as string
    StrRS = RC.Geometry_GetNodes(RiverID, ReachID)[3]; # Not in the book! - Or this looks different in the book - Pg. 36

    # Get flow profiles
    NoProfiles = RC.Output_GetProfiles()[0]
    ProfileNames = list(RC.Output_GetProfiles()[1:NoProfiles+1])[0]
    Entrenchment_Ratio1 = [0]*NoProfiles; # \sum_{i=1}^{n}{(ER_i \:DD_i})/ reach \:length
    Entrenchment_Ratio2 = [0]*NoProfiles; # {\frac{\sum_{i=1}^N{(Top Width_i})/ N}{\sum_{i=1}^N{(ChannelWidth_i })/ N}} = {\frac{\sum_{i=1}^N{(Top Width_i})}{\sum_{i=1}^N{(ChannelWidth_i })}}
    Entrenchment_Ratio3 = [0]*NoProfiles; # \frac{\sum_{i=1}^{n}{(EntrenchmentRatio_i })}{N}
    RatingCurve = [0]*NoProfiles;
    Flow = [0]*NoProfiles;
    Depth = [0]*NoProfiles;
    Velocity = [0]*NoProfiles;
    RatingCurve =  np.zeros(shape = (0,5));
    TopWidthP = [0]*NoProfiles;
    ChannelWidthP = [0]*NoProfiles;
    Avg_Vel = [0]*NumRS;
    ChannelStationRight = [0]*NumRS;
    ChannelStationLeft = [0]*NumRS;    
    #Flow, Depth, Velocity
    Avg_Vel = [0]*NumRS;
    QTotal = [0]*NumRS;
    MaxChDepth = [0]*NumRS; 
    
    outliers = []
    for i in range(NumRS):
        Avg_Vel[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, 1, AvgVelID)[0]
        if Avg_Vel[i] > 100:
            print int(i)
            outliers = np.append(outliers, i)  ### local  

    #NumRS = NumRS - len(outliers)
    # Create an empty column vector for each variable for the number of XS
    TopWidth = [0]*NumRS; 
    XS = [0]*NumRS;
    ChannelWidth = [0]*NumRS;
    DownstreamDistance = [0]*NumRS;
    ER = [0]*NumRS;
    ER2= [0]*NumRS;
    for p in range(1, NoProfiles+1): # For each flow profile, extract information from HEC-RAS files
        for i in range(NumRS): 
            if (i not in outliers): # for each cross section (XS)
                # print i
                XS[i] = int(float(StrRS[i]))
                # i - XS node number, 0 is upstreamsection for bridge, append zero to get the value and assign it to a row
                Avg_Vel[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, AvgVelID)[0] # p=3 (profile number) - hard coded in code Pg: 36
                MaxChDepth[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, MaxChDepthID)[0] # Maximum Channel Depth
                QTotal[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, QTotalID)[0] # Total Flow 
                TopWidth [i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, TopWidthID)[0] # Top Width
                ChannelStationRight[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, ChannelStationRightID)[0] # R.B.S of Channel
                ChannelStationLeft[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, ChannelStationLeftID)[0] # R.B.S of Channel
                ChannelWidth[i] = ChannelStationRight[i] - ChannelStationLeft[i] 
                
                if (i == 0): # Get downstream distance
                    DownstreamDistance[i] = 0 
                else:
                    DownstreamDistance[i]= (int(float(StrRS[i-1])) - int(float(StrRS[i])))
     
                # ENTRENCHMENT RATIO - vertical containment of a river
                # The width of the floodprone area is divided by the bankfull width to determine the entrenchment ratio (ER).
                # -> on average ratio of width corresponding to twice bankfull depth and bankfull depth
    
                ER[i] = (TopWidth[i])*DownstreamDistance[i]/ ChannelWidth[i]    # Entrenchment ratio in each cross-section # removed 
                ER2[i] = TopWidth[i]/ChannelWidth[i]
                l=[ras_file,XS[i],ProfileNames[p-1],MaxChDepth[i],QTotal[i]]
                RatingCurve = np.vstack((RatingCurve, np.array(l).T))
                for XS[i] in RatingCurve (RatingCurves["RatingCurve_"+ras_file[0:-4]+"_"+str(XS[i])] = RatingCurve)
                BigER2.append(ER2[i])
                BigXS.append(XS[i])
                BigXSSet = set(BigXS)
                
                '''len(BigXS) - len(BigXSSet)
                #Remove outliers before the below piece of loop for P
                '''
        TopWidthP[p-1] = np.average(TopWidth)
        ChannelWidthP[p-1] = np.average(ChannelWidth)
        Entrenchment_Ratio1[p-1] = np.sum(ER)/(XS[0]-XS[NumRS-1])   ##??    # Entrenchment ratio in each XS*downstream distance / total distance
        Entrenchment_Ratio2[p-1] = np.average(TopWidth)/np.average(ChannelWidth) #?? Average TopWidth/Average ChannelWidth
        Entrenchment_Ratio3[p-1] = np.average(ER2)
        RatingCurves = np.array(zip(ProfileNames,))
        #XS_ERs[ras_file[0:-4]]= np.array(zip(XS,ER2))
        
    EntrenchmentRatio = np.array(zip(ProfileNames,Entrenchment_Ratio1,Entrenchment_Ratio2,Entrenchment_Ratio3))
    
    
    EntrenchmentRatios["EntrenchmentRatio_"+ras_file[0:-4]] = EntrenchmentRatio
    
import pickle, os
pickle.dump(EntrenchmentRatios, open("EntrenchmentRatios.p", "wb"))   

os.chdir("C:\Users\solo\Dropbox\Python")
f = open("EntrenchmentRatios.p")
EntrenchmentRatios = pickle.load(f)
