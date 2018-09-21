
import wx.grid
from collections import OrderedDict
import Data

"""

This is the Data Entry/Manipulation Tab definition and primary file.

"""


class TabPanel(wx.Panel):
    
    """
    
    This panel holds and sizes the grid
    """
    
    #----------------------------------------------------------------------
    def __init__(self, parent, ID):
        """"""
 
        wx.Panel.__init__(self, parent, ID)
        
 
        self.sizer = wx.GridSizer()
        self.grid = wx.grid.Grid(self)
        self.table = DataGrid()
        
        self.grid.SetTable(self.table, True)
        self.sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizerAndFit(self.sizer)

        
class DataGrid(wx.grid.PyGridTableBase):
    """
    Data Entry Grid
    """
    def __init__(self):
        
        wx.grid.PyGridTableBase.__init__(self)
        
        """
        self.odd=wx.grid.GridCellAttr()
        self.odd.SetBackgroundColour("sky blue")
        #self.odd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.even=wx.grid.GridCellAttr()
        self.even.SetBackgroundColour("white")
        #self.even.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        """

        
        self.odd = wx.grid.GridCellAttr()
        self.odd.SetBackgroundColour("light blue")
        #self.odd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.even = wx.grid.GridCellAttr()
        self.even.SetBackgroundColour("white")
        #self.even.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
    def GetColLabelValue(self, col):
        return Data.currentdata.GetColName(col)
    
    def GetNumberRows(self):
        return Data.currentdata.GetNumberRows()
    
    def GetNumberCols(self):
        return Data.currentdata.GetNumberCols()
    
    def IsEmptyCell(self, row, col):
        return Data.currentdata.GetValue(row, col) is not None
    
    def GetValue(self, row, col):
        return Data.currentdata.GetValue(row, col)
        
    def SetValue(self, row, col, value):
        Data.currentdata.SetValue(row, col, value)
      
    def GetAttr(self, row, col, kind):
        attr = [self.even, self.odd][col % 2]
        attr.IncRef()
        return attr
