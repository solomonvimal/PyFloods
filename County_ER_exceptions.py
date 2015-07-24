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


FRIS_folder = 'F:\\EEP\\FRIS' # <path to FRIS folder>
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


def extract_subfolders(folder):
    '''
    Extract all files from sub-folders and place it in the parent folder
    '''
    import shutil
    import os
    #main_folder = "C:\Users\Solo\Dropbox\Python\\HEC-RAS_Models\\test3"
    main_folder = folder
    os.chdir(main_folder)
    # The current working directory
    dest_dir = os.getcwd()
    # The generator that walks over the folder tree
    walker = os.walk(dest_dir)
    # the first walk would be the same main directory which if processed, is
    # redundant and raises shutil.Error as the file already exists
    rem_dirs = walker.next()[1]
    for data in walker:
        for files in data[2]:
            try:
                shutil.move(data[0] + os.sep + files, dest_dir)
            except shutil.Error: # still to be on the safe side
                continue
    # clearing the directories from where we just removed the files
    for dirs in rem_dirs:
        shutil.rmtree(dest_dir + os.sep + dirs)
        

      
def get_HYDRAID_rasfiles_table(ras_folder_path):
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
        try:
            with zipfile.ZipFile(filename, "r") as z:
                z.extractall(temp)
                z.extractall(ras_folder_path)
        except:
            #HYDRAID = 'no_file_found'
            #rasfile = 'no_file_found'
            pass
        
        print temp
        os.chdir(temp)
        extract_subfolders(temp)
        rasfile = glob.glob("*.prj") #picks the first HEC-RAS model - typically, there is just one per zip folder
        HYDRAID = filename[:filename.find('_')]
        HYDRAIDs.append(HYDRAID)
        rasfiles.append(rasfile)
        os.chdir(ras_folder_path)
    return HYDRAIDs, rasfiles


def unzip_all(ras_folder_path):
    '''
    extract all the zip folders to the path where we want to do the entrechment ratio calculations
    '''
    import zipfile
    import os
    import glob
    outpath = ras_folder_path
    os.chdir(ras_folder_path)
    zipfilenames = glob.glob("*.zip")
    zip_shp = glob.glob("*SHP.zip")
    zip_GDB = glob.glob("*GDB.zip")
    zipfilenames = list(set(zipfilenames)-set(zip_shp) - set(zip_GDB))
    # Extract all files to outpath
    for zipfilename in zipfilenames:
        try:
            with zipfile.ZipFile(zipfilename, "r") as z:
                z.extractall(outpath)
                extract_subfolders(outpath)
        except:
            pass



def get_entrenchment_ratio(ras_folder_path, rasfiles, HYDRAIDs):
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
    
    os.chdir(ras_folder_path) 
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
            try:
                RC.Project_Open(ras_folder_path+ "\\"+ ras_file) 
                #RC.showras()
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
            except:
                pass
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
    with open(FRIS_folder+'\\'+filename, 'w') as the_file:
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
FRIS_counties_path = FRIS_folder
os.chdir(FRIS_counties_path)   
counties = os.listdir(os.getcwd())
counties = counties[2:] # get only the folders

done_counties = ["Wilson","Alexander", "Alleghany","Anson","Ashe",
        "Avery","Beaufort","Bertie","Burke","Cabarrus","Caldwell","Camden",
        "Carteret","Catawba","Cherokee","Chowan","Clay","Cleveland","Craven",
        "Currituck","Davidson","Davie","Durham","Edgecombe","Forsyth", "Franklin",
        "Gaston","Gates","Granville","Greene","Guilford","Halifax","Harnett",
        "Henderson","Hertford","Hoke","Johnston","Jones","Lee","Lenoir","Lincoln",
        "Macon","Martin","Mecklenburg","Montgomery","Moore","New Hanover",
        "Northampton","Onslow","Pamlico","Pasquotank","Perquimans","Person","Pitt",
        "Polk","Randolph","Richmond","Rockingham","Sampson","Scotland","Stanly",
        "Stokes","Surry","Vance","Wake","Warren","Washington","Wayne"]

''' 3 cases of undone counties - Exception cases:
1. Counties that have instead of a .zip file a .ERROR file that I mentioned in 
an earlier email. Brian said it might be because those files don't exist in the
 website, but we need to check this. 
 The counties with this case are Alamance, Cumberland, and Chatham.
2. Some counties have only the GDB and SHP zip files. Dare, Hyde, Tyrrell.
3. Some counties have the HEC-RAS files one step down within the zip folder.
Brunswick, Buncombe,  Jackson, Haywood, Madison, Mitchell, Swain, Transylvania, Yancey.
'''
    
undone_counties = ['Alamance','Cumberland','Chatham', 'Dare', 'Hyde', 'Tyrrell',
                   'Brunswick','Buncombe', 'Jackson','Haywood', 'Madison', 
                   'Mitchell', 'Swain', 'Transylvania', 'Yancey']

undone_counties = undone_counties[6:]

#for j, ras_folder in enumerate(counties):
#        if ras_folder in done_counties:
#            print("Calculattion of ER done!")
#        else:
#             print(str(ras_folder))
#             undone_counties.append(ras_folder)

for j, ras_folder in enumerate(undone_counties):
         ras_folder = undone_counties[j]
         print(j, ras_folder)
         time.sleep(0.000000000000000001)
         update_progress(j/len(counties))
         ras_folder_path = FRIS_counties_path+'\\'+ras_folder
         os.chdir(ras_folder_path)
         HYDRAIDs, rasfiles = get_HYDRAID_rasfiles_table(ras_folder_path)
         unzip_all(ras_folder_path)
         EntrenchmentTable = get_entrenchment_ratio(ras_folder_path, rasfiles, HYDRAIDs)
         write_entrenchment_table_to_csv(EntrenchmentTable)
         get_entrenchment_csvs_in_one_place(EntrenchmentTable)

        # Brunswick, Chatham (ERROR), Dare(only GDB), Haywood(one step-down) , Jackson, Madison, Mitchell
        # Swain(one step down - HEC-RAS), Transylvania (one-step down HEC-RAS, hec-ras)
         # Tyrrell (no zips with hec-ras, only gdb), Yancey (one_step_down)