import os
import wx
from numpy import array
import Data

import matplotlib
import operator

from matplotlib.figure import Figure
matplotlib.use('WX')
matplotlib.interactive(True)
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
from numpy import arange
import matplotlib.pyplot as plt

class TabPanel(wx.Panel):
    """ The main frame of the application
    """
    def __init__(self, parent, ID):

        wx.Panel.__init__(self, parent, ID)
        wx.NO_FULL_REPAINT_ON_RESIZE
        
        self.create_main_panel(self)        
        self.draw_figure(first_time=True)
        self.allow_update = False
            
    def create_main_panel(self, parent):
        """ Creates the main panel with all the controls on it:
             * mpl canvas 
             * mpl navigation toolbar
             * Control panel for interaction
        """
        self.panel = wx.Panel(self)

        self.sizer = wx.GridSizer()
        self.sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.dpi = 100
        self.fig = Figure(dpi=self.dpi)
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        self.fig.set_facecolor('white')
        # Since we have only one plot, we can use add_axes 
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        
        self.drawbutton = wx.Button(self.panel, -1, "Redraw")
        self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton)

        self.cb_residuals = wx.CheckBox(self.panel, -1,
            "Show Residuals Plot",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_residuals, self.cb_residuals)

        self.cb_grid = wx.CheckBox(self.panel, -1,
            "Show Grid",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid, self.cb_grid)

        self.cb_connected = wx.CheckBox(self.panel, -1,
            "Connect Points",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_connected, self.cb_connected)

        self.allow_updates = wx.CheckBox(self.panel, -1,
            "Allow Updates",
            style=wx.ALIGN_RIGHT)
        self.allow_updates.SetValue(False)
        self.Bind(wx.EVT_CHECKBOX, self.change_update_status, self.allow_updates)

        # Create the navigation toolbar, tied to the canvas
        #
        self.toolbar = NavigationToolbar(self.canvas)
        
        #
        # Layout with box sizers
        #
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.vbox.Add(self.toolbar, 0, wx.EXPAND)
        self.vbox.AddSpacer(10)
        
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL
        
        self.hbox.Add(self.drawbutton, 0, border=3, flag=flags)
        self.hbox.Add(self.cb_residuals, 0, border=3, flag=flags)
        self.hbox.Add(self.cb_grid, 0, border=3, flag=flags)
        self.hbox.Add(self.cb_connected, 0, border=3, flag=flags)
        self.hbox.Add(self.allow_updates, 0, border=3, flag=flags)
        
        self.vbox.Add(self.hbox, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        
        self.panel.SetSizer(self.vbox)

        self.updateflag = False

        self.Bind(wx.EVT_IDLE, self.onIdle)
        #self.Bind(wx.EVT_SIZE, self.onSize(self))

    def change_update_status(self, event):
        if event.GetInt() == 1:
            self.allow_update = True
        elif event.GetInt() == 0:
            self.allow_update = False

    def plot_xrange(self, groups="Internal_ALL"):
        #self.xrange=arange(0.5*Data.currentdata.xmin(), 1.5*Data.currentdata.xmax(), ((0.5*Data.currentdata.xmax() - 1.5*Data.currentdata.xmin())/500.0))
        return Data.currentdata.x(groups=groups)
        
    def default_axis(self):
        #self.axes.set_xlim(0.9*Data.currentdata.xmin(), 1.1*Data.currentdata.xmax())
        #self.axes.set_ylim(0.9*Data.currentdata.ymin(), 1.1*Data.currentdata.ymax())
        return [
                0.9 * Data.currentdata.xmin(),
                1.1 * Data.currentdata.xmax(),
                0.9 * Data.currentdata.ymin(),
                1.1 * Data.currentdata.ymax()
                ]

    def draw_figure(self, first_time=None):
        """ Redraws the figure
        """
        
        # clear the axes and redraw the plot anew
        #
        
        self.fig.clf(keep_observers=True)
        
                
        if self.cb_residuals.IsChecked():
            self.axes = self.fig.add_subplot(211)
            self.residualsplot = self.fig.add_subplot(212)
            self.axes.axis(self.default_axis())
        else:
            self.axes = self.fig.add_subplot(111)
            self.axes.axis(self.default_axis())

        plot_params = {
                  'axes.labelsize': 10,
                  'text.fontsize': 10,
                  'legend.fontsize': 10,
                  'xtick.labelsize': 8,
                  'ytick.labelsize': 8
                  }
        #self.fig.rcParams(plot_params)
        
        # Add Legend
        self.fig.subplots_adjust(right=0.7)
        
        if first_time or self.cb_residuals.IsChecked():
            self.axes.cla()
            self.axes.axis(self.default_axis())
        else:
            currentaxis = self.axes.axis()
            self.axes.cla()
            self.axes.axis(currentaxis)
            
        self.axes.grid(self.cb_grid.IsChecked())
        
        
        if self.cb_connected.IsChecked():
            self.linestyle = '-'
        else:
            self.linestyle = ''
        
        try:
            maxres = 0.0
            ssr = 0.0
            if not first_time:
                reload(self.Parent.Parent.model)
                test_new_max_res = max(abs(Data.currentdata.y(groups=Data.currentdata.GetPlotGroups()) - self.Parent.Parent.model.func(dict({"x":self.plot_xrange(groups=Data.currentdata.GetPlotGroups())}, **dict(Data.currentdata.GetPlotParams(groups=Data.currentdata.GetPlotGroups()), **Data.currentdata.traits(groups=Data.currentdata.GetPlotGroups()))))))
                if test_new_max_res > maxres:
                    maxres = test_new_max_res
                if self.cb_residuals.IsChecked():
                    self.residualsplot.axis([self.default_axis()[0], self.default_axis()[1], -1.1 * maxres, 1.1 * maxres])
                    self.residualsplot.axes.grid(self.cb_grid.IsChecked())
                self.xrange = Data.currentdata.x(groups=Data.currentdata.GetPlotGroups())
                currentfitvalues = self.Parent.Parent.model.func(dict({"x":self.plot_xrange(groups=Data.currentdata.GetPlotGroups())}, **dict(Data.currentdata.GetPlotParams(groups=Data.currentdata.GetPlotGroups()), **Data.currentdata.traits(groups=Data.currentdata.GetPlotGroups()))))
                ssr = sum((currentfitvalues - Data.currentdata.y(groups=Data.currentdata.GetPlotGroups()))**2)
                
            for group in Data.currentdata.GetPlotGroups():


                self.axes.errorbar(
                    Data.currentdata.x(groups=group),
                    Data.currentdata.y(groups=group),
                    xerr=Data.currentdata.xerr(groups=group),
                    yerr=Data.currentdata.yerr(groups=group),
                    marker='o',
                    markersize=3,
                    picker=5,
                    linestyle=self.linestyle,
                    label=group,
                    color=array(Data.currentdata.GetColor(group)) / 255.0
                    )
                
                
                if not first_time:
                    current_plot_points = self.Parent.Parent.model.func(dict({"x":self.plot_xrange(groups=group)}, **dict(Data.currentdata.GetPlotParams(groups=group), **Data.currentdata.traits(groups=group))))
                    #print current_plot_points
                    self.axes.plot(
                        self.plot_xrange(groups=group),
                        current_plot_points,
                        linewidth=1.0,
                        color=array(Data.currentdata.GetColor(group)) / 255.0
                        )
        
                    if self.cb_residuals.IsChecked():
                        self.residualsplot.scatter(
                            Data.currentdata.x(groups=group),
                            Data.currentdata.y(groups=group) - current_plot_points,
                            marker='o',
                            picker=5,
                            color=array(Data.currentdata.GetColor(group)) / 255.0
                            )
    
            # Sort Legend
            handles, labels = self.axes.get_legend_handles_labels()
            hl = sorted(zip(handles, labels), key=operator.itemgetter(1))
            handles2, labels2 = zip(*hl)
            
            # Finish Plotting
            self.axes.legend(
                        handles2,
                        labels2,
                        loc=2,
                        bbox_to_anchor=(1.01, 1.0),
                        title="Max Residual: %f" % maxres + "\nSSR:                %f" % ssr,
                        shadow=True,
                        fancybox=True,
                        markerscale=3
                        )

            self.canvas.draw()
        except ValueError:
            pass
    def on_cb_grid(self, event):
        self.Update()
        event.Skip()
    
    def on_cb_connected(self, event):
        self.Update()
        event.Skip()

    def on_cb_residuals(self, event):
        self.fig.clf(keep_observers=True)
        self.Update()
        event.Skip()
    
    def on_slider_width(self, event):
        self.Update()
        event.Skip()
    
    def on_draw_button(self, event):
        self.Update()
        event.Skip()
    
    """
    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        # 
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points
        
        dlg = wx.MessageDialog(
            self, 
            msg, 
            "Click!",
            wx.OK | wx.ICON_INFORMATION)

        dlg.ShowModal() 
        dlg.Destroy()        
    """

        
    def on_text_enter(self, event):
        self.Update()
        event.Skip()

    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self,
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)
        
        event.Skip()

    def Update(self):
        if self.allow_update == True:
            self.updateflag = True

    
    def onIdle(self, event):
        if self.updateflag:
            self.updateflag = False
            self.draw_figure()
        event.Skip()

    #def onSize( self, event):
    #    self.resizeflag = True
    #    event.Skip()

