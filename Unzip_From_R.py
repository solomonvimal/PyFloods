''' 
This function calls an R function to extract zip file,
because Python has a path issue in its library. 

Install rpy2 from UCIrvine list -  http://www.lfd.uci.edu/~gohlke/pythonlibs/
System settings -> advanced-> environmental variables -> system path ->  
In the system variable field add two new variables:
R_HOME    c:\Program Files\R\R-3.1.3
R_USER    C:\Python27\Lib\site-packages\rpy2
Variable value : C:\Python27\Lib\site-packages\rpy2;C:\Program Files\R\R-2.15.0\bin\i386;C:\Python27\Lib\site-packages\rpy2\robjects

'''

f = "C:\\Users\\Solo\\Dropbox\\NFIE\\test_Alabama\\Crenshaw\\austin branch_model.zip"
outfolder = "C:\\Users\\Solo\\Dropbox\\NFIE\\test_Alabama\\Crenshaw\\Extracted2"

import rpy2.robjects as robjects
def UnZip_R(f, outfolder):
    robjects.r('''
    unzip_R <- function(f, outfolder) {
      unzip(f, exdir=outfolder)
    }
    ''')
    unzip_loadedFromR = robjects.r['unzip_R']
    vector = unzip_loadedFromR(f, outfolder)
    return list(vector)
    
    
rrr = UnZip_R(f,outfolder)