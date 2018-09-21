import Data
from numpy import inf
from collections import OrderedDict
from FuncDesigner import oovars

if Data.model_init == False:
    Data.constrained = True
    
    Data.param = OrderedDict()
    Data.param = {
              's' : 0.0,
              'k1' : 0.0,
              }
    Data.param_upper_bounds = OrderedDict()
    Data.param_upper_bounds = {
              's' : 0.4,
              'k1' : inf,
              }
    Data.param_lower_bounds = OrderedDict()
    Data.param_lower_bounds = {
              's' : -0.2,
              'k1' : 0.0,
              }
    
    Data.use_individual_params = OrderedDict()
    for key in Data.param:
        Data.use_individual_params[key] = False

    Data.model_init = True


from numpy import ones

#from Data import ImportOld

def func(param, return_oofunvalue=False):
    PS = ((param["x"]+param["NCPconc"]+param['k1'])+((param["x"]+param["NCPconc"]+param['k1'])**(2.0)-4*(param["x"]*param["NCPconc"]))**(0.5))/2.0
    return param['s'] * PS / (param['NCPconc'])
