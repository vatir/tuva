from numpy import array
from numpy import append
from numpy import dtype

from collections import OrderedDict

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
        
        #self._data = OrderedDict()
        self._data = list()
        
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
                        groupentry = entry
                        line_list.append(str(entry))
                    else:
                        line_list.append(float(entry))
                    hoztestentry += 1
                self._data.append(line_list)
                
            except ValueError:
                current_hoz_pos = 0
                for entry in line.split():
                    
                    if entry in self.knowncol.keys():
                        self.knowncol[entry] = current_hoz_pos
                    else:
                        self.knowncol[entry] = current_hoz_pos
                    current_hoz_pos += 1
                    
        self._data = array(self._data)
        
        filehandle.close()
        
        
        self.init = True
        self.Update()
        self.init = False
        
    def Update(self):
        if self.init == False:
            from __main__ import MainFrame
            MainFrame.panel.plotpanel.Update()

    def traits(self):
        traitdict = dict()
        for key in self.knowncol.keys():
            if key in ["group"]:
                traitdict[key] = array(self._data[:, self.knowncol[key]], dtype='S')
            if key not in (self.builtin + ["group"]):
                traitdict[key] = array(self._data[:, self.knowncol[key]], dtype='f')
        return traitdict
    
    def x(self):
        return array(self._data[:, self.knowncol["ind"]], dtype='f')

    def y(self):
        return array(self._data[:, self.knowncol["dep"]], dtype='f')

    def xerr(self):
        return array(self._data[:, self.knowncol["ind_error"]], dtype='f')

    def yerr(self):
        return array(self._data[:, self.knowncol["dep_error"]], dtype='f')
    
    def xmin(self):
        return float(min(array(self._data[:, self.knowncol["ind"]], dtype='f')))

    def ymin(self):
        return float(min(array(self._data[:, self.knowncol["dep"]], dtype='f')))

    def xmax(self):
        return float(max(array(self._data[:, self.knowncol["ind"]], dtype='f')))

    def ymax(self):
        return float(max(array(self._data[:, self.knowncol["dep"]], dtype='f')))
    
    def Get_Row_Len(self):
        return int(self._data.shape[1])

    def Get_Col_Len(self):
        return int(self._data.shape[0])

    def GetNumberRows(self):
        return int(self._data.shape[0])

    def GetNumberCols(self):
        return int(self._data.shape[1])
        
    def GetValue(self, row, col):
        value = self._data[(row, col)]

        if value is not None:
            return value
        else:
            return ''

    def SetValue(self, row, col, value):
        if (self.knowncol["group"] == col):
            self._data[(row, col)] = str(value)
        else:
            self._data[(row, col)] = float(value)
        self.Update()
      
