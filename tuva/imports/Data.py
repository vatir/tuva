from numpy import array
from numpy import append
from numpy import dtype

import Data
from collections import OrderedDict
from numpy import ones
from numpy.random import random_integers 
# Is used in testing model run behavior
calltimes = 0
model_init = False

# Build a consistent color list
colorlist = OrderedDict()
colorlist["black"] = (0, 0, 0)
colorlist["red"] = (255, 0, 0)
colorlist["goldenrod"] = (218, 165, 32)
colorlist["magenta 3"] = (205, 0, 205)
colorlist["midnightblue"] = (25, 25, 112)
colorlist["indian red"] = (176, 23, 31)
colorlist["emeraldgreen"] = (0, 201, 87)
colorlist["honeydew 4"] = (131, 139, 131)
colorlist["green 2"] = (0, 238, 0)
colorlist["deepskyblue"] = (0, 191, 255)
colorlist["orangered 2"] = (238, 64, 0)
colorlist["sgi beet"] = (142, 56, 142)
colorlist["manganeseblue"] = (3, 168, 158)
colorlist["cornflowerblue"] = (100, 149, 237)

class ImportOld():
    """
    Import old conlin tab delimited data
    
    fileloc is the system path and filename
    """
    
    def __init__(self, fileloc):
        from numpy import array
        filehandle = open(fileloc, 'r')
        
        self.builtin = ["ind", "ind_error", "dep", "dep_error"]
        self.knowncol = {"ind":0, "ind_error":1, "dep":2, "dep_error":3, "group":4}
        
        self._groupeddata = OrderedDict()
        self._grouplist = list()
        
        for line in filehandle:
            line_list = list()
            
            try:
                hoztestentry = 0
                for testentry in line.split():
                    if not (self.knowncol["group"] == hoztestentry): 
                        float(testentry)
                    hoztestentry += 1
                hoztestentry = 0
                
                for entry in line.split():
                    if (self.knowncol["group"] == hoztestentry):
                        line_list.append(str(entry))
                        
                    else:
                        line_list.append(float(entry))
                    hoztestentry += 1
                
                try:
                    self._groupeddata[str(line_list[self.knowncol["group"]])].append(line_list)
                except KeyError:
                    self._groupeddata[str(line_list[self.knowncol["group"]])] = list()
                    self._groupeddata[str(line_list[self.knowncol["group"]])].append(line_list)
                # The following exception is a quick fix and may cause problems.
                except IndexError:
                    pass
                
            except ValueError:
                current_hoz_pos = 0
                for entry in line.split():
                    
                    if entry in self.knowncol.keys():
                        self.knowncol[entry] = current_hoz_pos
                    else:
                        self.knowncol[entry] = current_hoz_pos
                    current_hoz_pos += 1
                    
        filehandle.close()
        
        
        self.init = True
        self.Update()
        self.init = False
        self._plotgroups = self._groupeddata.keys()
        self._fitgroup = self._groupeddata.keys()
        n = 0
        while n < len(self._groupeddata.keys()):
            try:
                Data.colorlist[Data.colorlist.keys()[n]]
            except:
                Data.colorlist["Random Color: " + str(n)] = (random_integers(0, 255), random_integers(0, 255), random_integers(0, 255))
            n += 1
    def GetColName(self, col):
        for entry in self.knowncol:
            if col == self.knowncol[entry]:
                return entry
    
    def Update(self):
        if self.init == False:
            from __main__ import MainFrame
            MainFrame.panel.plotpanel.Update()

    def traits(self, groups="Internal_ALL"):
        traitdict = dict()
        if (groups == "Internal_ALL" and not hasattr(groups, '__iter__')):
            for key in self.knowncol.keys():
                if key in ["group"]:
                    traitdict[key] = array(map(str, array(sum(self._groupeddata.values(), []), dtype=object)[:, self.knowncol[key]]))
                if key not in (self.builtin + ["group"]):
                    traitdict[key] = array(map(float, array(map(float, array(sum(self._groupeddata.values(), []), dtype=object)[:, self.knowncol[key]]))))
        elif not hasattr(groups, '__iter__'):
            for key in self.knowncol.keys():
                if key in ["group"]:
                    traitdict[key] = array(map(str, array(self._groupeddata[groups], dtype=object)[:, self.knowncol[key]]))
                if key not in (self.builtin + ["group"]):
                    traitdict[key] = array(map(float, array(self._groupeddata[groups], dtype=object)[:, self.knowncol[key]]))
        elif hasattr(groups, '__iter__'):
            tempdata = list()
            for key in groups:
                tempdata.append(self._groupeddata[key])
            tempdata = sum(tempdata, [])
            for key in self.knowncol.keys():
                if key in ["group"]:
                    traitdict[key] = array(map(str, array(tempdata, dtype=object)[:, self.knowncol[key]]))
                if key not in (self.builtin + ["group"]):
                    traitdict[key] = array(map(float, array(map(float, array(tempdata, dtype=object)[:, self.knowncol[key]]))))
        
        return traitdict
    
    def x(self, groups="Internal_ALL"):
        if (groups == "Internal_ALL" and not hasattr(groups, '__iter__')):
            return array(map(float, array(sum(self._groupeddata.values(), []), dtype=object)[:, self.knowncol["ind"]]))
        elif not hasattr(groups, '__iter__'):
            return array(map(float, array(self._groupeddata[groups], dtype=object)[:, self.knowncol["ind"]]))
        elif hasattr(groups, '__iter__'):
            tempdata = list()
            for key in groups:
                tempdata.append(self._groupeddata[key])
            tempdata = sum(tempdata, [])
            return array(map(float, array(tempdata, dtype=object)[:, self.knowncol["ind"]]))
        
    def y(self, groups="Internal_ALL"):
        if (groups == "Internal_ALL" and not hasattr(groups, '__iter__')):
            return array(map(float, array(sum(self._groupeddata.values(), []), dtype=object)[:, self.knowncol["dep"]]))
        elif not hasattr(groups, '__iter__'):
            return array(map(float, array(self._groupeddata[groups], dtype=object)[:, self.knowncol["dep"]]))
        elif hasattr(groups, '__iter__'):
            tempdata = list()
            for key in groups:
                tempdata.append(self._groupeddata[key])
            tempdata = sum(tempdata, [])
            return array(map(float, array(tempdata, dtype=object)[:, self.knowncol["dep"]]))

    def xerr(self, groups="Internal_ALL"):
        if (groups == "Internal_ALL" and not hasattr(groups, '__iter__')):
            return array(map(float, array(sum(self._groupeddata.values(), []), dtype=object)[:, self.knowncol["ind_error"]]))
        elif not hasattr(groups, '__iter__'):
            return array(map(float, array(self._groupeddata[groups], dtype=object)[:, self.knowncol["ind_error"]]))
        elif hasattr(groups, '__iter__'):
            tempdata = list()
            for key in groups:
                tempdata.append(self._groupeddata[key])
            tempdata = sum(tempdata, [])
            return array(map(float, array(tempdata, dtype=object)[:, self.knowncol["ind_error"]]))

    def yerr(self, groups="Internal_ALL"):
        if (groups == "Internal_ALL" and not hasattr(groups, '__iter__')):
            return array(map(float, array(sum(self._groupeddata.values(), []), dtype=object)[:, self.knowncol["dep_error"]]))
        elif not hasattr(groups, '__iter__'):
            return array(map(float, array(self._groupeddata[groups], dtype=object)[:, self.knowncol["dep_error"]]))
        elif hasattr(groups, '__iter__'):
            tempdata = list()
            for key in groups:
                tempdata.append(self._groupeddata[key])
            tempdata = sum(tempdata, [])
            return array(map(float, array(tempdata, dtype=object)[:, self.knowncol["dep_error"]]))
    
    def xmin(self, groups="Internal_ALL"):
        if (groups == "Internal_ALL" and not hasattr(groups, '__iter__')):
            #print sum(self._groupeddata.values(), [])[:,0]
            return float(min(array(map(float, array(sum(self._groupeddata.values(), []), dtype=object)[:, self.knowncol["ind"]]))))

    def ymin(self, groups="Internal_ALL"):
        if (groups == "Internal_ALL" and not hasattr(groups, '__iter__')):
            return float(min(array(map(float, array(sum(self._groupeddata.values(), []), dtype=object)[:, self.knowncol["dep"]]))))

    def xmax(self, groups="Internal_ALL"):
        if (groups == "Internal_ALL" and not hasattr(groups, '__iter__')):
            return float(max(array(map(float, array(sum(self._groupeddata.values(), []), dtype=object)[:, self.knowncol["ind"]]))))

    def ymax(self, groups="Internal_ALL"):
        if (groups == "Internal_ALL" and not hasattr(groups, '__iter__')):
            return float(max(array(map(float, array(sum(self._groupeddata.values(), []), dtype=object)[:, self.knowncol["dep"]]))))

    def GetPlotParams(self, groups=None):
        #print "Got Groups: " +str(groups)
        tempparam = OrderedDict()
        for key in Data.param:
            if Data.use_individual_params[key] == True:
                tempparam[key] = list()
                if isinstance(groups, str):
                    tempparam[key].append(list(float(Data.param_individual[groups][key]) * ones(len(Data.currentdata.x(groups=groups)))))
                else:
                    for group in groups:
                        tempparam[key].append(list(float(Data.param_individual[group][key]) * ones(len(Data.currentdata.x(groups=group)))))
                tempparam[key] = array(sum(tempparam[key], []))
            else:
                tempparam[key] = Data.param[key]
        return tempparam

    def GetParam(self, groups = "Main"):
        #print "Got Groups: " +str(groups)
        tempparam = OrderedDict()
        for key in Data.param:
            if Data.use_individual_params[key] == True:
                tempparam[key] = list()
                if isinstance(groups, str):
                    tempparam[key].append(list(float(Data.param_individual[groups][key]) * ones(len(Data.currentdata.x(groups=groups)))))
                else:
                    for group in groups:
                        tempparam[key].append(list(float(Data.param_individual[group][key]) * ones(len(Data.currentdata.x(groups=group)))))
                tempparam[key] = array(sum(tempparam[key], []))
            else:
                tempparam[key] = Data.param[key]
        return tempparam

    """
    def GetGroups(self):
        return self._groupeddata.keys()
        self._plotgroups = self._groupeddata.keys()
        self._fitgroup = self._groupeddata.keys()
    """
    
    def SetFitGroup(self, group, state):
        if state == 1:
            self._fitgroup.append(group)
        elif state == 0:
            self._fitgroup.remove(group)
            
    def SetPlotGroup(self, group, state):
        if state == 1:
            self._plotgroups.append(group)
        elif state == 0:
            self._plotgroups.remove(group)

        if self.init == False:
            from __main__ import MainFrame
        MainFrame.panel.plotpanel.Update()

    def GetFitGroups(self):
        return self._fitgroup

    def GetPlotGroups(self):
        return self._plotgroups

    def GetGroups(self):
        return self._groupeddata.keys()
    
    def GetNumberRows(self):
        return len(sum(self._groupeddata.values(), []))

    def GetNumberCols(self):
        return len(self._groupeddata.values()[0][0])
         
    def GetValue(self, row, col):
        value = sum(self._groupeddata.values(), [])[row][col]

        if value is not None:
            return value
        else:
            return ''

    def GetColor(self, groupname):
        groupcolors = dict()
        
        for n in range(len(self._groupeddata.keys())):
            try:
                groupcolors[self._groupeddata.keys()[n]] = colorlist.values()[n]
            except IndexError:
                groupcolors[self._groupeddata.keys()[n]] = colorlist.values()[0]
        return groupcolors[groupname]
    
    """
    FIX ME
    """
    def SetValue(self, row, col, value):
        if (self.knowncol["group"] == col):
            self._data[(row, col)] = str(value)
        else:
            self._data[(row, col)] = float(value)
        self.Update()
