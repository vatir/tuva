import Data
from numpy import inf, zeros
from collections import OrderedDict
from FuncDesigner import oovar


if Data.model_init == False:
    Data.constrained = False
    
    Data.param = OrderedDict()
    Data.param = {
                  'none' : 0.0,
                  }
    Data.param_upper_bounds = OrderedDict()
    Data.param_upper_bounds = {
                               'none' : 0.0,
                              }
    Data.param_lower_bounds = OrderedDict()
    Data.param_lower_bounds = {
                              'none' : 0.0,
                              }

    Data.use_individual_params = OrderedDict()
    for key in Data.param:
        Data.use_individual_params[key] = False

    Data.model_init = True


def func(param, return_oofunvalue=False):
    length = len(param[param.keys()[0]])
    return zeros(length)
