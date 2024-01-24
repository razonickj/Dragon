'''
Written by Nicholas Razo

This file holds the classes for the objects used in solving the odes 
'''
#Import libraries nessisary to perform the computation
import pandas as pd
import numpy as np


#Classes for the architecture of the numeric solver

class DragonDataModule:
    '''
    This class host the following sets of data information about a dynamic system:
        Iteration: list
            This is the number of update steps in that have completed in the ode solver
        CurrentIndex: int
            The index number that corresponds to the next time element
        Time: list
            The time points for which the computation uses to compute the dynamics
        Derivatives: dictionary
            Contains the first derivative of the functions of interest. The keywords
            correspond to the name of the variables for the dynamic system.
        DynamicVarNames: list
            The names of the dynamic variables (keywords of Derivatives)
        UpdateParameters: dictionary
            Contains a dictionary of parameters for the dynamics of the system. By default
            no parameters exist in the system. (Can be temporal updates or not)
        ParameterNames: list
            The names of the parameters for the dynamic system (keywords of UpdateParameters)
        DynamicData: list
            Contains the data of the dynamic variables with respect to time (not the parameters)
        ParameterData: list
            Contains the parameter outputs with respect to time.
        initial_values: dictionary
            Contains the initial values for the dynamic variables and the parameters
        
    '''
    def __init__(self, Derivatives: dict, UpdateParameters = None, **kwargs):
        '''
        Intializes a DragonDataModule object to use for future computation.

        Input:
            Derivatives: dictionary
                Contains the first derivative functions of each variable.
                The keywords are the names of the variables in the dynamics system.
            UpdateParameters: dictionary
                Contains

        Output:
        None
        '''
        #settup the derivatives dictionary
        self.Derivatives = Derivatives
        self.DynamicVarNames = list(self.Derivatives.keys())
        self.DynamicData = []

        #determine if there are parameters passed to the function
        if UpdateParameters == None: 
            self.UpdateParameters = None
            self.ParameterNames = None
            self.ParameterData = None
        else:
            self.UpdateParameters = UpdateParameters
            self.ParameterNames = list(UpdateParameters.keys())
            self.ParameterData = []

        #setup the indexes for the system
        self.CurrentIndex = 0
        self.Iteration = [self.CurrentIndex]
        self.Time = [] #initialized with an empty list

        #determine if any flags were passed
        self.initial_values = kwargs.get('initial_values', None)
        if self.initial_values != None:
            self.set_initial_values(self.initial_values)

    def set_initial_values(self, initial_values: dict):
        '''
        Sets up the initial values for the problem. It also indexes up the function

        Input:
        initial_values: dictionary
            This is a dictionary with the keyword for the variable and the
            value for its initial variable. Note: 'time' must be a variabel intiialized
            in this dictionary or the function will not work.

        Output:
        None
        '''
        #set the initial values
        self.initial_values = initial_values
        try:
            #try to assign all the initial values
            #try for the word time
            varnam = 'time'
            self.Time.append(initial_values.get(varnam))

            #try for the dynamic variables
            self.DynamicData.append([initial_values.get(varnam) for varnam in self.DynamicVarNames])

            #try for the parameters if they exist
            if self.ParameterNames != None:
                self.ParameterData.append([initial_values.get(varnam) for varnam in self.ParameterNames])
        except:
            print(f"Exception has occured in the initialization function. Variable {varnam} was unable to be pulled from the initial values passed")
            raise Exception("The exception occured in the initialzation of the dataset.\n")
        
        #set the index up one for the first pass
        self.increment_index()

    def increment_index(self):
        '''
        Increments the CurrentIndex value by one
        '''
        self.CurrentIndex += 1

    def update_inc_list(self):
        '''
        Adds the increment to the list
        '''
        self.Iteration.append(self.CurrentIndex)

    def update_parameters(self):
        '''
        Updates the parameters through one time increment
        '''
        if self.UpdateParameters != None:
            self.ParameterData.append([self.UpdateParameters.get(pname)(self) for pname in self.ParameterNames])

    def get_data(self):
        '''
        Outputs the dynamic and parameter data as a data frame:
            index|time|dynamic1|dynamic2|...|Parameter1|Parameter2|...
        '''
        #create a blank dataframe
        out_data = pd.DataFrame()

        #For quick access to columns
        dd = np.array(self.DynamicData)
        pard = np.array(self.ParameterData)

        #put the index on there
        out_data = pd.DataFrame({'Index': self.Iteration})

        #put the time in the dataframe
        out_data = pd.concat([out_data, pd.DataFrame({'Time': self.Time})], axis=1)

        #put the dynamic variables in the dataframe
        for dyvar in self.DynamicVarNames:
            cur_i = self.DynamicVarNames.index(dyvar)
            out_data = pd.concat([out_data, pd.DataFrame({dyvar: list(dd[:,cur_i])})], axis=1)

        #put the parameter variables in the dataframe
        if self.UpdateParameters != None:
            for dyvar in self.DynamicVarNames:
                cur_i = self.ParameterNames.index(dyvar)
                out_data = pd.concat([out_data, pd.DataFrame({dyvar: list(pard[:,cur_i])})], axis=1)

        return out_data

class DragonSolver:
    '''
    Progresses the dynamic system through time via a variety of numerical solvers.

    Attributes:
    SolverName: string
        The name of the solver to use: Euler,...
    DynInc: function
        The solver that corresponds the name
    Solve: function
        This is the function that will solve the system
    StopCriteria: function
        This is a function that outputs a True or False depending on the input from the system
    '''

    def __init__(self, SolverName, StopCriteria, deltaT):
        '''
        Initilation of the object
        '''
        self.SolverName = SolverName
        self.StopCriteria = StopCriteria
        self.deltaT = deltaT

        #setup the function that is the specific solver type
        if self.SolverName == 'Euler':
            self.DynInc = self.euler_method
            self.TInc = self.fixed_time_inc 
        else:
            print('No solver was correctly specificified')
            raise Exception(f"Improper Solver Criteria. {self.SolverName} was given.")
        
    def euler_method(self, DataSet: DragonDataModule, variable_name):
        '''
        This is the implimentationof the Euler method
        '''
        cur_var_ind = DataSet.DynamicVarNames.index(variable_name)
        cur_ind = DataSet.CurrentIndex
        slope =  DataSet.Derivatives.get(variable_name)(DataSet)
        return slope * self.TInc(DataSet) + DataSet.DynamicData[cur_ind-1][cur_var_ind]
    
    def fixed_time_inc(self, DataSet: DragonDataModule):
        '''
        This function returns a contant fixed time increment of deltaT
        '''
        return self.deltaT
        
    def Solve(self, DataSet: DragonDataModule):
        #loop over the dataset and compute the methodology
        while not self.StopCriteria(DataSet):
            #update the time dynamics and time
            DataSet.DynamicData.append([self.DynInc(DataSet, vname) for vname in DataSet.DynamicVarNames])
            DataSet.Time.append(self.TInc(DataSet) + DataSet.Time[DataSet.CurrentIndex-1])

            #update the parameters and increment the index
            DataSet.update_inc_list()
            DataSet.update_parameters()
            DataSet.increment_index()

#Testing script portion
# dyn_functions = {'x1': (lambda dataObj,x: dataObj.DynamicData[1] + x),
#                  'x2': (lambda dataObj,x: dataObj.DynamicData[2] + 4 + x)}
# param_functions = {'alpha': (lambda dataObj: dataObj.Time[dataObj.CurrentIndex - 1])}
# intial_dict = {'x1': 1,
#                'x2': 3,
#                'alpha': 0.2,
#                'time': 0}
# Dataset = DragonDataModule(dyn_functions, param_functions, initial_values = intial_dict)
# Dataset.update_parameters()

# print('Done!')