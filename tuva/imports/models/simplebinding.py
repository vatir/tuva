import Data
from numpy import inf
from collections import OrderedDict
from FuncDesigner import oovars

if Data.model_init == False:
    Data.constrained = False
    
    Data.param = OrderedDict()
    Data.param = {
              's' : 0.19,
              'k1' : 0.01,
              'offset' : 0.01,
              }
    Data.param_upper_bounds = OrderedDict()
    Data.param_upper_bounds = {
              's' : 1.0,
              'k1' : 1.0,
              'offset' : 0.0,
              }
    Data.param_lower_bounds = OrderedDict()
    Data.param_lower_bounds = {
              's' : 0.0,
              'k1' : 0.0,
              'offset' : inf,
              }

    Data.use_individual_params = OrderedDict()
    for key in Data.param:
        Data.use_individual_params[key] = False

    Data.model_init = True


from openopt import SNLE
from FuncDesigner import oovar
from numpy import ones
from numpy import zeros

#from Data import ImportOld

def func(param, return_oofunvalue=False):
    #print traits
    #ImportOld.calltimes += 1
    #print x
    #print "I have been called: " + str(ImportOld.calltimes) + " times"
    num = len(param["x"])
    
    p = oovar(size=num)
    d = oovar(size=num)
    
    equations = [
                 (0==- param["x"] + (ones(num) + param['k1'] * d) * p)(tol=1e-8),
                 (0==- param['NCPconc'] + (ones(num) + param['k1'] * p) * d)(tol=1e-8)
                 ]
    
    startpoint = {p:param['x'], d:param['NCPconc']}
    
    system = SNLE(equations, startpoint, iprint= 10)

    if Data.constrained:
        # Slow but works when not close
        system.constraints = [
                      p > zeros(num), d > zeros(num),
                      p < param['x'], d < param['NCPconc']
                      ]

        solutions = system.solve('nssolve')
    else:
        # Fast and good if close
        solutions = system.solve('scipy_fsolve')
    
    P, D = p(solutions), d(solutions)
    
    return param['s'] * (param['k1']) * P * D / param['NCPconc']+ param['offset']

