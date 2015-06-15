'''
@author: Xing Zheng
Extracts elevations at station points of a cross-section from an intermediate file
'''

import string
import os
import sys
import numpy as np

def ReadGIS(GISfilename): # reads from txt file and writes to excel 
    Data = open(sys.path[0] + "\\" + GISfilename+'.txt','r')
    lines = Data.readlines()
    i = 0
    Riverstring = "River Name"
    Reachstring = "Reach Name"
    Stationstring = "RiverStation"
    for i in range(len(lines)):
        if lines[i].startswith(Riverstring):
            Rivername = lines[i][11:-2]
            Rivername = Rivername.replace(" ","_")
        elif lines[i].startswith(Reachstring):            
            Reachname = lines[i][11:-2]
            Reachname = Reachname.strip(" ")
            Reachname = Reachname.replace(" ","_")
        elif lines[i].startswith(Stationstring) and '*' not in lines[i] :
            if lines[i+1].startswith("XS"):
                Riverstation = lines[i][13:-2]
                Riverstation = Riverstation.strip(" ")
                X = []
                Y = []
                XY = []
                Distance = [0]
                Datapair = int(lines[i+1][16:-1]) # Get the number of GIS co-ordinate points
                Filename = Rivername + '_' + Reachname + '_' + Riverstation
                output = open(os.getcwd() + "\\Result\\GIS\\" + Filename + ".csv", 'w') # write the distance to XLS
                for j in range(Datapair):
                    XY = lines[i+3+j][:-1].split(",")
                    X.append(XY[0])
                    Y.append(XY[1])
                output.write("X(ft),Y(ft),Distance(ft)\n")
                output.write(X[0]+","+Y[0]+",0"+"\n")
                for j in range(1,Datapair):
                    Distance.append(((float(X[j])-float(X[j-1]))**2+(float(Y[j])-float(Y[j-1]))**2)**0.5 + Distance[j-1])
                    output.write(X[j]+","+Y[j]+","+str(Distance[j])+"\n")
                output.close()


def ReadGeometry(Geometryfilename): # station elevation table and write to CSV
    
    Data = open(sys.path[0] + "\\" + Geometryfilename + ".txt","r")
    lines = Data.readlines()
    i = 0
    Riverstring = "River Name"
    Reachstring = "Reach Name"
    Stationstring = "RiverStation"
    for i in range(len(lines)):
        if lines[i].startswith(Riverstring):
            Rivername = lines[i][11:-2]
            Rivername = Rivername.replace(" ","_")
        elif lines[i].startswith(Reachstring):      
            Reachname = lines[i][11:-2]
            Reachname = Reachname.strip(" ")
            Reachname = Reachname.replace(" ","_")
        elif lines[i].startswith(Stationstring) and '*' not in lines[i] :
            if lines[i+1].startswith("#Sta/Elev"):
                Riverstation = lines[i][13:-1].strip(' ')
                Filename = Rivername + '_' + Reachname + '_' + Riverstation
                output = open(os.getcwd() + "\\Result\\Geometry\\" + Filename + ".csv", 'w')
                output.write("Station(ft),Elevation(ft)\n")
    ##        elif lines[i].startswith('#Sta/Elev'):
                Datapair = int(lines[i+1][11:-1])
                for j in range(Datapair):
                    output.write(lines[i+3+j])
                output.close()

def CreatePoint(): # Interpolate X,Y,Z for each station point
    GISfolder = sys.path[0] + "\\Result\\GIS"
    Geometryfolder = sys.path[0] + "\\Result\\Geometry"
    Pointfolder = sys.path[0] + "\\Result\\Point"
    for GISfilename in os.listdir(GISfolder):
        for Geometryfilename in os.listdir(Geometryfolder):
            if GISfilename == Geometryfilename:
                Pointfilename = GISfilename
                Pointfilelocation = Pointfolder + "\\" + Pointfilename
                GISfilelocation = GISfolder + "\\" + GISfilename
                X, Y, Distance = np.loadtxt(GISfilelocation, delimiter=",", skiprows=1, usecols=(0,1,2), unpack=True)
                Geometryfilelocation = Geometryfolder + "\\" + Geometryfilename
                S, H = np.loadtxt(Geometryfilelocation, delimiter=",", skiprows=1, usecols=(0,1), unpack=True)
                PointX = np.empty(len(S))
                PointY = np.empty(len(S))
                PointM = np.empty(len(S))
                PointM = S*(Distance[-1]/S[-1])
                PointX = np.interp(S,Distance,X)
                PointY = np.interp(S,Distance,Y)
                np.savetxt(Pointfilelocation, np.column_stack((PointX,PointY,H,PointM)), fmt='%16.8f',delimiter=',', newline='\n', header='PointX,PointY,PointZ,PointM', comments='')
                continue

def XSPointmerge(): # make one big xls file

    Pointfolder = sys.path[0] + "\\Result\\Point"
    XSPoint = open(os.getcwd() + "\\Result\\XSPoint.csv", 'a')
    XSPoint.write("PointX,PointY,PointZ,PointM\n")
    for Pointfilename in os.listdir(Pointfolder):
        if Pointfilename.endswith(".csv"):
            XSPointpath = open(Pointfolder + "\\" + Pointfilename, 'r')
            XSPointset = XSPointpath.readlines()[1:]
            for line in XSPointset:
                XSPoint.write(line)
    XSPoint.close

def main():
    GISfilename = 'XSGIS'
    Geometryfilename = 'XSGeometry'
    ReadGIS(GISfilename)
    ReadGeometry(Geometryfilename)
    CreatePoint()
    XSPointmerge()
    print ("Work done! Please go to your project folder "
           + os.getcwd() + "\\Result" + " to check your result\n")

    done = raw_input('(press ENTER to quit)')

if __name__ == "__main__":
    main()
