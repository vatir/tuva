"""
func is the function that is being fit to the data

x is the independent variable

"""

from numpy import log

def func(x, param, traits):
    
    return param['amp'] * log(param['b'] * x) + param['c'] + traits["length"]
