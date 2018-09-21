import Data
from numpy import inf
from collections import OrderedDict
from FuncDesigner import oovars

if Data.model_init == False:
    Data.constrained = True
    Data.local_constrained = False
    Data.snle = False
    Data.param = OrderedDict()
    Data.param = {
              'k1' : 0.0,
              'od'  : 1.0,
              'm'  : 0.6,
              }
    Data.param_upper_bounds = OrderedDict()
    Data.param_upper_bounds = {
              'k1' : inf,
              'od'  : inf,
              'm'  : 3.0,
              }
    Data.param_lower_bounds = OrderedDict()
    Data.param_lower_bounds = {
              'k1' : 0.0,
              'od'  : 1.0,
              'm'  : 0.0,
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

def func(param, return_oofunvalue=False, snle_style = False):
    #print traits
    #ImportOld.calltimes += 1
    #print x
    #print "I have been called: " + str(ImportOld.calltimes) + " times"
    num = len(param["x"])
    
    p = oovar(size=num)
    print param
#    equations = [
#                 (0.0 == param["x"] - p * (ones(num) + param['k1'] * s * (ones(num) + 2.0 * param['k2'] * p)))(tol=1e-12),
#                 (0.0 == param["Substrate"] - s * (ones(num) + param['k1'] * p * (ones(num) + param['k2'] * p)))(tol=1e-12),
#                 ]
    
    # m == k2/k1
    # 
    s = param["N"]
    equations = [
                 (0.0 == param['od']*param["x"] - p * (ones(num) + param['k1'] * s * (ones(num) + 2.0 * param['k1'] * param['m'] * p)))(tol=1e-12)
                 ]
    
    #startpoint = {p:param['x']/2.0, s:param['Substrate']/2.0}
    startpoint = {p:param['x']}
    #startpoint = {p:zeros(num), s:zeros(num)}
    
    system = SNLE(equations, startpoint, iprint= 1000)

    if Data.local_constrained:
        # Slow but works when not close
        constraints = [
                      p > zeros(num), s > zeros(num),
                      p < param['x'], s < param['Substrate'],
                      p > param['x'] - 2*param['Substrate']
                      ]
        system.constraints = constraints
        #solutions = system.solve('interalg')
    
    if Data.local_constrained:
        solutions = system.solve('nssolve')
        
    else:
        # Fast and good if close
        solutions = system.solve('scipy_fsolve')
        
    P = p(solutions)
    print "Protein:"
    print P

    return s * (ones(num) + param['k1'] * P * (ones(num) + param['k1'] * param['m'] * P))/param['od']

