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
from numpy import zeros
from numpy import ones, power, e
from scipy.special import gamma, gammaincc

#from Data import ImportOld

def func(param, return_oofunvalue=False):
    #print param
    #ImportOld.calltimes += 1
    #print "I have been called: " + str(ImportOld.calltimes) + " times"
    num = len(param["x"])
    value = (param["A"] * (param["kd"] - param["kend"] + param["kt"] * param["r"] * (ones(num) - power (param["kt"] * param["x"], param["n"]) / power ((param["kd"] - param["kend"] + param["kt"]) * param["x"], param["n"])) + (param["kt"] * param["r"] * (power (param["kt"] * param["x"], param["n"]) * ((param["kd"] - param["kend"] + param["kt"]) * param["x"]) ** -param["n"] * gamma(param["n"]) * gammaincc (param["n"], (param["kd"] - param["kend"] + param["kt"]) * param["x"]) - power (e, (-param["kd"] + param["kend"]) * param["x"]) * gamma(param["n"]) * gammaincc (param["n"], param["kt"] * param["x"]))) / gamma (param["n"]))) / (power (e, param["kend"] * param["x"]) * (param["kd"] - param["kend"]) * (ones(num) + param["n"] * param["r"]))
    return value
