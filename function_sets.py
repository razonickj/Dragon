'''
This houses the functions for the ode solver
'''
#import
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Data_Architecture as da
import function_sets as fs


def x1(DataSet: da.DragonDataModule):
    #get the previous time value index (need previous time given definition used in update function)
    t = DataSet.CurrentIndex - 1

    #grab the index for the variable(s) of interest
    x1_ind = DataSet.DynamicVarNames.index('x1')

    #grab x1 value at the time of interest
    x1_t = DataSet.DynamicData[t][x1_ind]

    #write out the equation for variables first derivative
    #x1 + 1 = f(x)
    out = 1 + x1_t

    #return the 
    return out

def stopcriteria(DataSet: da.DragonDataModule):
    #This function should return true when you want to stop the simulation

    #grab the most recent time point
    ind = DataSet.CurrentIndex
    t = DataSet.Time[ind-1]
    if t >= 6:
        out = True
    else:
        out = False
    return out

def stopcriteria2(DataSet: da.DragonDataModule):
    #this function will run till time is 1
    #grab the most recent time point
    ind = DataSet.CurrentIndex
    t = DataSet.Time[ind-1]
    if t >= 1:
        out = True
    else:
        out = False
    return out

def analytic_solution(t_set: list):
    return [(math.exp(t) - 1) for t in t_set]