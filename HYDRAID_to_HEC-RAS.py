# -*- coding: utf-8 -*-
"""

This script takes all the *.zip files from a folder (ras_zip_folder) and makes
a table of HYDRAIDs and rasfiles and extracts all the contents of the .zip files
to a location (ras_zip_folder) - in this case the parent folder.

Created on Sun Jun 14 02:56:32 2015

@author: Solo
"""
# Changeables
#ras_zip_folder = r'C:\Users\Solo\Dropbox\Python\HEC-RAS_Models' ### Test case Tar
ras_zip_folder = r'C:\Users\Solo\Dropbox\EEP\Beaufort' ### Test case Catawba (9 minutes))

# Rest
import glob
import os
import tempfile
import zipfile

os.chdir(ras_zip_folder)
os.getcwd()

filenames = glob.glob("*.zip")

rasfiles = []
HYDRAIDs = []

for filename in filenames:
    temp = tempfile.mkdtemp()
    with zipfile.ZipFile(filename, "r") as z:
        z.extractall(temp)
        #z.extractall(ras_zip_folder)
        print temp
        os.chdir(temp)
        rasfile = glob.glob("*.prj")
        HYDRAID = filename[:filename.find('_')]
        os.chdir(ras_zip_folder)

        HYDRAIDs.append(HYDRAID)
        rasfiles.append(rasfile)

table = zip(HYDRAIDs, rasfiles)


###
'''if '\\' in filename:
    fname = fname.replace('\\', '/')
return fname'''

# 
# C:\Users\Solo\Dropbox\Python\HEC-RAS_Model
