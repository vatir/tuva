import Data
from numpy import inf, zeros
from collections import OrderedDict
from FuncDesigner import oovar


if Data.model_init == False:
    Data.constrained = True
    
    Data.param = OrderedDict()
    Data.param['signal1'] = 100.0
    Data.param['signal2'] = 100.0
    Data.param['signal3'] = 100.0
    Data.param['signal4'] = 100.0
    Data.param['signal5'] = 100.0
    Data.param['signal6'] = 100.0
    Data.param['width1'] = 3.0
    Data.param['width2'] = 3.0
    Data.param['width3'] = 3.0
    Data.param['width4'] = 3.0
    Data.param['width5'] = 3.0
    Data.param['width6'] = 3.0
    Data.param['position1'] = 0.5
    Data.param['delta1'] = 5.0
    Data.param['delta2'] = 5.0
    Data.param['delta3'] = 5.0
    Data.param['delta4'] = 5.0
    Data.param['delta5'] = 5.0
    Data.param['slope'] = 0.01
    Data.param['offset'] = 0.01
    

    Data.param_upper_bounds = OrderedDict()
    Data.param_upper_bounds = {
                  'signal1' : 100000.0,
                  'signal2' : 100000.0,
                  'signal3' : 100000.0,
                  'signal4' : 100000.0,
                  'signal5' : 100000.0,
                  'signal6' : 100000.0,
                  'width1' : 50.0,
                  'width2' : 50.0,
                  'width3' : 50.0,
                  'width4' : 50.0,
                  'width5' : 50.0,
                  'width6' : 50.0,
                  'position1' : 20.0,
                  'delta1' : 10.0,
                  'delta2' : 10.0,
                  'delta3' : 20.0,
                  'delta4' : 20.0,
                  'delta5' : 20.0,
                  'slope' : 1.0,
                  'offset' : 100.0
                              }
    Data.param_lower_bounds = OrderedDict()
    Data.param_lower_bounds = {
                  'signal1' : 0.0,
                  'signal2' : 0.0,
                  'signal3' : 0.0,
                  'signal4' : 0.0,
                  'signal5' : 0.0,
                  'signal6' : 0.0,
                  'width1' : 0.01,
                  'width2' : 0.01,
                  'width3' : 0.01,
                  'width4' : 0.01,
                  'width5' : 0.01,
                  'width6' : 0.01,
                  'position1' : -20.0,
                  'delta1' : 2.0,
                  'delta2' : 6.0,
                  'delta3' : 6.0,
                  'delta4' : 6.0,
                  'delta5' : 6.0,
                  'slope' : -5.0,
                  'offset' : -50.0
                              }

    Data.use_individual_params = OrderedDict()
    for key in Data.param:
        Data.use_individual_params[key]=False

    Data.model_init = True


def func(param, return_oofunvalue=False):
    

    lorentz1 = (param['signal1']*param['width1']/3.1416)/((param['x']-param['position1'])**2.0+param['width1']**2.0)

    position2=param['position1']+param['delta1']
    
    lorentz2 = (param['signal2']*param['width2']/3.1416)/((param['x']-position2)**2.0+param['width2']**2.0)
 
    position3 = position2+param['delta2']
    
    lorentz3 = (param['signal3']*param['width3']/3.1416)/((param['x']-position3)**2.0+param['width3']**2.0)
    
    position4 = position3+param['delta3']
    
    lorentz4 = (param['signal4']*param['width4']/3.1416)/((param['x']-position4)**2.0+param['width4']**2.0)
 
    position5 = position4+param['delta4']
    
    lorentz5 = (param['signal5']*param['width5']/3.1416)/((param['x']-position5)**2.0+param['width5']**2.0)
    
    position6 = position5+param['delta5']
    
    lorentz6 = (param['signal6']*param['width6']/3.1416)/((param['x']-position6)**2.0+param['width6']**2.0)
    
        
    return lorentz1+lorentz2+lorentz3+lorentz4+lorentz5+lorentz6+param['slope']*param['x']+param['offset']