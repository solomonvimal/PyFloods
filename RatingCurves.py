# -*- coding: utf-8 -*-
"""
Created on Tue May 26 18:55:39 2015
Extract Rating Curves from HEC-RAS models
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

RiverID = 1; ReachID = 1; ProfileNo = 1;
AvgVelID = 23; # Average Velocity
QTotalID = 9; # Total flow in cross section
MaxChDepthID = 4; # Max Channel Depth
AvgVelID = 23; # Average Velocity

os.chdir("C:\Users\solo\Dropbox\Python\HEC-RAS_Models\extracted")
projectfiles = glob.glob("*.prj")
RatingCurves = {}

for idx, ras_file in enumerate(projectfiles):
    print idx, ras_file
    RC.Project_Open('C:\Users\solo\Dropbox\Python\HEC-RAS_Models\extracted\\' + ras_file) 
    NumRS =  RC.Schematic_XSCount(); # Number of nodes HEC-RAS will populate: not sure -> verify this
    StrNodeType = "" #  XS node type
    StrRS = RC.Geometry_GetNodes(RiverID, ReachID)[3]; # Not in the book! - Or this looks different in the book - Pg. 36
    # Get flow profiles
    NoProfiles = RC.Output_GetProfiles()[0]
    ProfileNames = list(RC.Output_GetProfiles()[1:NoProfiles+1])[0]
    Velocity = [0]*NoProfiles;

    Avg_Vel = [0]*NumRS;
    #Flow, Depth, Velocity
    Avg_Vel = [0]*NumRS;
    QTotal = [0]*NumRS;
    MaxChDepth = [0]*NumRS; 
    outliers = []
    Depth = []
    Flow = []
    for i in range(NumRS):
        Avg_Vel[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, 1, AvgVelID)[0]
        if Avg_Vel[i] > 100:
            print int(i)
            outliers = np.append(outliers, i)  ### local  

    #NumRS = NumRS - len(outliers)
    # Create an empty column vector for each variable for the number of XS
    XS = [0]*NumRS;
    RatingCurve =  np.zeros(shape = (0,5));
    #To do: Add reach and river looping + condition for XS node "", etc.
    for i in range(NumRS): 
        if (i not in outliers): # for each cross section (XS)
            # print i
            XS[i] = int(float(StrRS[i]))
            # i - XS node number, 0 is upstreamsection for bridge, append zero to get the value and assign it to a row
        for p in range(1, NoProfiles+1): # For each flow profile, extract information from HEC-RAS files
            depth = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, MaxChDepthID)[0] # Maximum Channel Depth
            Depth.append(depth)
            flow = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, QTotalID)[0] # Total Flow                     
            Flow.append(flow)
            l=[ras_file[:-4],XS[i],ProfileNames[p-1],depth,flow]
            RatingCurve = np.vstack((RatingCurve, np.array(l).T))
        RatingCurves["RatingCurve_"+ras_file[0:-4]+"_"+str(XS[i])] = RatingCurve
        RatingCurve =  np.zeros(shape = (0,5));
   
                '''len(BigXS) - len(BigXSSet)
                #Remove outliers before the below piece of loop for P
                '''

pickle.dump(RatingCurves, open("RatingCurves.p", "wb"))  
os.chdir("C:\Users\solo\Dropbox\Python")

f = open("RatingCurves.p")
RatingCurves = pickle.load(f)