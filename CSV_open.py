# -*- coding: utf-8 -*-
"""
Created on Tue May 26 20:20:53 2015
Text matching
@author: Solo
"""
os.chdir("C:\Users\solo\Dropbox\Python")
path = "C:\Users\solo\Dropbox\Python\XS_table2.txt"
# open the csv file in excel and change the decimal places to none.
from numpy import genfromtxt


f = open('XS_table2.txt', 'r')
data = f.read()
data_split = re.split((r'\t'), data)



d = np.loadtxt(path, delimiter = "\t")


table = []
for row in reader:
    table.append(
    print re.split((r"\t"),b )
    
    a = 'adsfjdhfksdf\tdjlfhksdf'
    b = str(row)[2:-2]
    
os.chdir("C:\Users\solo\Dropbox\Python\HEC-RAS_Models")

import re
zips = glob.glob("*.zip")
TP37 = list([0]*len(zips))
for i, zip in enumerate(zips):
    print i, zip
    TP37[i] = re.split(r'_', zip)[0]
    
    
os.chdir("C:\Users\solo\Dropbox\Python\HEC-RAS_Models\extracted")

g01s = glob.glob("*.g01")    
