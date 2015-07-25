# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 01:01:46 2015
Merges the tabes of entrenchment ratio and makes a csv file with it
@author: Solo
"""
import csv
import glob
import pandas as pd
import os
import numpy as np
path = "C:\\Users\\Solo\\Dropbox\\EEP_2\\EntrenchmentTables"
os.chdir(path)
files = glob.glob("*.csv")
tables = [[],[]]

for file in files:
    print file
    for i,j in table:
        print i,j
        tables.append([i, str(j)])
tables = tables[2:]

filename = '.csv'
with open(path+filename, "w") as the_file:
    csv.register_dialect("custom", delimiter=",")
    writer = csv.writer(the_file, dialect="custom")
    for tup in tables:
        print tup
        writer.writerow(tup)