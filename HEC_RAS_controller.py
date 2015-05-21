
# -*- coding: utf-8 -*-

"""
Script to use HEC-RAS Controller on existing HEC-RAS project files (with some example usage)
Created on Wed Mar 18 09:35:42 2015
@author: Solomon Vimal

What is Component Object Model for HEC-RAS - RASController?
COM/ActiveX in Python - http://stackoverflow.com/questions/1065844/what-can-you-do-with-com-activex-in-python

Instructions for getting RAS-Controller Running from Python:

Step 1: Install pywin32 module from Source forge
http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/ 
For Windows x32: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win32-py2.7.exe/download
For Windows x64: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20
219/pywin32-219.win-amd64-py2.7.exe/download

Step 2: Run makepy utilities
- Go to the path where Python modules are sitting:
It may look like this -> C:\Users\solo\Anaconda\Lib\site-packages\win32com\client
or C:\Python27\ArcGIS10.2\Lib\site-packages\win32com\client
or C:\Python27\Lib\site-packages\win32com\client
- Open command line at the above (^) path and run $: python makepy.py
select HECRAS River Analysis System (1.1) from the pop-up window
this will build definitions and import modules of RAS-Controller for use

"""
# Extract the model zip files to a specified folder location
import zipfile
ras_folder = 'C:\Users\Solo\Dropbox\Python\HEC-RAS_Models'
#ras_file = 'C:/Users/solo/Dropbox/Python/Solomon_Xing_Min/dtl_tuckasegee_rvr.prj'; # project name ########## CHANGE 1  - file name ###############
outpath = 'C:\Users\Solo\Dropbox\Python\HEC-RAS_Models\extracted'

# Extract all files to outpath
for filename in glob.glob("*.zip"):
    with zipfile.ZipFile(filename, "r") as z:
        z.extractall(outpath)

#def GetEntrenchmentRatio():
# Import modules and HEC-RAS Controller
import win32com.client
import inspect
import os
import numpy as np
import matplotlib.pyplot as plt
from numpy import matrix
import re
import glob

# Import Controller as an object handle
RC4 = win32com.client.Dispatch("RAS41.HECRASCONTROLLER") # not case sensitive
RC = win32com.client.Dispatch("RAS500.HECRASCONTROLLER") # HEC-RAS Version 5 (Beta)

# Check out the methods in the controller
# inspect.getmembers(RC, predicate=inspect.ismethod)
#ov = RC.Output_Variables()
#RC.ShowRAS()
# RAS Geometry Files
#RC.Schematic_ReachCount()
#RC.Schematic_ReachPointCount()
#RC.Schematic_XSCount()
#XSPointCount = RC.Schematic_XSPointCount()
# h.Schematic_XSPoints()
# h.Geometry_GetNode()
# RC.ShowRas()#To see the HEC-RAS application
# Sub routine:GetWSEandVelocity()
# Retrieving Output Procedures: Pg 41, 42, 43

###############     Global Parameters/Variables: Code/ID for the output feature    ####################
################   this bit can be converted into a textfile with variable code   #####################
#################   then write a function to make the code shorter (for later)   ######################

RiverID = 1;
ReachID = 1;
ProfileNo = 1;
WSElevID = 2; # Water surface elevation
EGElevID = 3; # Energy Gradeline for given WSElev
MaxChDepthID = 4; # Max Channel Depth
MinChElevID = 5; # Min Channel Elevation
QLeftID = 6; # Flow in left overbank
QChannelID = 7; # Flow in main channel
QRightID = 8; # Flow in right overbank
QTotalID = 9; # Total flow in cross section
FlowAreaID = 10; # Flow Area (in each node)
FlowAreaLBankID = 11;
FlowAreaChannelID = 12;
FlowAreaRBankID = 13;
WP_XSID = 14; # wetted perimeter total
WP_LID = 15;  # left over bank
WP_ChID = 16;
WP_RID = 17;
# Conveyance K = A^(5/3)/n*P^(2/3) - available 18-21
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

###############################################################################


# Set working directory to where the HEC-RAS files are located:
os.getcwd()
os.chdir("C:\Users\solo\Dropbox\Python\HEC-RAS_Models")  ## This has to be adjusted to your directory of Dropbox

thelist = dir(RC)

os.chdir("C:\Users\solo\Dropbox\Python\HEC-RAS_Models\extracted")
geometryfiles = glob.glob("*.g01")
projectfiles = glob.glob("*.prj")

BigXSPointX = []
EntRatio = []
BigER  = []
BigER2  = []
BigXS  = []
for idx, ras_file in enumerate(projectfiles):
    #print idx, ras_file
    RC.Project_Open('C:\Users\solo\Dropbox\Python\HEC-RAS_Models\extracted\\' + ras_file) 
    # first time use -> pop up for accepting terms
    # Get number of cross-sections
    NumRS =  RC.Schematic_XSCount(); # Number of nodes HEC-RAS will populate: not sure -> verify this
    StrNodeType = "" ############  XS node type
    # StrRS[i] = RC.Geometry.NodeRS(RiverID,ReachID, i) # River Station as string
    StrRS = RC.Geometry_GetNodes(RiverID, ReachID)[3]; # Not in the book! - Or this looks different in the book - Pg. 36
    # Loop over all the XS and pull out the values for each variable
    #RSID[i] = RC.Geometry_GetNodes()
    # Usage of the Node_Output function: 
    # RC.Output.NodeOutput(RiverID, ReachID, UPDNBoolean (not needed for XS), profile no, Variable ID))

    # Get flow profiles
    NoProfiles = RC.Output_GetProfiles()[0]
    ProfileNames = RC.Output_GetProfiles()[1:NoProfiles-1]
    Entrenchment_Ratio1 = [0]*NoProfiles; 
    Entrenchment_Ratio2 = [0]*NoProfiles; 
    Entrenchment_Ratio3 = [0]*NoProfiles; 
    TopWidthP = [0]*NoProfiles;
    ChannelWidthP = [0]*NoProfiles;
    # matching = ['100' for s in ProfileNames if "100-YR" in s]
    Avg_Vel = [0]*NumRS;

    outliers = []
    for i in range(NumRS):
        Avg_Vel[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, 1, AvgVelID)[0]
        if Avg_Vel[i] > 100:
            print int(i)
            outliers = np.append(outliers, i)  ### local  

    #NumRS = NumRS - len(outliers)
    # Create an empty column vector for each variable for the number of XS
    WSElev = [0]*NumRS;
    Avg_Vel = [0]*NumRS;
    MaxChDepth = [0]*NumRS;
    MinChElev = [0]*NumRS;
    TopWidth = [0]*NumRS;
    LStation = [0]*NumRS;
    RStation = [0]*NumRS;
    XS = [0]*NumRS;
    ChannelStationRight = [0]*NumRS;
    ChannelStationLeft = [0]*NumRS;
    LOBElev = [0]*NumRS;
    ROBElev = [0]*NumRS;
    LowBankHeight = [0]*NumRS;
    IncisionRatio = [0]*NumRS;
    MinChElStation = [0]*NumRS;
    ChannelWidth = [0]*NumRS;
    MinSectionElevation = [0]*NumRS;
    DownstreamDistance = [0]*NumRS;
    ER = [0]*NumRS;
    ER2= [0]*NumRS;
    QLeft = [0]*NumRS;
    QChannel = [0]*NumRS;
    QRight = [0]*NumRS;
    QTotal = [0]*NumRS;
    TopWidthP = [0]*NoProfiles
    ChannelWidthP = [0]*NoProfiles

    '''    
        ## Remove outliers!! why do they exist?!
        # Identify Outliers using velocity > 100
        bla = zip(XS, WSElev, Avg_Vel, MaxChDepth,  MinChElev, MinChElev, TopWidth,LStation,RStation,\
        ChannelStationRight, ChannelStationLeft,LOBElev, ROBElev, MinChElStation, MinSectionElevation, ChannelWidth)
        bla = np.array(bla)
    
    Zip unpacking?
        #blablabla = ('XS', 'WSElev', 'Avg_Vel', 'MaxChDepth', 'MinChElev', 'MinChElev', 'TopWidth','LStation','RStation',\
        #    'ChannelStationRight', 'ChannelStationLeft','LOBElev','ROBElev','MinChElStation', 'MinSectionElevation', 'ChannelWidth')    
        # Unpack blabla manually and move on (because long LHS for zip throws an error: too many values to unpack - could not find a quick fix )
    
        #Take tranpose of balabla 
        blabla = blabla.T;     XS = blabla[0]
        WSElev = blabla[1];     Avg_Vel = blabla[2]
        MaxChDepth = blabla[3];     MinChElev  = blabla[4]
        MinChElev  = blabla[5];     TopWidth = blabla[6]
        LStation = blabla[7];     RStation = blabla[8]
        ChannelStationRight = blabla[9];     ChannelStationLeft = blabla[10]
        LOBElev = blabla[11];   ROBElev = blabla[12]
        MinChElStation = blabla[13] ;     MinSectionElevation = blabla[14]
        ChannelWidth  = blabla[15];     np.average(blabla)
    '''

    # Delete the outliers in all the variables (bla) to get blabla
    # blabla = np.delete(bla, [outliers], axis=0) # axis=0 refers to rows, axis =1 refers to columns   - NOT NEEDED (loop changed below!)

    # NumRS = NumRS - len(outliers)  

    # ZE LOOP
    for p in range(1, NoProfiles+1): # For each flow profile, extract information from HEC-RAS files
        for i in range(NumRS): 
            if (i not in outliers): # for each cross section (XS)
                # print i
                XS[i] = int(float(StrRS[i]))
                WSElev[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, WSElevID)[0]
                # i - XS node number, 0 is upstreamsection for bridge, append zero to get the value and assign it to a row
                Avg_Vel[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, AvgVelID)[0] # p=3 (profile number) - hard coded in code Pg: 36
                MaxChDepth[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, MaxChDepthID)[0] # Maximum Channel Depth
                MinChElev[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, MinChElevID)[0] # Minimum Channel Elevation
                QTotal[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, QTotalID)[0] # Total Flow 
                TopWidth [i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, TopWidthID)[0] # Top Width
                LStation [i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, LStationID)[0] # Left Bank Station of XS
                RStation [i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, RStationID)[0] # Right Bank Station of XS
                ChannelStationRight[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, ChannelStationRightID)[0] # R.B.S of Channel
                ChannelStationLeft[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, ChannelStationLeftID)[0] # R.B.S of Channel
                LOBElev[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, LOBElevID)[0] # LOB of of XS
                ROBElev[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, ROBElevID)[0] # ROB of XS
                MinChElStation[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, MinChElStationID)[0] # Station of Min Channel Elevation
                MinSectionElevation[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, MinSectionElevationID)[0] # Min Section Elevation
                ChannelWidth[i] = ChannelStationRight[i] - ChannelStationLeft[i] 
                if (i == 0): # Get downstream distance
                    DownstreamDistance[i] = 0 
                else:
                    DownstreamDistance[i]= (int(float(StrRS[i-1])) - int(float(StrRS[i])))
     
                # ENTRENCHMENT RATIO - vertical containment of a river
                # The width of the floodprone area is divided by the bankfull width to determine the entrenchment ratio (ER).
                # -> on average ratio of width corresponding to twice bankfull depth and bankfull depth
    
                ER[i] = (TopWidth[i]*DownstreamDistance[i])/ ChannelWidth[i]    # Entrenchment ratio in each cross-section
                ER2[i] = TopWidth[i]/ChannelWidth[i]
                BigER.append(ER[i])
                BigER2.append(ER2[i])
                BigXS.append(XS[i])
    BigXSSet = set(BigXS)
    len(BigXS) - len(BigXSSet)
        #Remove outliers before the below piece of loop for P

        TopWidthP[p-1] = np.average(TopWidth)
        ChannelWidthP[p-1] = np.average(ChannelWidth)
        Entrenchment_Ratio1[p-1] = np.average(ER)/(XS[0]-XS[NumRS-1])            # Entrenchment ratio in each XS*downstream distance / total distance
        Entrenchment_Ratio2[p-1] = np.average(TopWidth)/np.average(ChannelWidth) # Average TopWidth/Average ChannelWidth
        Entrenchment_Ratio3[p-1] = np.average(ER2)                               # Average of all XS Entrenchment ration 

    EntrenchmentRatio = np.array(zip(Entrenchment_Ratio1,Entrenchment_Ratio2,Entrenchment_Ratio3))


    #################    XS co-ordinate points extraction   #######################

    # Get number of cross-section cutline points
    AllXSPointCount = RC.Schematic_XSPointCount()

    # Predefine size of arguments with no values in them -> values will be populated in L.H.S
    RSName = [0]*NumRS;
    ReachIndex = [0]*NumRS;
    XSStartIndex = [0]*NumRS;
    XSPointCount = [0]*NumRS;
    XSPointX = [0]*AllXSPointCount;
    XSPointY = [0]*AllXSPointCount;

    # THE MOST USEFUL RASController function
    RSName,ReachIndex,XSStartIndex,XSPointCount,XSPointX,XSPointY = \
    RC.Schematic_XSPoints(RSName,ReachIndex, XSStartIndex, XSPointCount, XSPointX, XSPointY)

    #BigXSPointX.append(max(XSPointX))    

    # Plot the river schematic XS points
    plt.figure(idx); ax1 = plt.subplot(111)
    ax1.plot(XSPointX,XSPointY, 'ro', color = 'R', label='XY coordinate points')
    plt.ylabel('Latitude (in decimal degrees)'); plt.xlabel('Longitude (in decimal degrees)')
#    plt.xlim(760000,780000); plt.ylim(570000,590000)
    ax1.legend(bbox_to_anchor=(1, 1)); plt.title('XY Coordinate points'); plt.grid()  

    # Cross section profile plots
    Left  = zip(ChannelStationLeft, LOBElev)            
    Right = zip(ChannelStationRight, ROBElev)
    Center = zip(MinChElStation, MinChElev)

    plt.figure(2)
    plt.plot(Left[i][0], Left[i][1],'ro') # Left Station and elevation
    plt.plot(Right[i][0], Right[i][1],'ro') # Right Station and elevation
    plt.plot(Center[i][0], Center[i][0], 'ro') # min Station and elevation

    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure(6)
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(XS)):
        plt.scatter(Left[i][0], XS[i], zs=Left[i][1], zdir = u'z')
        plt.scatter(Right[i][0], XS[i], zs=Right[i][1], zdir = u'z')
        plt.xlim(0,1000); plt.ylim(245367,275744); #plt.zlim(0,2000)
    # HEC-RAS Plots
    RC.plotXS(1,1,XS[i])    
    RC.QuitRAS()

    ###############################################################################

    # Difference in Elevation between left and right banks
        
    # INCISION RATIO: The low bank height is divided by bankfull maximum depth to determine the incision ratio for the channel (Step 2.8).
    # Pg 25: http://tinyurl.com/m476mrm

    # Calculated as the lower-bank-height/Max_Channel_Depth
    Diff =  matrix(LOBElev)- matrix(ROBElev)        
    for j in range(NumRS):
        if float(Diff.transpose()[j]) >= 0:
            LowBankHeight[j] = ROBElev[j] - MinChElev[j]
        else:
            LowBankHeight[j] = LOBElev[j] - MinChElev[j]    
            IncisionRatio[j] = LowBankHeight[j]/MaxChDepth[j] 
            IR = np.average(IncisionRatio)  


    # Station from the left to right

    StationDiff = np.subtract(RStation,LStation)
    LStation [i] 
    ChannelStationLeft[i] 
    MinChElStation[i]
    ChannelStationRight[i]
    RStation [i]
    ChannelWidth[i]
    TopWidth[i] # this depends on flow profile
    # Elevations from left to right
    LOBElev[i]
    MinChElev[i]
    #MinSectionElevation[i]
    ROBElev[i]

    # FLOODPRONE WIDTH

    #########################################        Ze Plots         ##################################################
    #XS = np.array(StrRS);
    ################## FIGURE 1  #####################  WATER SURFACE ELEVATION and MINIMUM CHANNEL ELEVATION
    plt.figure(idx+1)

    ax1 = plt.subplot(511)
    ax1.plot(XS, WSElev, 'ro', color = 'R', label='Water Surface Elevation')
    ax1.plot(XS, MinChElev, 'ro', color = 'G', label='Minimum Channel Elevation')
    #plt.xlabel('XS number'), 
    xticklabels = ax1.get_xticklabels()#+ax2.get_xticklabels()+ax3.get_xticklabels()
    plt.setp(xticklabels, visible=False)
    plt.ylabel('Elevation (Feet)')
    ax1.legend(bbox_to_anchor=(0.9, 0.3))
    plt.ylim((2000,2305))
    plt.title('Min Channel & Water Surface Elevations, Max Channel Depth and Top Width'); plt.grid()
    
    
    ax3 = plt.subplot(512, sharex = ax1)
    ax3.plot(XS, MaxChDepth, 'ro', color = 'B', label = 'Maximum Channel Depth') # Same as Depth = list(np.array(WSElev)-np.array(MinChElev))
    plt.ylabel('Depth (Feet)'); 
    ax3.legend(bbox_to_anchor=(1, 1))
    plt.ylim((0,20))
    xticklabels2 = ax3.get_xticklabels()#+ax2.get_xticklabels()+ax3.get_xticklabels()
    plt.setp(xticklabels2, visible=False); plt.grid()
    
    ax4 = plt.subplot(513, sharex = ax1)
    ax4.plot(XS, TopWidth, 'ro', color = 'Y', label = 'Top Width')
    plt.ylabel('Width (Feet)'); 
    ax4.legend(bbox_to_anchor=(1, 1))
    plt.ylim((0,400))
    plt.grid()
    plt.setp(ax4.get_xticklabels(), visible=False)
    
    ax2 = plt.subplot(515, sharex = ax1)
    ax2.plot(XS, MinChElev, 'ro', label='Minimum Channel Elevation Ouliers')
    plt.ylabel('Elevation (Feet)')
    ax2.legend(bbox_to_anchor=(0.9, 0.6))
    plt.grid()
    #plt.setp(ax2.get_xticklabels(), visible=False)
    plt.xlabel('Cross Section ID')
    
    
    ax5 = plt.subplot(514, sharex = ax1)
    ax5.plot(XS, Avg_Vel, 'ro', label='Average Velocity')
    plt.ylim((0,20))
    plt.ylabel('Average Velocity (Ft/s)')
    ax5.legend(bbox_to_anchor=(0.9, 0.3))
    plt.setp(ax5.get_xticklabels(), visible=False)
    plt.grid()
    
    
    ##### FIGURE 2  ########
    plt.figure(2)
    
    # Stations: 
    ax1 = plt.subplot(211)
    ax1.plot(XS, RStation, 'ro', label='RStation')
    plt.ylim((0,2000))
    plt.ylabel('Staion Length (Ft/s)')
    ax1.legend(bbox_to_anchor=(0.9, 0.3))
    #plt.setp(ax5.get_xticklabels(), visible=False)
    plt.grid()
    ax2 = plt.subplot(212, sharex = ax1)
    ax2.plot(XS, LStation, 'ro', label='LStation')
    plt.ylim((0,2000))
    plt.ylabel('Station Length (Feet)')
    ax2.legend(bbox_to_anchor=(0.9, 0.3))
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.grid()
    
    
    ######  FIGURE 3  ###############
    plt.figure(3)
    ax1 = plt.subplot(311)
    ax1.plot(XS, LOBElev, 'ro', label='LOBElev')
    plt.ylim((2000,2300))
    plt.ylabel('Elevation (Feet)')
    ax1.legend(bbox_to_anchor=(0.9, 0.3))
    #plt.setp(ax5.get_xticklabels(), visible=False)
    plt.grid()
    ax2 = plt.subplot(312, sharex = ax1)
    ax2.plot(XS, ROBElev, 'ro', label='ROBElev')
    plt.ylim((2000,2300))
    plt.ylabel('Elevation (Feet)')
    ax2.legend(bbox_to_anchor=(0.9, 0.3))
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.grid()
    
    
    ax3 = plt.subplot(313, sharex = ax1)
    ax3.plot(XS,Diff.transpose(), 'ro', label='Difference in elevation between left and right banks')
    #plt.ylim((0,12))
    plt.ylabel('Elevation (Feet)')
    ax3.legend(bbox_to_anchor=(0.9, 0.3))
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.grid()
    
    
    ##################        FIGURE 4          #####################
    
    plt.subplot(313)                                                            ### Channel Station Right
    plt.plot(XS, ChannelStationRight, 'ro')
    plt.ylabel('Channel Station Right')
    plt.ylim((0,500))
    title = str(ReachID)
    plt.suptitle('Plots of Channel and XS Station', size=20)
    
    plt.figure(1)
    plt.subplot(313)                                                            ### XS Station Right
    ax = plt.subplot(122)
    ax.plot(XS, RStation, 'ro', label='Right Station', color='green')
    ax.legend(bbox_to_anchor=(0.8, 0.8))
    plt.ylim((0,2000))
    plt.title('Right Station')
    
    ###########################    other plots   #############################
    
    
       plt.figure(4)
       plt.subplot(111)                                                            ### AVERAGE VELOCITY
       plt.plot(StationDiff,TopWidth, 'ro')
       plt.title('Top Width & Diff between Stations')
       plt.xlabel(' ? ')
       plt.ylabel('feet')
       plt.ylim((0,2000))
       #plt.savefig('AverageVelocity.png')
    
    
       plt.figure(3)
       plt.subplot(111)                                                            ### AVERAGE VELOCITY
       plt.plot(Avg_Vel, 'ro')
       plt.title('Average Velocity')
       plt.xlabel('XS number')
       plt.ylabel('velocity (ft?/s)')
       plt.ylim((0,20))
       #plt.savefig('AverageVelocity.png')
    
    
    from pylab import *
    x = np.linspace(0.4 * np.pi, 100)
    plot(x, np.sin(x))
    show()
    
    
    
    # RC.QuitRAS() # - Pg 39 - read again



######################## EXPERIMENTS  #########################################

 n  = 1
x = (float('nan'),) #*(n + 1)  # (n + 1) Adjust to 0-based indexing
y = (float('nan'),) #*(n + 1)  # (n + 1) Adjust to 0-based indexing

x = np.zeros(shape=(len(XS),1))
y = np.zeros(shape=(len(XS),1))


x = np.array([])
y = np.array([])
# Important function: 
RC.Geometery.NodeCutLine_Points(1,1,XS[1],x,y) ## attribute error!??!?!?!?!?!?! 




# what is this?
RC.Geometry.im_func.func_code.co_cellvars.count(1)



    
##################################################################################################################################
# CLOSE PROJECT AND RELEASE HANDLES ?
#  all interface handles to the server object must be released in order for the server process to terminate.


### Write a method to pick up all the 268 variables and plot them -> naming, plotting, plot extents, etc. has to be figured out


### Print stuff to text file

from __future__ import print_function
    if os.path.exists('C:/Users/solo/Dropbox/Python/ras500.txt'):
       print ("File exists")

    else:
        textfile = open("C:/Users/solo/Dropbox/Python/ras500_builtmethods.txt", 'w')
BuiltMethods = RC._builtMethods_;
for item in thelist5:
  textfile.write("%s \n" % item)

###############################   OPENING UP THE GEOMETRY FILE  ##############################################################

# - ESRI post - https://geonet.esri.com/thread/67987
# and GITHIB - https://gist.github.com/anonymous/df899701271a62ff4543#file-gistfile1-py
#Extract data from RAS Geometry files
#@skulk001
# Modified by Solomon Vimal
########################################################################
import os
import re
import time
import csv
from operator import floordiv

folderLocation = "C:\Users\solo\Dropbox\Python\HEC-RAS_Models\extracted\"
listSubFolders = os.listdir(folderLocation)
flowChangeLocationsTable = []
streamGeometry = {}
for subFolder in listSubFolders:
    subFolderPath = folderLocation + "\\" + subFolder
    if os.path.isdir(subFolderPath):
        listSubFolderFiles = os.listdir(subFolderPath)
        for file in listSubFolderFiles:
            #Geometry files in hecras have a ".g0*" extension, the code below filters to look for that geometry files only
            if file.find(".g01") != -1:
                print file #### to check if it prints the right extensions. 
                openFile = open(subFolderPath + "\\" + file, "r")
                readFile= openFile.read()
                # pattern matching to extract specific portion of the file
                ## Use regular expressions to identify the portion of text file to extract
                pattern2 = re.compile("(?<=\n#Mann=).+(?![A-z]+)") # Manning's n 
                pattern3 = re.compile(r"(?<=Type RM Length L Ch R =).+(\d+)") # Stations
                manningsCoeff = pattern2.finditer(readFile)
                stations = pattern3.finditer(readFile)

                stationsList = []
                for station in stations:
                    if int(station.group().split(",")[0].strip()) == 1:
                        stationsList.append(station.group().split())
                manningsCoeffList = []
                for coeffs in manningsCoeff:
                    numberOfIter = floordiv(int(coeffs.group().split(",")[0])-1, 3) + 1
                    newStartLocation = coeffs.start() + readFile[coeffs.start():].find("\n") + 1
                    TempList = []
                    while numberOfIter > 0:
                        line = readFile[newStartLocation:newStartLocation + readFile[newStartLocation:].find("\n")]
                        newStartLocation = newStartLocation + readFile[newStartLocation:].find("\n") + 1
                        numberOfIter = numberOfIter - 1
                        for item in line.split():
                            TempList.append(item)
                    manningsCoeffList.append(TempList)
                streamGeometryData = map(list.__add__,stationsList,manningsCoeffList)
                streamGeometry[file] = streamGeometryData

##CSV generation
#outputCheckMannings = csv.writer(open(folderLocation + "\\" +'streamGeometry'+ str(time.gmtime().tm_sec) + '.csv', 'wb'))
#list = []
#for key,value in streamGeometry.items():
#    temp = []
#    for i in range(len(value)):
#        temp1 = []
#        temp1.append(key)
#        for item in value[i]:
#            temp1.append(item)
#        temp.append(temp1)
#
#    for items in temp:
#        finalRow = []
#        for item in items:
#            for i in item.split(","):
#                finalRow.append(i)
#        outputCheckMannings.writerow(finalRow)
#
#
#
##############  GLOB AND TEXT FILE OPERATIONS  ##################
#
## From the email chain from some L/Reuven guy 
#import json
#import glob
#
#scores = { }
#for filename in glob.glob("scores/*.json"):
#
#    scores[filename] = { }
#
#    f = open(filename)
#    for result in json.load(f):
#        for subject, score in result.items():
#            scores[filename].setdefault(subject, [])
#            scores[filename][subject].append(score)
#
#for one_class in scores:
#    print(one_class)
#    for subject, subject_scores in scores[one_class].items():
#        print("\t{}: min {}, max {}, average {}".format(subject,
#                                                        min(subject_scores),
#                                                        max(subject_scores),
#                                                        float(sum(subject_scores)) / len(subject_scores)))
