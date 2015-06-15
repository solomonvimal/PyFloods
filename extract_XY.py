# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 18:57:55 2015
Extraction of X, Y geographic co-ordinate pairs of cross-sections from the schematic using the RAS-Controller
Note: We could use shape file modules to reproject it anywhere we want.
@author: Solo
"""

import win32com.client
import matplotlib.pyplot as plt

# Example HEC-RAS file
ras_file = 'WhiteOakSwampMultiple.prj'
path_to_prj = 'C:\Users\solo\Dropbox\Python\HEC-RAS_Models\extracted\\' + ras_file

# Import Controller as an object handle
RC = win32com.client.Dispatch("RAS500.HECRASCONTROLLER") # HEC-RAS Version 5 (Beta)
RC.Project_Open(path_to_prj) 
AllXSPointCount = RC.Schematic_XSPointCount()
# Predefine size of arguments with no values in them
# values will be populated in L.H.S
NumRS =  RC.Schematic_XSCount()
RSName = [0]*NumRS;
ReachIndex = [0]*NumRS;
XSStartIndex = [0]*NumRS;
XSPointCount = [0]*NumRS;
XSPointX = [0]*AllXSPointCount;
XSPointY = [0]*AllXSPointCount;
# THE MOST USEFUL RASController function for X, Y coordinate pair export
RSName,ReachIndex,XSStartIndex,XSPointCount,XSPointX,XSPointY = \
RC.Schematic_XSPoints(RSName,ReachIndex, XSStartIndex, XSPointCount, XSPointX, XSPointY)

X = XSPointX
Y = XSPointY
plt.figure(1)
plt.plot(X,Y, 'ro', color = 'R', label='XY coordinate points')

