'''
This is where the ODE is actually solved by the user.
'''

#import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import Data_Architecture as da
import function_sets as fs



#------
#Setup
delta_t = 0.05
dyn_functions = {'x1': fs.x1}
#param_functions = {'alpha': (lambda dataObj: dataObj.Time[dataObj.CurrentIndex - 1])}
intial_dict = {'x1': 0,
               'time': 0}
Dataset = da.DragonDataModule(dyn_functions, initial_values = intial_dict)
odesolver = da.DragonSolver('Euler', fs.stopcriteria, delta_t)


#------
#run the ode solver
odesolver.Solve(Dataset)

outdata = Dataset.get_data()

#save the output data in a csv file
outdata.to_csv('dynamics_sim.csv')

#------
#compute for the solved function
t_set = Dataset.Time
x1_actual = fs.analytic_solution(t_set)

#------
#plot the data
plt.style.use('bmh')
fig, ax = plt.subplots()
ax.plot(np.array(outdata['Time']), np.array(outdata['x1']), color='orange',
        label='Approximate Solution')
ax.plot(np.array(t_set), np.array(x1_actual), color='blue',
        label='Analytic Solution')
plt.xlabel("Time (a.u.)")
plt.ylabel("X1")
ax.legend()
ax.set_title(f"Solution with Delta T = {delta_t} a.u.")
plt.show()

#print out the dataframe
print(outdata)

#find number of points that meets error criteria
num_pnts_list = list(range(300,1000))
errorv = 0.001

#compute the analytic value for t=1
an_val = fs.analytic_solution([1.0])
[an_val] = an_val

#needed points
needed_pts = 0

#loop over these (I definately do  not need to go out to 1000 but I am lazy and do not want to write a while loop)
for num_pts in num_pnts_list:
    pts = np.linspace(0,1,num=num_pts)
    delta_t = pts[1] - pts[0]
    Dataset2 = da.DragonDataModule(dyn_functions, initial_values = intial_dict)
    odesolver2 = da.DragonSolver('Euler', fs.stopcriteria2, delta_t)
    odesolver2.Solve(Dataset2)

    #check if it is 0.1 error
    t_1 = Dataset2.CurrentIndex - 1
    [lat_ap] = Dataset2.DynamicData[t_1]
    frac_dif = abs(an_val - lat_ap)/an_val
    if frac_dif < errorv:
        needed_pts = num_pts
        print(f"Number of points needed is: {needed_pts}")
        break
