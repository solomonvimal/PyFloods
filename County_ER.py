# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 8:21:49 2015
County_wide
@author: Solo
Takes the path to the county folder and gives out a table of entrenchment values for that county
"""
##################                                    #########################
##################            Variables               #########################
##################        (to be changed)             #########################


FRIS_folder = 'C:\\Users\\Solo\\Dropbox\\EEP\\FRIS' # <path to FRIS folder>
# outpath = ras_folder

############################################################################### 
###############################################################################

import inspect
import os
import numpy as np
import matplotlib.pyplot as plt
from numpy import matrix
import pickle 
import glob
import re
import csv
import time
import sys

def update_progress(progress):
    import sys
    barLength = 25 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
    
    
def get_HYDRAID_rasfiles_table(ras_folder):
    '''
    From the ras_folder which could be a HUC-8 or river basin or county folder,
    all the zip files are extracted to a temporary location to save the HEC-RAS
    model name and the corresponding zip file name (HYDRAID)
    The function returns 2 lists: 'HYDRAIDs' and 'rasfiles'
    '''
    import tempfile
    import glob
    import zipfile
    import os
    os.chdir(ras_folder_path)
    filenames = glob.glob("*.zip")
    zip_shp = glob.glob("*SHP.zip")
    zip_GDB = glob.glob("*GDB.zip")    
    filenames = list(set(filenames)-set(zip_shp) - set(zip_GDB))

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
            HYDRAIDs.append(HYDRAID)
            rasfiles.append(rasfile)
            os.chdir(ras_folder_path)
    return HYDRAIDs, rasfiles


def unzip_all(ras_folder):
    '''
    extract all the zip folders to the path where we want to do the entrechment ratio calculations
    '''
    import zipfile
    import os
    import glob
    outpath = ras_folder
    os.chdir(ras_folder)
    zipfilenames = glob.glob("*.zip")
    zip_shp = glob.glob("*SHP.zip")
    zip_GDB = glob.glob("*GDB.zip")
    zipfilenames = list(set(zipfilenames)-set(zip_shp) - set(zip_GDB))
    # Extract all files to outpath
    for zipfilename in zipfilenames:
        with zipfile.ZipFile(zipfilename, "r") as z:
            z.extractall(outpath)



def get_entrenchment_ratio(ras_folder, rasfiles, HYDRAIDs):
    '''
    Takes the ras_folder where the unzipped HEC_RAS files are sitting and opens
    each file iteratively to get the entrenchment ratios at each cross-section 
    and averages them over the model reach length using 3 formulas. Entrenchment
    using one formula is retained for making the entrenchment table that maps 
    the extracted HEC-RAS model information onto a unique HYDRAID, using 
    rasfiles as primary key. 'rasfiles' (primary key) is used to identify the 
    index of the HEC-RAS model filename (*.prj).
    '''
    import glob
    import win32com.client
    import os
    import numpy as np
    # Import Controller as an object handle
    RC4 = win32com.client.Dispatch("RAS41.HECRASCONTROLLER") # not case sensitive
    RC = win32com.client.Dispatch("RAS500.HECRASCONTROLLER") # HEC-RAS Version 5 (Beta)
    
    ###############     Global Parameters/Variables: Code/ID for the output feature    ####################
    
    RiverID = 1; ReachID = 1; ProfileNo = 1; AvgVelID = 23; TopWidthID = 62; 
    TopWidthLID = 63; TopWidthRID = 65; TopWidthID = 62; MinSectionElevationID = 136;
    ChannelStationLeftID = 158; ChannelStationRightID =  159;
    ChannelCenterStationID = 161; LOBElevID = 197; ROBElevID = 198;
    HydRadXSID = 208; # Hydarulic Radius = Area/Width
    HydRadLID = 209; HydRadCID = 210;
    HydRadRID = 211; MinChElStationID = 255;
    LStationID = 263; # Left Station of XS
    RStationID = 264; # Right Station of XS
    QTotalID = 9; # Total flow in cross section
    MaxChDepthID = 4; # Max Channel Depth
    AvgVelID = 23; # Average Velocity
   
    ###############################################################################
    
    os.chdir(ras_folder) 
    projectfiles = glob.glob("*.prj")
    BigXSPointX = []
    EntRatio = []
    BigER  = []
    BigER2  = []
    BigXS  = []
    EntrenchmentRatios = {}
    XS_ERs = {}
    RatingCurves = {}
    EntrenchmentTableID = []
    EntrenchmentTableValue = []
    
    for idx, ras_file in enumerate(projectfiles):
        if idx<0:
            pass
        else:
            print idx, ras_file
            RC.Project_Open(ras_folder+ "\\"+ ras_file) 
            print ras_file
            NumRS =  RC.Schematic_XSCount(); # Number of nodes HEC-RAS will populate: not sure -> verify this
            StrNodeType = "" # XS node type
            StrRS = RC.Geometry_GetNodes(RiverID, ReachID)[3]; # Not in the book! - Or this looks different in the book - Pg. 36
            # Get flow profiles
            NoProfiles = RC.Output_GetProfiles()[0]
            ProfileNames = list(RC.Output_GetProfiles()[1:NoProfiles+1])[0]
            Entrenchment_Ratio1 = [0]*NoProfiles; # LATEX: \sum_{i=1}^{n}{(ER_i \:DD_i})/ reach \:length
            Entrenchment_Ratio2 = [0]*NoProfiles; # LATEX: {\frac{\sum_{i=1}^N{(Top Width_i})/ N}{\sum_{i=1}^N{(ChannelWidth_i })/ N}} = {\frac{\sum_{i=1}^N{(Top Width_i})}{\sum_{i=1}^N{(ChannelWidth_i })}}
        
            Entrenchment_Ratio3 = [0]*NoProfiles; # LATEX: \frac{\sum_{i=1}^{n}{(EntrenchmentRatio_i })}{N}
            RatingCurve = [0]*NoProfiles;
            Flow = [0]*NoProfiles;
            Depth = [0]*NoProfiles;
            Velocity = [0]*NoProfiles;
            RatingCurve =  np.zeros(shape = (0,5));
            TopWidthP = [0]*NoProfiles;
            ChannelWidthP = [0]*NoProfiles;
            Avg_Vel = [0]*NumRS;
            ChannelStationRight = [0]*NumRS;
            ChannelStationLeft = [0]*NumRS;    
            #Flow, Depth, Velocity
            Avg_Vel = [0]*NumRS;
            QTotal = [0]*NumRS;
            MaxChDepth = [0]*NumRS; 
            outliers = []
            for i in range(NumRS):
                Avg_Vel[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, 1, AvgVelID)[0]
                if Avg_Vel[i] > 100:
                    print int(i)
                    outliers = np.append(outliers, i)  ### local  
        
            #NumRS = NumRS - len(outliers)
            # Create an empty column vector for each variable for the number of XS
            TopWidth = [0]*NumRS; 
            XS = [0]*NumRS;
            ChannelWidth = [0]*NumRS;
            DownstreamDistance = [0]*NumRS;
            ER = [0]*NumRS;
            ER2= [0]*NumRS;
            for p in range(1, NoProfiles+1): # For each flow profile, extract information from HEC-RAS files
                for i in range(NumRS): 
                    if (i not in outliers): # for each cross section (XS)
                        # print i
                        XS[i] = int(float(StrRS[i]))
                        # i - XS node number, 0 is upstreamsection for bridge, append zero to get the value and assign it to a row
                        Avg_Vel[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, AvgVelID)[0] # p=3 (profile number) - hard coded in controller Pg: 36
                        MaxChDepth[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, MaxChDepthID)[0] # Maximum Channel Depth
                        QTotal[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, QTotalID)[0] # Total Flow 
                        TopWidth [i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, TopWidthID)[0] # Top Width
                        ChannelStationRight[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, ChannelStationRightID)[0] # R.B.S of Channel
                        ChannelStationLeft[i] = RC.Output_NodeOutput(RiverID, ReachID, i+1, 0, p, ChannelStationLeftID)[0] # R.B.S of Channel
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
                TopWidthP[p-1] = np.average(TopWidth)
                ChannelWidthP[p-1] = np.average(ChannelWidth)
                Entrenchment_Ratio1[p-1] = np.sum(ER)/(XS[0]-XS[NumRS-1])            # Entrenchment ratio in each XS*downstream distance / total distance
                Entrenchment_Ratio2[p-1] = np.average(TopWidth)/np.average(ChannelWidth) # Average TopWidth/Average ChannelWidth
                Entrenchment_Ratio3[p-1] = np.average(ER2)
                if p==1:
                    if [ras_file] in rasfiles:
                        print ras_file
                        Index = rasfiles.index([ras_file])    
                        EntrenchmentTableID.append(HYDRAIDs[Index])
                        EntrenchmentTableValue.append(Entrenchment_Ratio1[p-1]) 
                    else:
                        pass
            EntrenchmentRatio = np.array(zip(ProfileNames,Entrenchment_Ratio1,Entrenchment_Ratio2,Entrenchment_Ratio3))
            EntrenchmentRatios["EntrenchmentRatio_"+ras_file[0:-4]] = EntrenchmentRatio
            #        import pickle, os
            #        os.chdir("C:\Users\solo\Dropbox\Python")
            #        pickle.dump(EntrenchmentTable, open("EntrenchmentTable.p", "wb"))   
            #        f = open("EntrenchmentRatios.p")
            #        g = open("EntrenchmentTable.p")
            #        EntrenchmentRatios = pickle.load(f)
            #        EntrenchmentTable = pickle.load(g)
        EntrenchmentTable = zip(EntrenchmentTableID, EntrenchmentTableValue)
    return EntrenchmentTable


###################  SAVE!! EntrenchmentTable somewhere #####################


# write to csv - both inside the folder and outside the folder
def write_entrenchment_table_to_csv(EntrenchmentTable):
    import csv
    filename = '{0}_ET_Table_CSV.csv'.format(ras_folder)
    with open(ras_folder_path+'\\'+filename, "w") as the_file:
        csv.register_dialect("custom", delimiter=",")
        writer = csv.writer(the_file, dialect="custom")
        for tup in EntrenchmentTable:
            print tup
            writer.writerow(tup)
            
def get_entrenchment_csvs_in_one_place(EntrenchmentTable):
    import csv
    filename = '{0}_ET_Table_CSV.csv'.format(ras_folder)
    with open('C:\\Users\\Solo\\Dropbox\\EEP\\FRIS\\1\\EntrenchmentTables\\'+filename, 'w') as the_file:
        csv.register_dialect("custom", delimiter=",")
        writer = csv.writer(the_file, dialect="custom")
        for tup in EntrenchmentTable:
            print tup
            writer.writerow(tup)

###############################################################################

#def main(FRIS_folder):
'''
The function runs through all the HEC-RAS county folders and populates 
the EntrenchmentTable within each folder
'''
import time
import os
import sys
FRIS_counties_path =FRIS_folder
os.chdir(FRIS_counties_path)   
counties = os.listdir(os.getcwd())
counties = counties[13:] # where the 2-last files are the county folders

for j, ras_folder in enumerate(counties):
    try:
        ras_folder = counties[j]
        print j, ras_folder
        time.sleep(0.000000000000000001)
        update_progress(j/len(counties))
        ras_folder_path = FRIS_counties_path+'\\'+ras_folder
        os.chdir(ras_folder_path)
        HYDRAIDs, rasfiles = get_HYDRAID_rasfiles_table(ras_folder_path)    
        unzip_all(ras_folder_path)
        EntrenchmentTable = get_entrenchment_ratio(ras_folder_path, rasfiles, HYDRAIDs)
        write_entrenchment_table_to_csv(EntrenchmentTable)
        get_entrenchment_csvs_in_one_place(EntrenchmentTable)
    except:
        pass