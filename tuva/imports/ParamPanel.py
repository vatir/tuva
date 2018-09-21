from functools import partial
import wx
from numpy import zeros
import Data
from collections import OrderedDict
import  wx.lib.scrolledpanel as scrolled
from openopt import NLLSP
from openopt import NLP
from openopt import SNLE
from numpy import array
from time import time
from numpy import ones
from FuncDesigner import oovar

class TabPanel(scrolled.ScrolledPanel):
    """
    This is the parameter setting and control panel. 
    """
    #----------------------------------------------------------------------
    def __init__(self, parent, ID):
        """"""
        scrolled.ScrolledPanel.__init__(self, parent, -1)
 
        vsizer = wx.BoxSizer(wx.VERTICAL)

        exportbuttontuva = wx.Button(
                                  self,
                                  label="Export All - tuva"
                                  )
        
        exportbuttontuva.Bind(wx.EVT_BUTTON, partial (self.Exporttuva, "exportfilename"))
        
        vsizer.Add(exportbuttontuva)

        exportbuttontable = wx.Button(
                                  self,
                                  label="Export All - Table"
                                  )
        
        exportbuttontable.Bind(wx.EVT_BUTTON, partial (self.Exporttable, "exportfilename"))
        
        vsizer.Add(exportbuttontable)
        
        self.paramentrylinks = OrderedDict()
        
        """
        Add data fitting options
        and setup visual layout.
        """
        
        self.add_group_selection_boxes(vsizer)
        
        self.add_param_boxes(vsizer, Data.param, self.paramentrylinks, Main=True)
        self.add_fit_button(vsizer, self.paramentrylinks, "Fit Selected", groups=Data.currentdata.GetFitGroups(), Main=True)
        indssrresult = OrderedDict()
        indtimeresult = OrderedDict()
        self.individualparamentrylinks = OrderedDict()
        self.Groups = Data.currentdata.GetGroups()
        Data.param_individual = OrderedDict()
        for entry in Data.currentdata.GetGroups():
            Data.param_individual[entry] = Data.param.copy()
            self.individualparamentrylinks[entry] = OrderedDict()
            
            self.add_param_boxes(vsizer, Data.param, self.individualparamentrylinks[entry], groups=entry)
            indssrresult[entry], indtimeresult[entry] = self.add_fit_button(vsizer, self.individualparamentrylinks[entry], "Fit Group: " + str(entry), groups=entry)
            
        fitallsep = wx.Button(
                              self,
                              label="Fit All Individually"
                              )
        
        ssrresult = wx.StaticText(self,
                         label="",
                         size=(150, 12)
                         )
        
        timeresult = wx.StaticText(self,
                         label="",
                         size=(150, 12)
                         )

        fitallsep.Bind(wx.EVT_BUTTON, partial (self.runfitallsep, self.individualparamentrylinks, indssrresult=indssrresult, indtimeresult=indtimeresult))

        fitsizer = wx.BoxSizer(wx.HORIZONTAL)
        fitsizer.Add(fitallsep)
        fitsizer.Add(ssrresult)
        fitsizer.Add(timeresult)

        vsizer.Add(fitsizer)
        
        """
        Set panel sizer and scrolling
        """
        self.SetSizer(vsizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

    def add_fit_button(self, vsizer, paramentrylinks, buttonlabel, groups=None, Main=False):
        fitsizer = wx.BoxSizer(wx.HORIZONTAL)
        mainfit = wx.Button(
                                  self,
                                  label=buttonlabel
                                  )
        
        ssrresult = wx.StaticText(self,
                         label="",
                         size=(150, 12)
                         )
        
        timeresult = wx.StaticText(self,
                         label="",
                         size=(150, 12)
                         )
        
        fitsizer.Add(mainfit)
        fitsizer.Add(ssrresult)
        fitsizer.Add(timeresult)
        
        mainfit.Bind(wx.EVT_BUTTON, partial (self.datafit, groups=groups, paramlinks=paramentrylinks, ssrresult=ssrresult, timeresult=timeresult, Main=Main))
        
        vsizer.Add(fitsizer)
        return (ssrresult, timeresult)

    def runfitallsep(self, paramlinks, event, indssrresult=None, indtimeresult=None):
        for entry in paramlinks.keys():
            self.datafit(event, paramlinks=paramlinks[entry], groups=entry, ssrresult=indssrresult[entry], timeresult=indtimeresult[entry])
            
    def add_param_boxes(self, vsizer, params, paramlinks, Main=False, groups=None):
        if Main == True:
            self.use_individual_fit_params = OrderedDict()
        for key in params.keys():

            """
            Add parameter setting options
            """
            
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            paramtext = wx.StaticText(self,
                                     label=key,
                                     pos=(10, 12)
                                     )
            
            paramentry = wx.TextCtrl(self,
                                    wx.ID_ANY,
                                    str(params[key]),
                                    pos=(40, 10),
                                    style=wx.TE_PROCESS_ENTER
                                    )
            
            paramfit = wx.CheckBox(self,
                                   wx.ID_ANY,
                                   "Fit Me"
                                   )
            ssrresult = wx.StaticText(self,
                             label="",
                             size=(150, 12)
                             )
            
            paramfit.SetValue(True)
            paramfit.Bind(wx.EVT_CHECKBOX, partial(self.paramfit_main, key=key))
            
            paramentry.Bind(wx.EVT_TEXT_ENTER, partial (self.updateentry, key=key, main=Main, groups=groups))
            paramlinks[key] = (paramtext, paramentry, paramfit, ssrresult)
            
            hsizer.Add(paramtext)
            hsizer.Add(paramentry)
            hsizer.Add(paramfit)
            if Main == True:
                update_other_params = wx.Button(
                                                self,
                                                label="Set Individual Prameters to Global"
                                                )
                hsizer.Add(update_other_params)
                update_other_params.Bind(wx.EVT_BUTTON, partial (self.update_other_params_action, param_name=key))
                self.use_individual_fit_params[key] = wx.CheckBox(
                                                                  self,
                                                                  wx.ID_ANY,
                                                                  "Use the Individual Fit Parameters"
                                                                  )
                self.use_individual_fit_params[key].Bind(wx.EVT_CHECKBOX, partial(self.use_individual_fit_params_action, param=key))
                self.use_individual_fit_params[key].SetValue(False)                
                hsizer.Add(self.use_individual_fit_params[key])
                
            vsizer.Add(hsizer)
            
    def paramfit_main(self, event, key):
        if event.GetInt() == 1:
            self.use_individual_fit_params[key].SetValue(0)
            Data.use_individual_params[key] = False
            self.Parent.Parent.plotpanel.Update()
            
    def use_individual_fit_params_action(self, event, param):
        if event.GetInt() == 1:
            self.paramentrylinks[param][2].SetValue(0)
            Data.use_individual_params[param] = True
        elif event.GetInt() == 0:
            Data.use_individual_params[param] = False
        self.Parent.Parent.plotpanel.Update()
    
    def update_other_params_action(self, event, param_name):
        for entry in self.individualparamentrylinks:
            self.individualparamentrylinks[entry][param_name][1].SetValue(self.paramentrylinks[param_name][1].GetValue())
            self.individualparamentrylinks[entry][param_name][2].SetValue(self.paramentrylinks[param_name][2].GetValue())
    
    def add_group_selection_boxes(self, vsizer):
        for group in Data.currentdata.GetGroups():
            """
            Add group options setting options
            """
            
            group_hsizer = wx.BoxSizer(wx.HORIZONTAL)
            group_name = wx.StaticText(self,
                                     label=group,
                                     pos=(10, 12)
                                     )

            fit_set = wx.CheckBox(self,
                                   wx.ID_ANY,
                                   "Fitting"
                                   )

            plot_set = wx.CheckBox(self,
                                   wx.ID_ANY,
                                   "Plotting"
                                   )

            fit_set.SetValue(True)
            plot_set.SetValue(True)
            fit_set.Bind(wx.EVT_CHECKBOX, partial (self.set_fit_group, group=group))
            plot_set.Bind(wx.EVT_CHECKBOX, partial (self.set_plot_group, group=group))
            
            group_hsizer.Add(group_name)
            group_hsizer.Add(fit_set)
            group_hsizer.Add(plot_set)
            
            vsizer.Add(group_hsizer)
            
    def set_plot_group(self, event, group):
        Data.currentdata.SetPlotGroup(group, event.GetSelection())
    
    def set_fit_group(self, event, group):
        Data.currentdata.SetFitGroup(group, event.GetSelection())
    
    def updateentry(self, event, key, main, groups):
        try:
            float(event.GetString());
            if main:
                Data.param[key] = float(event.GetString())
            else:
                Data.param[key] = float(event.GetString())
                Data.param_individual[groups][key] = float(event.GetString())
            
            self.Parent.Parent.plotpanel.Update()
            #event.Skip()
        except ValueError:
            #event.Skip()
            print "Input Error in Fitting Parameter Input"
        
    def datafit(self, event, paramlinks, groups=[], ssrresult=None, timeresult=None, Main=False):
        def errfunc(fit_params, x=None, y=None, yerr=None, consts=None, traits=None, groups=None, snle_style = False):
            fitrun = fitfunc(fit_params, x, consts, traits, groups, return_oofunvalue=True, snle_style = snle_style)
            #print "Fit Params: " + str(fitrun)
            #print "Bad Fit Adjust: " + str(ssr_mod_for_bad_fit[0])
            if snle_style:
                try:
                    if fitrun[0]:
                        fitrun[2].append(0==((fitrun[1] - y) / (array(yerr) + 1.0))**2.0)
                        return [fitrun[2], fitrun[3], fitrun[4]]
                except:
                    if fitrun[0]:
                        fitrun[2].append(0==((fitrun[1] - y) / (array(yerr) + 1.0))**2.0)
                        return [fitrun[2], fitrun[3]]
            else:
                return ((fitrun - y) / (array(yerr) + 1.0))**2.0
            #*(1.0+ssr_mod_for_bad_fit)

        def fitfunc(fit_params, x, consts=None, traits=None, groups=None, return_oofunvalue=False, snle_style = False):
            reload(self.Parent.Parent.model)
            tempparam = OrderedDict()
            k = 0
            m = 0

            templist = list()
            for j in range(len(paramlinks.keys())):
                key = paramlinks.keys()[j]

                if (paramlinks[key][2].IsChecked()):
                    tempparam[key] = fit_params[k]
                    k += 1

                elif (Main == True and self.use_individual_fit_params[key].GetValue()):
                    tempparam[key] = list()
                    for group in groups:
                        tempparam[key].append(list(float(self.individualparamentrylinks[group][key][1].GetValue())*ones(len(Data.currentdata.x(groups=group)))))
                    tempparam[key] = array(sum(tempparam[key], []))
                else:
                    try:
                        tempparam[key] = consts[m]
                        m += 1
                    except:
                        pass
                
            tempparam["x"] = x
            tempparam.update(traits)
            #print "Fit Params: "+str(fit_params)
            #print "x values: "+str(x)
            #print "consts: "+str(consts)
            #print "traits: "+str(traits)
            #print "Results:" +str(self.Parent.Parent.model.func(x, tempparam, traits))
            
            return self.Parent.Parent.model.func(tempparam, return_oofunvalue=return_oofunvalue, snle_style = snle_style)

        # Find Current Params
        params = OrderedDict()
        for param in paramlinks.keys():
            params[param] = float(paramlinks[param][1].GetValue())
        
        
        # Check for empty groups
        if groups == []:
            return False
            
        #from scipy.optimize import leastsq
        t = time()

        #results = fitting.solve('nlp:scipy_slsqp', iprint = 1)
        #results = fitting.solve('nlp:lincher', iprint = 1)
        
        print_level = 10
        # Best so far
        if Data.constrained and Data.snle:
            #fitting = NLLSP(
            p0 = list()
            consts = list()
            ibounds = list()
            sp = OrderedDict()
            # Setup fitted params and consts
            for j in range(len(params.keys())):
                key = params.keys()[j]
                value = params.values()[j]
                if paramlinks[key][2].IsChecked():
                    try:
                        point = oovar(size=len(value))
                    except TypeError:
                        point = oovar()
                    p0.append(point)
                    sp[point] = value
                    ibounds.append(Data.param_upper_bounds[key] > p0[-1] > Data.param_lower_bounds[key])
                else:
                    consts.append(array(value))
            equations = []
            startpoint = []
            equations = errfunc(p0, y=Data.currentdata.y(groups=groups),
                                     yerr=Data.currentdata.yerr(groups=groups),
                                     consts=consts,
                                     traits=Data.currentdata.traits(groups=groups),
                                     x=Data.currentdata.x(groups=groups),
                                     groups=groups,
                                     snle_style = True
                                     )
            startpoint = equations[1]
            startpoint.update(sp)
            print startpoint
            fitting = SNLE(
                            equations[0],
                            startpoint,
                            ftol=1e-10,
                            )
            equations[2].extend(ibounds)
            fitting.constraints = equations[2]
            #results = fitting.solve('nlp:ralg', iprint=print_level)
            results = fitting.solve('nssolve', iprint = print_level, maxIter = 1e8)

            p1 = results.xf
            
            for key in p1:
                try:
                    params[key]
                    params[key] = p1[key]
                except:
                    pass

        elif (not Data.constrained) and (not Data.snle):
            p0 = list()
            consts = list()
            ub = list()
            lb = list()
            # Setup fitted params and consts
            for j in range(len(params.keys())):
                key = params.keys()[j]
                value = params.values()[j]
                if paramlinks[key][2].IsChecked():
                    p0.append(array(value))
                    ub.append(Data.param_upper_bounds[key])
                    lb.append(Data.param_lower_bounds[key])
                else:
                    consts.append(array(value))

            equations = partial (errfunc,
                                     y=Data.currentdata.y(groups=groups),
                                     yerr=Data.currentdata.yerr(groups=groups),
                                     consts=consts,
                                     traits=Data.currentdata.traits(groups=groups),
                                     x=Data.currentdata.x(groups=groups),
                                     groups=groups,
                                     snle_style = False,
                                     )
            fitting = NLP(
                            equations,
                            p0,
                            )
            results = fitting.solve('scipy_leastsq', iprint=print_level, maxIter = 1e8)
            p1 = results.xf
            
            i = 0
            for j in range(len(params.keys())):
                key = params.keys()[j]
                if paramlinks[key][2].IsChecked():
                    params[key] = p1[i]
                    i += 1

        elif (Data.constrained) and (not Data.snle):
            p0 = list()
            consts = list()
            ub = list()
            lb = list()
            # Setup fitted params and consts
            for j in range(len(params.keys())):
                key = params.keys()[j]
                value = params.values()[j]
                if paramlinks[key][2].IsChecked():
                    p0.append(array(value))
                    ub.append(Data.param_upper_bounds[key])
                    lb.append(Data.param_lower_bounds[key])
                else:
                    consts.append(array(value))

            fitting = NLP(
                            partial(errfunc,
                                     y=Data.currentdata.y(groups=groups),
                                     yerr=Data.currentdata.yerr(groups=groups),
                                     consts=consts,
                                     traits=Data.currentdata.traits(groups=groups),
                                     x=Data.currentdata.x(groups=groups),
                                     groups=groups,
                                     snle_style = False,
                                     ),
                            p0,
                            ub=ub,
                            lb=lb,
                            ftol=1e-16,
                            
                            )
            
            results = fitting.solve('ralg', iprint = print_level, maxIter = 1e8)
            #results = fitting.solve('nssolve', iprint = print_level, maxIter = 1e8)
            p1 = results.xf
        
            i = 0
            for j in range(len(params.keys())):
                key = params.keys()[j]
                if paramlinks[key][2].IsChecked():
                    params[key] = p1[i]
                    i += 1

        # Good if close
        #results = fitting.solve('nlp:scipy_cobyla', iprint = 1)
        
        #print('solution: '+str(results.xf)+'\n||residuals||^2 = '+str(results.ff)+'\nresiduals: ')
        
        
        
        if not Main:
            #print groups
            #print p1
            #print Data.param_individual["3"].keys()
            #print Data.param
            try:
                i = 0
                for key in params.keys():
                    if paramlinks[key][2].IsChecked():
                        Data.param_individual[groups][key] = p1[i]
                        i += 1
            except:
                print "More than one group was passed, when there should have been only one."
            #print Data.param_individual
            
        """
        Cleanup and redraw
        """
        
        for key in paramlinks.keys():
            paramlinks[key][1].SetValue(str(params[key]))
        
        self.Parent.Parent.plotpanel.Update()
        
        self.xrange = Data.currentdata.x(groups=groups)
        currentfitvalues = fitfunc(p1, Data.currentdata.x(groups=groups), consts=consts, traits=Data.currentdata.traits(groups=groups), groups=groups)
        #ssr = sum((currentfitvalues - Data.currentdata.y(groups=groups)) ** 2)
        ssr = sum(map(lambda x: x**2, currentfitvalues - Data.currentdata.y(groups=groups)))/len(currentfitvalues)

        #print "SSR:" + str(ssr)
        Data.param = params
        
        ssrresult.SetLabel("SSR: " + str(ssr))
        timeresult.SetLabel("Time Elapsed: %f" % (time() - t))
        
        self.Parent.Parent.plotpanel.Update()

    def Exporttuva(self, filename, action):

        import cPickle
        output = open('data.pkl', 'wb')
        for group in Data.currentdata.GetGroups():
            cPickle.dump(group, output)
            cPickle.dump(Data.currentdata.GetPlotParams(group), output)
        output.close()

    def Exporttable(self, filename, action):
        #print filename
        
        print "Global Fit"
        for x in Data.currentdata.GetPlotParams():
            print str(x) + "\t" + str(Data.currentdata.GetPlotParams()[x])
            
        for group in Data.currentdata.GetGroups():
            print "Group: " + str(group)
            print group
            for x in Data.currentdata.GetPlotParams(groups=group):
                print str(x) + "\t" + str(Data.currentdata.GetPlotParams(groups=group)[x])
