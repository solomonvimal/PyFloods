# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 02:56:32 2015

@author: Solo
"""

import glob
import os

ras_folder = 'C:\Users\Solo\Dropbox\Python\HEC-RAS_Models'
ras_folder = r'C:\Users\Solo\Dropbox\Python\HEC-RAS_Models\test'
os.chdir(ras_folder)
os.getcwd()

ZipNames = []
RASFileNames = []
filenames = glob.glob("*.zip")

outpath = 'C:\Users\Solo\Dropbox\Python\HEC-RAS_Models\test\extracted'



for filename in filenames:
    with zipfile.ZipFile(filename, "r") as z:
        outpathu = outpath + '\\' +filename [:-4]
        z.extractall(outpathu)
        os.chdir(outpathu)
        if glob.glob("*.prj"):
            print glob.glob("*.prj")
            matches = []


for root, dirnames, filenames in os.walk('C:\Users\Solo\Dropbox\Python\HEC-RAS_Models\test'):
    print root 
    print dirnames 
    print filenames
  for filename in fnmatch.filter(filenames, '*.c'):
    matches.append(os.path.join(root, filename))


          
zipnames.append(filename)

print filename[:filename.find('_')]

for t in tests.splitlines(): 

     print t[:t.find('_')].replace('.', '').upper()
     
re.sub("[^A-Z\d]", "", re.search("^[^_]*", str).group(0).upper())
