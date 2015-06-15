# -*- coding: utf-8 -*-
"""
Created on Thu May 28 10:35:15 2015
X and Y co-ordinate pairs from HEC-RAS Controller
@author: Solo
"""

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

###############################################################################
os.chdir("C:\Users\solo\Dropbox\Python\HEC-RAS_Models\extracted")
geometryfiles = glob.glob("*.g01")
projectfiles = glob.glob("*.prj")

BigXSPointX = []
EntRatio = []
BigER  = []
BigER2  = []
BigXS  = []
XMax = []
XMaxGeog = [] # maximum of x -coordinate in each
 model
XMaxHEC = []
for idx, ras_file in enumerate(projectfiles):
    print idx, ras_file
    RC.Project_Open('C:\Users\solo\Dropbox\Python\HEC-RAS_Models\extracted\\' + ras_file) 
    # first time use -> pop up for accepting terms
    # Get number of cross-sections
    NumRS =  RC.Schematic_XSCount(); # Number of nodes HEC-RAS will populate: not sure -> verify this
    StrNodeType = "" ############  XS node type
    # StrRS[i] = RC.Geometry.NodeRS(RiverID,ReachID, i) # River Station as string
    StrRS = RC.Geometry_GetNodes(RiverID, ReachID)[3]; # Not in the book! - Or this looks different in the book - Pg. 36

    # Get flow profiles
    NoProfiles = RC.Output_GetProfiles()[0]
    ProfileNames = RC.Output_GetProfiles()[1:NoProfiles-1]
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
    x = np.array(XSPointX)
    xmax = np.max(x)
    XMax.append(xmax)
    if xmax > 1:
        XMaxGeog.append(x)
    else:
        XMaxHEC.append(x)        
        l1 = len(XMaxHEC)
        l2 = len(XMaxGeog)
        diff = l1-l2        
print "Of the total %s HEC-RAS models, %s are in (0,0) to (1,1) co-ordinates and %s are \
in geographic co-ordinates" %(len(XMax), l1, l2)        
