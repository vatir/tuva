'''
Created on Mar 13, 2012

@author: Koan Briggs
'''
from numpy import array
from main import debug_level

class Import_Data_From_File():
    
    """
    Import old tuva tab delimited data
    
    fileloc is the system path and filename
    """
    
    def __init__(self, fileloc):
        filehandle = open(fileloc,'r')
        
        self.knowncol = {"Run_Name":0}
        self.uncertaintycol = {}
        self.uncertainty_columns = {}
        
        self._data = list()
        
        for line in filehandle:
            line_list = list()
            
            try:
                hoztestentry = 0
                for testentry in line.split():
                    if not (self.knowncol["Run_Name"] == hoztestentry): 
                        float(testentry)
                    hoztestentry += 1
                    
                hoztestentry = 0
                for entry in line.split():
                    if (self.knowncol["Run_Name"] == hoztestentry):
                        line_list.append(str(entry))
                    else:
                        line_list.append(float(entry))
                    hoztestentry += 1
                self._data.append(line_list)
                
            except ValueError:
                current_hoz_pos = 0
                for entry in line.split():
                    entry = entry.split("+")
                    if len(entry) > 1:
                        if entry[1]=="Uncertainty":
                            try:
                                self.uncertainty_columns[entry[0]]=entry[2]
                            except:
                                if debug_level >= 2:
                                    print "Data file heading included uncertainty without being followed with an uncertainty type."
                        if entry[0] in self.uncertaintycol.keys():
                            self.uncertaintycol[entry[0]] = current_hoz_pos
                        else:
                            self.uncertaintycol[entry[0]] = current_hoz_pos   
                    else:
                        if not (entry[0]=="Run_Name"):
                            self.uncertainty_columns[entry[0]]="None"
                        if entry[0] in self.knowncol.keys():
                            self.knowncol[entry[0]] = current_hoz_pos
                        else:
                            self.knowncol[entry[0]] = current_hoz_pos
                    current_hoz_pos += 1
                    
        self._data = array(self._data)
        filehandle.close()
        
    def uncertainty_types(self):
        return self.uncertainty_columns
    
    def uncertainty_values(self):
        traitdict = dict()
        for key in self.uncertaintycol.keys():
            traitdict[key] = array(self._data[:, self.uncertaintycol[key]],dtype='f8')
        return traitdict

    """
    If there is an error in the following function check for garbage at the end of the input file.
    
    Excel leaves spare tabs and newlines that can cause problems.  
    """
    def traits(self):
        traitdict = dict()
        for key in self.knowncol.keys():
            if key in ["Run_Name"]:
                traitdict[key] = array(self._data[:, self.knowncol[key]],dtype='S')
            if key not in (["Run_Name"]):
                traitdict[key] = array(self._data[:, self.knowncol[key]],dtype='f8')
        return traitdict

    def GetNumberRows(self):
        return int(self._data.shape[0])

    def GetNumberCols(self):
        return int(self._data.shape[1])
