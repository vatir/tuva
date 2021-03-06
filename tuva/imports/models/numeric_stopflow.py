import Data
from numpy import inf
from collections import OrderedDict
from FuncDesigner import oovar

if Data.model_init == False:
    Data.constrained = False
    
    Data.param = OrderedDict()
    Data.param = {
                  'A' : 1.0,
                  'r' : 1.0,
                  'n' : 1.0,
                  'kt' : 1.0,
                  'kd' : 1.0,
                  'kend' : 1.0,
                  }
    Data.param_upper_bounds = OrderedDict()
    Data.param_upper_bounds = {
                  'A' : inf,
                  'r' : inf,
                  'n' : inf,
                  'kt' : inf,
                  'kd' : inf,
                  'kend' : inf,
                              }
    Data.param_lower_bounds = OrderedDict()
    Data.param_lower_bounds = {
                  'A' : 0.0,
                  'r' : 0.0,
                  'n' : 0.0,
                  'kt' : 0.0,
                  'kd' : 0.0,
                  'kend' : 0.0,
                              }

    Data.use_individual_params = OrderedDict()
    for key in Data.param:
        Data.use_individual_params[key] = False

    Data.model_init = True


from openopt import SNLE
from FuncDesigner import oovars
from numpy import ones, power, e, array, zeros
from scipy.special import gamma, gammaincc


from functools import partial
from funcs.talbot import talbot
from multiprocessing import Pool, cpu_count, current_process


def ToBeRun(self, i):
    return func.ToBeRun2(self, i)

class func():

    def __init__(self, param, return_oofunvalue=False):
        worker_pool = Pool(1)
        #print param
        #ImportOld.calltimes += 1
        #print "I have been called: " + str(ImportOld.calltimes) + " times"
        from wx import SafeYield
        from time import time
        start_run_time = time()
        self.param = param
        self.num = len(param["x"])
        self.return_values = worker_pool.map(partial(ToBeRun, self), xrange(self.num))
        worker_pool.close()
        worker_pool.join()
        print "Time elapsed: %f :" % (time() - start_run_time) + " : Run Param (n): %f" % param["n"]
        SafeYield()
        
    def __len__(self):
        return len(self.return_values)
    def __sub__(self, other):
        return self.return_values - other
    
    def F(self, s, A, n, r, kend, kd, kt):
        from numpy import ones
        value = A * (1.0 + n * r) ** (-1.0) * ((s + kend) ** (-1.0) * (1.0 + kt * r * (s + kd) ** (-1.0) * (1.0 - ((kt) * (s + kt + kd) ** (-1.0)) ** n)))
        return value

    def ToBeRun2(self, i):
        return talbot(partial(self.F, \
                               A=(self.param["A"] * ones(self.num))[i], \
                               n=(self.param["n"] * ones(self.num))[i], \
                               r=(self.param["r"] * ones(self.num))[i], \
                               kend=(self.param["kend"] * ones(self.num))[i], \
                               kd=(self.param["kd"] * ones(self.num))[i], \
                               kt=(self.param["kt"] * ones(self.num))[i]), \
                       self.param["x"][i], \
                       0.0, \
                       ntrap=30)
