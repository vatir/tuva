import Data
from numpy import inf
from collections import OrderedDict
from FuncDesigner import oovar

if Data.model_init == False:
    Data.constrained = False
    
    Data.param = OrderedDict()
    Data.param = {
                  's' : 1.0,
                  'A' : 1.0,
                  'k1' : 1.0,
                  'k3' : 1.0,
                  'k4' : 1.0,
                  }
    Data.param_upper_bounds = OrderedDict()
    Data.param_upper_bounds = {
                              's' : inf,
                              'A' : inf,
                              'k1' : inf,
                              'k3' : inf,
                              'k4' : inf,
                              }
    Data.param_lower_bounds = OrderedDict()
    Data.param_lower_bounds = {
                              's' : 0.0,
                              'A' : 0.0,
                              'k1' : 0.0,
                              'k3' : 0.0,
                              'k4' : 0.0,
                              }

    Data.use_individual_params = OrderedDict()
    for key in Data.param:
        Data.use_individual_params[key] = False

    Data.model_init = True


from openopt import SNLE
from FuncDesigner import oovars
from numpy import zeros
from numpy import ones

#from Data import ImportOld

def func(param, return_oofunvalue=False):
    #print param
    #ImportOld.calltimes += 1
    #print "I have been called: " + str(ImportOld.calltimes) + " times"
    
    num = len(param["x"])
    
    p = oovar(size=num)
    d = oovar(size=num)
    n = oovar(size=num)
    
    equations = [
                 (0 == (param['k4'] + param['k4'] * param['k1'] * d + param['k3'] * param['k1'] * n + param['k4'] * param['k3'] * param['k1'] * d * n) * p - param['k4'] * param['x'])(tol=1e-8),
                 (0 == (ones(num) + param['k1'] * p + param['k3'] * param['k1'] * p * n) * d - param['dnaconc'])(tol=1e-8),
                 (0 == (param['k4'] + param['k1'] * param['k3'] * p + param['k4'] * param['k3'] * param['k1'] * p * d) * n - param['k4'] * param['nconc'])(tol=1e-8)
                 ]
    
    startpoint = {p:param['x'], d:param['dnaconc'], n:param['nconc']}
    
    system = SNLE(equations, startpoint, iprint= -1)
    
    if Data.constrained:
        # Slow but works when not close
        system.constraints = [
                              p > zeros(num), d > zeros(num), n > zeros(num),
                              p < param['x'], d < param['dnaconc'], n < param['nconc']
                              ]
        solutions = system.solve('nssolve')

    else:
        # Fast and good if close
        solutions = system.solve('scipy_fsolve')
    
    P, D, N = p(solutions), d(solutions), n(solutions)
    #print "P: " + str(P)
    #print "D: " + str(D)
    #print "N: " + str(N)
    return param['s'] * param['k1'] * (ones(num) + param['A'] * param['k3'] * N) * P * D / param['dnaconc']
    #if return_oofunvalue == True:
    #    return [param['s']*(param['k1']+param['A']*param['k2']*param['k4']*N)*P*D/param['dnaconc'],solutions.ff]
