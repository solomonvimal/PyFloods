# -*- coding: utf-8 -*-
"""
Created on Fri May 01 13:24:53 2015

@author: Solo
"""



#############  GLOB AND TEXT FILE OPERATIONS  ##################
import json
import glob

scores = { }
for filename in glob.glob("scores/*.json"):

    scores[filename] = { }
    f = open(filename)
    for result in json.load(f):
        for subject, score in result.items():
            scores[filename].setdefault(subject, [])
            scores[filename][subject].append(score)

for one_class in scores:
    print(one_class)
    for subject, subject_scores in scores[one_class].items():
        print("\t{}: min {}, max {}, average {}".format(subject,
                                                        min(subject_scores),
                                                        max(subject_scores),
                                                        float(sum(subject_scores)) / len(subject_scores)))

##############   UNZIP  #####################

inspect.getmembers(zipfile, predicate=inspect.ismethod)
dir(zipfile)

dest_dir = '..'

import zipfile,os.path
def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)


#  Remove outliers by median
data = [1,2,3,200,5,6,7,8,9,10]

def reject_outliers(data, m = 0.5):
    #data = np.array(data)
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    data2 = [0]*len(data)
    s = d/mdev if mdev else 0.
    for i in range(len(data)):
        if (s[i]>=m):
            data[i] = (data[i-1]+data[i+1])/2
        else:
            data[i] = data[i]
            return data
    
def reject_outliers_threshold(data):
    
    