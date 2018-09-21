"""
This is the main starting point for project tuva.
Project tuva is a generalized data fitting application. 
The primary event loop will be initiated from the main function of this file.

Custom modules will be contained in the folder ./imports

Path to ./imports is added with AddSysPath

"""

"""
Import global modules
"""

import wx

# Debugging
#import pdb

"""
Setup path to custom modules
"""

def AddSysPath(new_path):
    import sys, os
    # standardise
    new_path = os.path.abspath(new_path)

    # MS-Windows does not respect case
    if sys.platform == 'win32':
        new_path = new_path.lower()

    # disallow bad paths
    do = -1
    if os.path.exists(new_path):
        do = 1
        
        # check against all paths currently available
        for x in sys.path:
            x = os.path.abspath(x)
            if sys.platform == 'win32':
                x = x.lower()
            if new_path in (x, x + os.sep):
                do = 0

        # add path if we don't already have it
        if do:
            sys.path.append(new_path)
            pass



if __name__ == "__main__":
    
    """
    
    Setup data holding module for cross module data sharing.
    
    data module contains all data and must be imported into any module that will use it.
    
    """
    
    AddSysPath('imports')
    
    
    import Data
    import MainWindow as mw
    
    # Import the data
    #Data.currentdata = Data.ImportOld('data/ISWI ATPase No Comp With 161 NCP 5-11-2012.dat')
    #Data.currentdata = Data.ImportOld('data/ISWI ATPase With ATP Gamma S With 161 NCP 5-11-2012.dat')
    Data.currentdata = Data.ImportOld('data/ISWI DNA Binding with ATP Gamma S.dat')
    
    
    # Instantiate the GUI enviornment.
    MainApp = wx.PySimpleApp()
    MainFrame = mw.CoreFrame(None)
    
    """
    
    Start GUI
    
    """
    
    """
    # Inspection Widget this allows tracking of GUI objects when uncommented.
    import wx.lib.inspection
    wx.lib.inspection.InspectionTool().Show()
    """
    
    # Startup main GUI Loop
    # Program runs as long as this loop is running
    MainApp.MainLoop()
