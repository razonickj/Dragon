'''
This is where the ODE is actually solved by the user.
'''

#import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Data_Architecture as da



#------
#Setup
def x1(DataSet: da.DragonDataModule):
    #get the previous time value index (need previous time given definition used in update function)
    t = DataSet.CurrentIndex - 1

    #grab the index for the variable(s) of interest
    x1_ind = DataSet.DynamicVarNames.index('x1')

    #write out the equation for variables first derivative
    #x1 + 1 = f(x)
    out = 1 + DataSet.DynamicData[t][x1_ind]

    #return the 
    return out

def stopcriteria(DataSet: da.DragonDataModule):
    #This function should return true when you want to stop the simulation
    if DataSet.CurrentIndex > 1000:
        out = True
    else:
        out = False
    return out

dyn_functions = {'x1': x1}
#param_functions = {'alpha': (lambda dataObj: dataObj.Time[dataObj.CurrentIndex - 1])}
intial_dict = {'x1': 25,
               'time': 0}
Dataset = da.DragonDataModule(dyn_functions, initial_values = intial_dict)
odesolver = da.DragonSolver('Euler', stopcriteria, 0.01)


#------
#run the ode solver
odesolver.Solve(Dataset)

outdata = Dataset.get_data()

#save the output data in a csv file
outdata.to_csv('dynamics_sim.csv')

#------
#compute for the solved function


#------
#plot the data
fig, ax = plt.subplots()
ax.plot(np.array(outdata['Time']), np.array(outdata['x1']))
plt.xlabel("Time (s)")
plt.ylabel("X1")

print(outdata)
plt.show()