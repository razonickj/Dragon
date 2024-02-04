import numpy as np
from matplotlib import pyplot as plt
import graph_method_functions as gmf
import special_biochem_functions as sbf
import pandas as pd
from scipy.optimize import curve_fit

#test the interpolation function
x = np.linspace(0,5, 5)
h_line = 12.221
y = x*5
ans_int = gmf.find_abscissa_interp(x, y, h_line) #returns a list
ans = h_line/5
#uncomment to see output
#print(f"The interpolator found the intersection at: {ans_int[0]}") #need to get the number out of the list
#print(f"The actual answer is: {ans}")

#testing how it works at finding multiple values with noise
#y = np.random.normal(0, 0.2, len(x)) + x #noise based just to check stability
y = x
h_lines = np.linspace(0.25, 3.25, 4)
xp_vals = gmf.find_mult_intersect(x,y,h_lines)
#uncomment to see output
# print(f"Expected values: {h_lines}")
# print(f"The values found were: {xp_vals}")

#Test the fitting function.
x_free = np.linspace(1, 20, 1000)
#calculate x_bar but with some noise
x_bar = sbf.n_independant_identical_binding(x_free, 4, 2.68) + np.random.normal(0, 0.03, len(x_free))
#plt.plot(x_free, x_bar)
#plt.show()
params, covar = curve_fit(sbf.n_independant_identical_binding, x_free, x_bar)
print(params)

#Test some of the conversions
x_bar = 3.5
m_tot = 10
x_free = 3.1

x_tot = sbf.convert_ligand_concentration('X_total', X_bar = x_bar, X_free = x_free, M_total = m_tot)
x_b1 = sbf.convert_ligand_concentration('X_bound', M_total = m_tot, X_bar = x_bar)
x_b2 = sbf.convert_ligand_concentration('X_bound', X_total = x_tot, X_free = x_free)
#test with numpy array
x_free = np.linspace(1,10,10)
x_bar = 25 - x_free
x_tot = sbf.convert_ligand_concentration('X_total', X_free = x_free, X_bar = x_bar, M_total = 1)
# print(x_b1)
# print(x_b2)
# print(x_tot)

#test the plotting function (uncomment to see it in action)
# gmf.plot_mult(x_bar, x_free, 'r', 'X free', 'scatter',
#               x_bar, x_tot, 'g--', 'X total', 'line',
#               'BS plot', 'X bar', 'X Concentration')

#print done

#test the function that yeilds the closest value
aray = np.linspace(1, 100, 100)
close_targ = gmf.clostest_val(aray, 57.23)
print(close_targ)

print('Done')
