
#import all nessicary packages
from matplotlib import pyplot as plt
import math
import pandas as pd
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline

def find_abscissa_interp(x_vals:np.array, y_vals:np.array, h_line):
    '''
    Finds where the data is expected to cross y = h_line (horizontal line).
    Returns a numpy array of x values where it expects to find the cross.
    Only one value of h_line can be passed at a time. Interpolation is used
    to find the intersection.
    
    Inputs:
    x_vals: np.array
        The x values of the data
    y_vals: np.array
        the y values of the data
    h_line: number
        This is the value you want to find the location of the data cross.
        
    Output:
    np.array:
        The x-values associated with corssing the y value h_line according to 
        interpolation of the data.
    '''
    
    #interpolate the data
    solutions = InterpolatedUnivariateSpline(x_vals, y_vals - h_line).roots()
    return solutions
    
def find_mult_intersect(x_vals:np.array, y_vals:np.array, inter_y_vals:np.array):
    '''
    Finds the intersection of the a dataset with multiple y values.
    
    Inputs:
    x_vals: np.array
        The x values of the data
    y_vals: np.array
        the y values of the data
    h_line: np.array
        This is the value you want to find the location of the data cross.
        
    Output:
    list of np.array:
        The x-values associated with crossing at the y values
    '''
    return [find_abscissa_interp(x_vals, y_vals, y_int) for y_int in inter_y_vals]

def clostest_val(aray:np.array, target_val):
    '''
    Finds and returns the value that is closest to target_val in aray
    '''
    idx = (np.abs(aray - target_val)).argmin()
    return aray[idx]

def plot_mult(*args):
    '''
    This function will plot multiple lines for you on one graph given the following input style:
    X, Y, Color_Line_Info ('g--'), legend label, Plot Type, ..., 'Title', X_label, Y_label
    
    Inputs:
    X: numpy.array
        the x data to plot
    Y: numpy.array
        the y data to plot
    ColorLineInfo: string
        A code used to produce different line colors and types (review matplotlib docs for more info)
    Legend_label: string
        This is the label that will appear for that line in the legend.
        Ex: 'Titration 1', 'Macromolecule 1.0uM'
    Plot Type: string
        tells the type of plot to add to the figure ('line' or 'scatter')
    Title: string
        This is the string that will be displayed across the top of the figure.
    X_label: string
        The label that will be displayed below the x axis
    Y_label: string
        The the label that will be displayed across the y-axis
    
    Outputs a matplotlib.pyplot, but does nto return anything.
    '''
    #number of arguments per dataset/number of ending info
    num_arg_dataset = 5
    num_arg_ending = 3
    #check that args is a multiple of 4
    num_args = len(args)
    if (num_args - num_arg_ending) % num_arg_dataset == 0:
        #comute the number of datasets
        num_datasets = math.floor((num_args - num_arg_ending) / num_arg_dataset)
        
        #start the figure window
        fig, ax = plt.subplots()
        
        #loop over each dataset
        #Indexing: i=X, i+1=Y, i+2=colorinfo, i+3=legendname, i+4=plottype
        m = num_arg_dataset #multiple for the extra plots
        for set_i in list(range(num_datasets)):
            #determine the type of pyplot to produce
            plttype = args[m*set_i+4]
            if plttype == 'line':
                plt.plot(args[m*set_i], args[m*set_i+1], 
                         args[m*set_i+2],label=args[m*set_i+3])
            elif plttype == 'scatter':
                plt.scatter(args[m*set_i], args[m*set_i+1], 
                            color=args[m*set_i+2], label=args[m*set_i+3])
            else:
                print(f"Invalid plottype specified. {args[set_i+4]}\nExpected: 'line' or 'scatter'.\nDataset {set_i} was skipped as a result.")

        #set the title and axis info and plot
        plt.title(args[num_args-3]) #set title
        plt.xlabel(args[num_args-2]) #set x label
        plt.ylabel(args[num_args-1]) #set y label
        plt.legend()
        fig.show
        plt.show()
    else:
        print('Invalid number of arguements passed to plot_mult')