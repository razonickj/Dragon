#import all nessicary packages
import numpy as np
from matplotlib import pyplot as plt
import graph_method_functions as gmf
import special_biochem_functions as sbf
import pandas as pd
from scipy.optimize import curve_fit
from itertools import product

#import the datafiles of interest
f1_ab = '/Users/nrazo/Documents/Spring2024/Data_ProblemSet3_1ab.csv'
f1_cd = '/Users/nrazo/Documents/Spring2024/Data_ProblemSet3_1cd.csv'
f2_a = '/Users/nrazo/Documents/Spring2024/DP2_b.csv'
f2_b = '/Users/nrazo/Documents/Spring2024/CP2_c.csv'
f3 = '/Users/nrazo/Documents/Spring2024/Data_ProblemSet3_3.csv'

#open each file into its own dataframe
df1a = pd.read_csv(f1_ab)
df1d = pd.read_csv(f1_cd)
df2 = pd.read_csv(f2_a)
df2a = pd.read_csv(f2_b)
df3 = pd.read_csv(f3)





#---------------
#Problem 1
#---------------

#grab the x and y data and plot them
x_tot = np.array(df1a['X_T (uM)'])
x_bar = np.array(df1a['X_Bar'])

#plot the data
# plt.plot(np.log10(x_dat), y_dat)
# plt.xlabel('log(X_T (uM))')
# plt.ylabel('<X>')
# plt.show()

#produce plots that guess
k_list = [1.5, 1.75, 2.0]
n_list = [3, 4, 5]
M_t = 5

#create a list to iterate over
x_tt = np.linspace(0, max(x_tot)-M_t*max(x_bar), 10000)
all_combos = list(product(n_list, k_list))
#loop over each combo
# for n_val, k_val in all_combos:
#     xp_bar = sbf.n_independant_identical_binding(x_tt, n_val, k_val)
#     xp_tot = sbf.convert_ligand_concentration('X_total', M_total =M_t,
#                                               X_bar = xp_bar, X_free = x_tt)
    
#     gmf.plot_mult(x_tot, x_bar, 'r', 'Original Data', 'scatter',
#                 xp_tot, xp_bar, 'g--', 'Model', 'line',
#                 f"Problem 1B Model: N = {n_val}; k = {k_val} (1/uM)", 'X Total (uM)', '<X>')






#---------------
#Problem 2
#---------------
#gather data
x_tot1 = 1000000*np.array(df2['X_T_274 (M)'])
x_tot2 = 1000000*np.array(df2a['X_T_945 (M)'])
m_tot1 = 0.274
q1 = np.array(df2['Quenching_274'])
q2 = np.array(df2a['Quenching_945'])
m_tot2 = 0.945

#plot 1 and 2 curves
gmf.plot_mult(np.log10(x_tot1), q1, 'r', 'Curve 0.274uM', 'scatter',
              np.log10(x_tot2), q2, 'g', 'Curve 0.945uM', 'scatter',
              'Comparing two M', 'X total', 'Quenching')

#points to interpolate on
q_interp = np.linspace(0.4, 0.8, 7)

#grab the interpolated data
x_tot1_interp = gmf.find_mult_intersect(x_tot1, q1, q_interp)
x_tot2_interp = gmf.find_mult_intersect(x_tot2, q2, q_interp)

#compute the x_bar value
x_bar = [(x_tot2_interp[idx]-x_tot1_interp[idx])/(m_tot2-m_tot1) for idx in list(range(len(q_interp)))]

#plot the data
fig, ax = plt.subplots()
plt.scatter(x_bar, q_interp)
plt.xlabel('<X>')
plt.ylabel('Quenching')
plt.show()

#end of the script
print("Done")