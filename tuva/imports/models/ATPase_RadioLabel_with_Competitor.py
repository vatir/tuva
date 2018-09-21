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
              'KmATP'   :   1371.41004902,
              'KCat'    :   0.0928310457138,
              'KdADP'    :   0.0001,
              'KdComp'    :   0.0001
              }
    """
    Data.param = {
              'r1' :  0.4,
              'r2'  : 0.4,
              #'k2' : 0.0,
              'k1A'  : 1.0,
              'kratio' : 1.0,
              'kfactor'  : 1.0,
              }
    """
    Data.param_upper_bounds = OrderedDict()
    Data.param_upper_bounds = {
              'KmATP'   :   1000000000.0,
              'KCat'    :   1000000000.0,
              'KdADP'    :   1000000000.0,
              'KdComp'    :   1000000000.0
              }
    Data.param_lower_bounds = OrderedDict()
    Data.param_lower_bounds = {
              'KmATP'   :   0.0,
              'KCat'    :   0.0,
              'KdADP'    :   0.0,
              'KdComp'    :   0.0
              }

    Data.use_individual_params = OrderedDict()
    for key in Data.param:
        Data.use_individual_params[key] = False

    Data.model_init = True


#from openopt import SNLE
#from FuncDesigner import oovar
#from numpy import ones
#from numpy import zeros

"""
from openopt import GLP
from numpy import array
from FuncDesigner import oovar
from FuncDesigner import oosystem
"""
def lambertw(orig_input):
    print "LambertW:"
    print orig_input
    #ret = lambertwmain(orig_input)
    ret = lambertwmain(orig_input,k=0,tol=10.0**-12)
    #print ret
    return ret

def exp(orig_input):
    #print "exp:"
    #print orig_input
    ret = expmain(orig_input)
    #print ret
    return ret

#from numpy import sqrt
from numpy import array
from numpy import exp as exp
from numpy import log
from numpy import ones
from scipy.special import lambertw as lambertwmain
from numpy import nan_to_num
import numpy
from numpy.random import normal

def func(param, return_oofunvalue=False, snle_style = False):
    debuging = True
    
    if debuging:
        import time
        start_time = time.time()
        
    Very_Small_Array = float(numpy.finfo(numpy.float32).tiny)*ones(len(param['x']))*10.0**0.0*1.0
    
    
    ATPStart    =   param['ATPInitialConc']+Very_Small_Array
    ADPStart    =   param['ADPInitial']
    #ADPStart    =   param['ADPInitial']+ATPStart*0.006
    #ADPStart    =   param['ADPInitial']
    
    Comp        =   param['CompetitorConc']
    ProteinConc =   param['ProteinConc']
    t           =   param['x']

    KmATP       =   param['KmATP']*ones(len(param['x']))
    KCat        =   param['KCat']*ones(len(param['x']))
    KdADP       =   param['KdADP']*ones(len(param['x']))
    KdComp      =   param['KdComp']*ones(len(param['x']))+Very_Small_Array
    
    Vmax        =   KCat*ProteinConc

#    if debuging:
#        print ATPStart
#        print ADPStart
#    
#        print Comp
#        print ProteinConc
#        print t
#    
#        print KmATP
#        print KCat
#        print KdADP
#        print KdComp
#        
#        print Vmax
#
#        print (ADPStart*ATPStart*KdADP*KdComp + ADPStart*Comp*KdADP*KmATP + ADPStart**2*KdComp*KmATP + ADPStart*KdADP*KdComp*KmATP + ATPStart*KdADP*KdComp*t*Vmax)/(ATPStart*KdADP*KdComp + Comp*KdADP*KmATP + ADPStart*KdComp*KmATP + KdADP*KdComp*KmATP)
#        print (ATPStart*KdADP*KdComp + Comp*KdADP*KmATP + ADPStart*KdComp*KmATP + KdADP*KdComp*KmATP)
#        print ATPStart
#        print KdComp
#        print KCat
#        print (ATPStart*KdADP*KdComp)
#        print (Comp*KdADP*KmATP)
#        print (ADPStart*KdComp*KmATP)
#        print (KdADP*KdComp*KmATP)

    Run_Version = 0
    
    if Run_Version==0:
        # Competition with both ADP and ALternate but no changes in ADP over time
        ADP=(ADPStart*ATPStart*KdADP*KdComp + ADPStart*Comp*KdADP*KmATP + ADPStart**2*KdComp*KmATP + ADPStart*KdADP*KdComp*KmATP + ATPStart*KdADP*KdComp*t*Vmax)/(ATPStart*KdADP*KdComp + Comp*KdADP*KmATP + ADPStart*KdComp*KmATP + KdADP*KdComp*KmATP)
        
    if Run_Version==1:
        # Very Complicated (Comp with ADP changing)
        ADP=(ATPStart*KdADP*KdComp - ATPStart*KdComp*KmATP - Comp*KdADP*KmATP*lambertw((KdComp*((-((exp(-1 + (Comp*KdADP)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + (ADPStart*KdComp)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + (KdADP*KdComp)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + KdADP/KmATP - (Comp*KdADP**2)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP) - (ADPStart*KdADP*KdComp)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP) - (KdADP**2*KdComp)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP))*(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*(-1 + (Comp*KdADP)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + (ADPStart*KdComp)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + (KdADP*KdComp)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + KdADP/KmATP - (Comp*KdADP**2)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP) - (ADPStart*KdADP*KdComp)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP) - (KdADP**2*KdComp)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP))*KmATP)/(KdComp*(KdADP - KmATP))))**((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)/(Comp*KdADP))/exp((KdComp*t*Vmax)/(Comp*KmATP)))**((Comp*KdADP)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp))*(-KdADP + KmATP))/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP)) - ATPStart*KdComp*KmATP*lambertw((KdComp*((-((exp(-1 + (Comp*KdADP)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + (ADPStart*KdComp)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + (KdADP*KdComp)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + KdADP/KmATP - (Comp*KdADP**2)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP) - (ADPStart*KdADP*KdComp)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP) - (KdADP**2*KdComp)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP))*(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*(-1 + (Comp*KdADP)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + (ADPStart*KdComp)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + (KdADP*KdComp)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + KdADP/KmATP - (Comp*KdADP**2)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP) - (ADPStart*KdADP*KdComp)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP) - (KdADP**2*KdComp)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP))*KmATP)/(KdComp*(KdADP - KmATP))))**((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)/(Comp*KdADP))/exp((KdComp*t*Vmax)/(Comp*KmATP)))**((Comp*KdADP)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp))*(-KdADP + KmATP))/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP)) - KdADP*KdComp*KmATP*lambertw((KdComp*((-((exp(-1 + (Comp*KdADP)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + (ADPStart*KdComp)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + (KdADP*KdComp)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + KdADP/KmATP - (Comp*KdADP**2)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP) - (ADPStart*KdADP*KdComp)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP) - (KdADP**2*KdComp)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP))*(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*(-1 + (Comp*KdADP)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + (ADPStart*KdComp)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + (KdADP*KdComp)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp) + KdADP/KmATP - (Comp*KdADP**2)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP) - (ADPStart*KdADP*KdComp)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP) - (KdADP**2*KdComp)/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP))*KmATP)/(KdComp*(KdADP - KmATP))))**((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)/(Comp*KdADP))/exp((KdComp*t*Vmax)/(Comp*KmATP)))**((Comp*KdADP)/(Comp*KdADP + ATPStart*KdComp + KdADP*KdComp))*(-KdADP + KmATP))/((Comp*KdADP + ATPStart*KdComp + KdADP*KdComp)*KmATP)))/(KdComp*(KdADP - KmATP))
        ADP=nan_to_num(ADP.real)+Very_Small_Array*normal()*10.0**0.0
    
    if Run_Version==2:
        # Semi Complicated (No comp but ADP changing)
        ADP = (ATPStart*KdADP - ATPStart*KmATP - ATPStart*KmATP*lambertw(-(((KdADP - KmATP)*((-((exp((-(ADPStart*KdADP) + ATPStart*KdADP + ADPStart*KmATP - ATPStart*KmATP)/((ATPStart + KdADP)*KmATP))*(-(ADPStart*KdADP) + ATPStart*KdADP + ADPStart*KmATP - ATPStart*KmATP))/(KdADP - KmATP)))**((ATPStart + KdADP)/ATPStart)/exp((KdADP*t*Vmax)/(ATPStart*KmATP)))**(ATPStart/(ATPStart + KdADP)))/((ATPStart + KdADP)*KmATP))) - KdADP*KmATP*lambertw(-(((KdADP - KmATP)*((-((exp((-(ADPStart*KdADP) + ATPStart*KdADP + ADPStart*KmATP - ATPStart*KmATP)/((ATPStart + KdADP)*KmATP))*(-(ADPStart*KdADP) + ATPStart*KdADP + ADPStart*KmATP - ATPStart*KmATP))/(KdADP - KmATP)))**((ATPStart + KdADP)/ATPStart)/exp((KdADP*t*Vmax)/(ATPStart*KmATP)))**(ATPStart/(ATPStart + KdADP)))/((ATPStart + KdADP)*KmATP))))/(KdADP - KmATP)
        ADP = nan_to_num(ADP.real)+Very_Small_Array*normal()*10.0**0.0

    if Run_Version==3:
        # Basic (No ADP Change)    
        ADP = ProteinConc*ATPStart*t*KCat/(ATPStart+KmATP)

    if Run_Version==4:
        # ADP changes but no binding to comp or ADP
        ADP = ATPStart - KmATP*lambertw(-(exp(ATPStart/KmATP - (t*Vmax)/KmATP - (ATPStart - KmATP*log(((ADPStart*exp((-ADPStart + ATPStart)/KmATP))/KmATP - (ATPStart*exp((-ADPStart + ATPStart)/KmATP))/KmATP)*KmATP))/KmATP)/KmATP))
        ADP = nan_to_num(ADP.real)
    
    if Run_Version==5:
        # Basic (No ADP Change) with starting ADP
        ADP = (ADPStart*ATPStart + ADPStart*KmATP + ATPStart*t*Vmax)/(ATPStart + KmATP)
        
    if Run_Version==6:
        # Competition with ALternate Only but no changes in ADP over time
        ADP = (ADPStart*ATPStart*KdComp + ADPStart*Comp*KmATP + ADPStart*KdComp*KmATP + ATPStart*KdComp*t*Vmax)/(ATPStart*KdComp + Comp*KmATP + KdComp*KmATP)
        
    if debuging:
        print "Run Time:"
        print time.time() - start_time
        print "ADP:"
        print ADP
        print float(numpy.finfo(numpy.float32).tiny)

    return ADP
