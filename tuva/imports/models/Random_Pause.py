import Data
from numpy import inf
from collections import OrderedDict
from FuncDesigner import oovar

if Data.model_init == False:
    Data.constrained = False
    
    Data.param = OrderedDict()
    Data.param = {
                  'kt' : 20.0,
                  'kd' : 0.5,
                  'r' : 1.0,
                  'm' : 1.0,
                  'd' : 1.0,
                  'A' : 1.0,
                  'C' : 1.0,
                  }
    Data.param_lower_bounds = OrderedDict()
    Data.param_lower_bounds = {
                  'kt' : 0.0,
                  'kd' : 0.0,
                  'r' : 0.0,
                  'm' : 0.0,
                  'd' : 0.0,
                  'A' : 0.0,
                  'C' : 0.0,
                  }
    Data.param_upper_bounds = OrderedDict()
    Data.param_upper_bounds = {
                  'kt' : inf,
                  'kd' : inf,
                  'r' : inf,
                  'm' : inf,
                  'd' : inf,
                  'A' : inf,
                  'C' : inf,
                  }

    Data.use_individual_params = OrderedDict()
    for key in Data.param:
        Data.use_individual_params[key] = False

    Data.model_init = True


from openopt import SNLE
from FuncDesigner import oovars
from numpy import ones, power, e, array, zeros, ndarray
from scipy.special import gamma, gammaincc


from functools import partial
from funcs.talbot import talbot
from multiprocessing import Pool, cpu_count, current_process



def ToBeRun(self, i):
    return func.ToBeRun2(self, i)

def ToBeRun2(i, param, num):
    return talbot(partial(F, \
                           kt=(param["kt"] * ones(num))[i], \
                           kd=(param["kd"] * ones(num))[i], \
                           r=(param["r"] * ones(num))[i], \
                           m=(param["m"] * ones(num))[i], \
                           d=(param["d"] * ones(num))[i], \
                           A=(param["A"] * ones(num))[i], \
                           C=(param["C"] * ones(num))[i], \
                           dna_length=(param["dna_length"] * ones(num))[i]), \
                           param["x"][i], \
                           0.0, \
                           ntrap=30)
    
def F(s, kt, kd, r, m, d, A, C, dna_length):
    from numpy import ones
    n = (dna_length - d) / m
    value = C / s - A * ((kt * (kd + kt + s) ** (-1.0)) ** n - 1.0) * (kd + kt * r + s) * ((kd + s) ** (2.0) * (n * r + 1)) ** (-1.0)
    return value

class func(ndarray):

    def __new__(self, param, return_oofunvalue=False):
        worker_pool = Pool(2)
        #print param
        #ImportOld.calltimes += 1
        #print "I have been called: " + str(ImportOld.calltimes) + " times"
        from wx import SafeYield
        from time import time
        start_run_time = time()
        self.num = len(param["x"])
        self.return_values = worker_pool.map(partial(ToBeRun2, param=param, num=self.num), xrange(self.num))
        worker_pool.close()
        worker_pool.join()
        print "Time elapsed: %f :" % (time() - start_run_time)
        SafeYield()
        return self.return_values
    
    """
    def __init__(self, param, return_oofunvalue=False):
        worker_pool=Pool(1)
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
        
        print "Time elapsed: %f :" % (time()-start_run_time) + " : Run Param (n): %f" % param["n"]
        SafeYield()
    """


    def __len__(self):
        return len(self.return_values)
    def __sub__(self, other):
        return self.return_values - other
    def __get__(self):
        return self.return_values
    

