

#from numpy import inf
from collections import OrderedDict
from openopt import SNLE
from FuncDesigner import oovars
from numpy import ones
from numpy import zeros

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

main_constrained = False     # Main Solver
local_constrained = True   # Model Solver

param = OrderedDict()
param = {
          's' : 0.50,
          'k1' : 0.50,
          }
param_upper_bounds = OrderedDict()
param_upper_bounds = {
          's' : 1.0,
          'k1' : 1.0,
          }
param_lower_bounds = OrderedDict()
param_lower_bounds = {
          's' : 0.0,
          'k1' : 0.0,
          }
tolerence = 1e-8
max_runs = 1e4

"""
Setup Defaults for if parameters should be fit globally or per Run_Name Grouping

First Set to False then change the relevant parameters.
"""

use_individual_params = OrderedDict()
for key in param:
    use_individual_params[key]=False

use_individual_params["s"]=True



#from Data import ImportOld

def func(param, return_oofunvalue=False):
    
    num = len(param["Substrate"])
    
    p, s = oovars(2, size = num)
    
    equations = [
                 (0==-param["Protein"]+(ones(num)+param['k1']*s)*p)(tol=tolerence),
                 (0==-param['Substrate']+(ones(num)+param['k1']*p)*s)(tol=tolerence),
                 ]
    
    startpoint = {p:param["Protein"], s:param['Substrate']}
    
    system = SNLE(equations, startpoint, iprint = -100)
    
    
    if local_constrained:
        # Slow but works when not close
        system.constraints = [
                      p > zeros(num), s > zeros(num),
                      p < param['Protein'], s < param['Substrate']
                      ]
        solutions = system.solve('nssolve')
    else:
        # Fast and good if close
        solutions = system.solve('scipy_fsolve')
    
    
    P, S = p(solutions), s(solutions)
    
    return param['s']*(param['k1'])*P*S/param['Substrate']
