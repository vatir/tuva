cur = float()
from collections import OrderedDict

def set_cur(newcur):
    global cur
    cur = newcur

def get_cur():
    return cur

from numpy import array


class ImportOld():
    """
    Import old conlin tab delimited data
    
    fileloc is the system path and filename
    """
    # Is used in testing model run behavior
    calltimes = 0
    model_init = False
    
    
    def __init__(self, fileloc):
        from numpy import array
        filehandle = open(fileloc, 'r')
        
        
        
        self.builtin = ["ind", "ind_error", "dep", "dep_error"]
        self.knowncol = {"ind":0, "ind_error":1, "dep":2, "dep_error":3, "group":4}
        
        self._data = OrderedDict()
        self._vertlen = 0
        self.numaddcol = 0
        for line in filehandle:
            self._hozlen = 0
            try:
                hoztestentry = 0
                for testentry in line.split():
                    if not (self.knowncol["group"] == hoztestentry): 
                        float(testentry)
                    hoztestentry += 1
                hoztestentry = 0
                for entry in line.split():
                    if (self.knowncol["group"] == hoztestentry):
                        self._data[(self._vertlen, self._hozlen)] = entry
                    else:
                        self._data[(self._vertlen, self._hozlen)] = float(entry)
                    self._hozlen += 1
                    hoztestentry += 1
                self._vertlen += 1
                
            except ValueError:
                for entry in line.split():
                    if entry in self.knowncol.keys():
                        self.knowncol[entry] = self._hozlen
                        self._hozlen += 1
                        
                    else:
                        self.numaddcol += 1
                        self.knowncol[entry] = self._hozlen
                        self._hozlen += 1
                        
        filehandle.close()
        
        
        self.init = True
        self.Update()
        self.init = False
        
    def Update(self):
        self._x = []
        self._y = []
        self._xerr = []
        self._yerr = []
        for i in range(self._vertlen):
            self._x.append(float(self._data[(i, self.knowncol["ind"])]))
            self._y.append(float(self._data[(i, self.knowncol["dep"])]))
            self._xerr.append(float(self._data[(i, self.knowncol["ind_error"])]))
            self._yerr.append(float(self._data[(i, self.knowncol["dep_error"])]))
        if self.init == False:
            from __main__ import MainFrame
            MainFrame.panel.plotpanel.Update()
            
    def traits(self):
        list = OrderedDict()
        for key in self.knowncol.keys():
            templist = []
            if key in ["group"]:
                for i in range(self._vertlen):
                    templist.append(self._data[(i, self.knowncol[key])])
                list[key] = array(templist)
            if key not in (self.builtin + ["group"]):
                for i in range(self._vertlen):
                    templist.append(float(self._data[(i, self.knowncol[key])]))
                list[key] = array(templist)
        return list
    
    def x(self):
        return array(self._x)

    def y(self):
        return array(self._y)

    def xerr(self):
        return array(self._xerr)

    def yerr(self):
        return array(self._yerr)
    
    def xmin(self):
        return float(min(self._x))

    def ymin(self):
        return float(min(self._y))

    def xmax(self):
        return float(max(self._x))

    def ymax(self):
        return float(max(self._y))
    
    def Get_Row_Len(self):
        return int(self._hozlen)

    def Get_Col_Len(self):
        return int(self._vertlen)

    def GetNumberRows(self):
        return int(self._vertlen)

    def GetNumberCols(self):
        return int(self._hozlen)
        
    def GetValue(self, row, col):
        value = self._data[(row, col)]

        if value is not None:
            return value
        else:
            return ''

    def SetValue(self, row, col, value):
        if (self.knowncol["group"] == col):
            self._data[(row, col)] = value
        else:
            self._data[(row, col)] = float(value)
        self.Update()
        

if __name__ == "__main__":
    data = ImportOld('../data/currentdata.dat')
    print data._data
    print data._hozlen
    print data._vertlen
