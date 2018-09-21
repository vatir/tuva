from numpy import inf
#from numpy import ones
from collections import OrderedDict

"""
Setup Data Parameters for the Model
"""

data_param = [  "Substrate",
                "Anisotropy",
                "Protein",
                "Run_Name"]

output_param = "Anisotropy"

"""
Set Properties for Constrained Version:
    Can be written for both then changed with the Data.contrained variable.
"""

main_constrained = True     # Main Solver
local_constrained = True   # Model Solver

param = OrderedDict()
param = {
          's' : 0.0,
          'k1' : 0.0,
          }
param_upper_bounds = OrderedDict()
param_upper_bounds = {
          's' : 0.4,
          'k1' : 100.0,
          }
param_lower_bounds = OrderedDict()
param_lower_bounds = {
          's' : -0.2,
          'k1' : 0.0,
          }

#tolerence = 1e-8
#max_runs = 1e4
tolerence = 1e-6
max_runs = 1e8

"""
Setup Defaults for if parameters should be fit globally or per Run_Name Grouping

First Set to False then change the relevant parameters.
"""

use_individual_params = OrderedDict()
for key in param:
    use_individual_params[key]=False

use_individual_params["s"]=True

def func(param, return_oofunvalue=False):
    #try: 
        #((param["Protein"]+param["Substrate"]+1/param['k1'])-((param["Protein"]+param["Substrate"]+1/param['k1'])**(2.0)-4*(param["Protein"]*param["Substrate"]))**(0.5))/2.0
    PS = ((param["Protein"]+param["Substrate"]+param['k1'])-((param["Protein"]+param["Substrate"]+param['k1'])**(2.0)-4*(param["Protein"]*param["Substrate"]))**(0.5))/2.0
    #except ZeroDivisionError:
    #    print "Divide by Zero in PS Concentration Calculation"
    #    return ones(len(param["Protein"]))
    
    #try:
        #param['s'] * PS / (param['Substrate'])
    return param['s'] * PS / (param['Substrate'])
    #except ZeroDivisionError:
    #    print "Divide by Zero in Anisotropy Calculation"
    #    return ones(len(param["Protein"]))
