# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 10:24:34 2015

@author: Solo
"""

import arcpy
arcpy.env.workspace = "C:\\WorkSpace\\GISPy\\Class6"

import arcpy.mapping # import only specific class

from arcpy import env
env.workspace = "c:\\WorkSpace\\GISPy\\Class6"
from arcpy import *

arcpy.Clip_analysis("stream.shp", "study.shp", "results.shp", "#", "#",
                    {optional stuff})

arcpy.analysis.Clip(" ,, ")

# Geoprocessing using Python
my_count = arcpy.GetCount_managemtn("streets.shp")
print my_count

my_result = arcpy.Copy_management('street.shp','streets5.shp')

# environmental settings
env.workspace = r"C:\\WorkSpace\\GISPy\Class6"
env.cellsize = 30
env.overwriteOuput = True # by default ArcGIS does not allow to overwrite /
# this is very useful

print arcpy.ProductInfo()
print arcpy.CheckExtension("3D") # returns available or unavailable, ... 
print arcpy.CheckExtension("Spatial")
                                  
'''
if arcpy.CheckExtension("3D") == "Available":
    arcpy.CheckoutExtension("3D")
    arcpy.Slope_3d("dem", "slope", "DEGREES")
    arcpy.CheckInExtension("3D")
else:
    print "3D analyst license is unavailable"
'''

# from results in arcmap - drap drop the hammer to Python within ArcGIS
# to get the syntax of any tool


# Script Tools - script to GUI
# script tools does error checking visually with a check mark

# .py - .tbx - modify to get arguments from user

# Print doesn't work in ArcPy
arcPy.AddWarning("something was done")
arcPy.AddWarning("something was done") # this will be visible
#in the "tool is running GUI"


















