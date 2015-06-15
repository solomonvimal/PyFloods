# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 21:10:13 2015
Extract all files from sub-folders and place it in the main folder

@author: Solo
"""

import shutil
import os
 
main_folder = "C:\Users\Solo\Dropbox\Python\\HEC-RAS_Models\\test2\\extracted"
os.chdir(main_folder)
 
# The current working directory
dest_dir = os.getcwd()
# The generator that walks over the folder tree
walker = os.walk(dest_dir)
 
# the first walk would be the same main directory
# which if processed, is
# redundant
# and raises shutil.Error
# as the file already exists
 
rem_dirs = walker.next()[1]
for data in walker:
    for files in data[2]:
        try:
            shutil.move(data[0] + os.sep + files, dest_dir)
        except shutil.Error: # still to be on the safe side
            continue
        
# clearing the directories
# from whom we have just removed the files
for dirs in rem_dirs:
    shutil.rmtree(dest_dir + os.sep + dirs)
