
import wx.aui
import numpy as np
from numpy import array


class TabbedPanel(wx.Panel):
    """
    This will be the panel that holds the tabs.
    """
    import DataPanel, PlotPanel, ParamPanel
    #import models.simplebinding as model
    #import models.bindingwithnuc as model
    
    """
    Import the data fitting model. This needs to be changed to a selection.
    """
    import models.single_site_binding_with_nucleotide as model
    
    import wx.py
    
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """
        Setup the GUI interface.
        """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        # create the AuiNotebook instance
        self.nb = wx.aui.AuiNotebook(self)
        
        
        #self.param = Data.param
        #self.currentdata = Data.currentdata
        
        """
        Each tab on the main gui gets an entry here. Then is added to the 
        """
        self.datapanel = self.DataPanel.TabPanel(self.nb, wx.ID_ANY)
        self.plotpanel = self.PlotPanel.TabPanel(self.nb, wx.ID_ANY)
        self.parampanel = self.ParamPanel.TabPanel(self.nb, wx.ID_ANY)
        #self.fitcodepanel = wx.py.editor.EditorFrame(self.nb , filename='imports/models/default.py')
        
        """
        Set the visable names for the tabs.
        """ 
        self.tabs = [
                (self.datapanel, "Data"),
                (self.plotpanel, "Plot"),
                (self.parampanel, "Parameters")
                #(self.fitcodepanel, "Fitting Code")
                ]
        
        """
        Add the tabs to the manager and setup the automatic sizer.
        """ 
        for page, label in self.tabs:
            self.nb.AddPage(page, label)
        
        self.sizer = wx.GridSizer()
        self.sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizerAndFit(self.sizer)

########################################################################

class CoreFrame(wx.Frame):
    
    """
    This is the main frame that hold all additional GUI elements.
    """
    
    #----------------------------------------------------------------------
    def __init__(self, parent):


        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "tuva",
                          size=(1024, 768))
        
        self._mgr = wx.aui.AuiManager(flags=wx.aui.AUI_MGR_DEFAULT) 
        self._mgr.SetManagedWindow(self) 

        self.panel = TabbedPanel(self)
        
        PaneInfoCenter = wx.aui.AuiPaneInfo().Center().MaximizeButton(True).MinSize((400, 300))
        self._mgr.AddPane(self.panel, PaneInfoCenter)
        #fitcodepanel = wx.py.editor.EditorFrame(self , filename='imports/models/default.py')
        #self._mgr.AddPane( fitcodepanel, PaneInfoCenter )
        self._mgr.Update()
        self.Show()

    def OnInit(self, evt):
        print "Hello"
        ConfigScreen = ConfigScreenSetup()
        ConfigScreen.Show()


class ConfigScreenSetup(wx.SplashScreen):
    """
    Setup initial config screen.
    """
    def __init__(self, parent=None):
        wx.SplashScreen.__init__(self, aBitmap, splashStyle, splashDuration, parent)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        wx.Yield()
#----------------------------------------------------------------------
