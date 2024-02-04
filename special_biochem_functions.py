'''
This file contains many specialty functions that are primarily used in biochem
'''
import numpy as np
import graph_method_functions as gmf

def n_independant_identical_binding(x:np.array, n, k):
    '''
    Function associated with determining the average number of bound molecules
    per macromolecule.
    
    Input:
    n: number
        The integer of the total number of binding sites
    k: number
        The kappa for the binding site constants
    x: np.array
        The free ligand concentration to feed in
    '''
    return (n*k*x)/(1+k*x)

def convert_ligand_concentration(solve_lig = 'X_total', **kwargs):
    '''
    This solves for different formations of ligand concentration.
    Ex: convert_ligand_concentration('X_total', 'X_free' = x_free, 'X_bar' = x_bar, 'M_total' = m_tot)
    This will solve for x_total given x_bar, x_free, and M_tot.
    This is designed to return none if you do not provide the specifications required
    Inputs:
    solve_lig: string
        This is a keyword for the value to convert to.
        Acceptable values include: 'X_total', 'X_free', 'X_bound', 'X_bar'.
        Values passed can be numbers of np.array of same length.
    kwargs: keys are strings of acceptible solve_lig type and the values are numpy arrays
        Ex: 'X_free' = x_free_array
    
    Output:
    numpy.array:
        This is the variable output asked for
    '''
    #List all accepted solving types
    acceptable_inputs = ['X_total',
                         'X_free',
                         'X_bound',
                         'X_bar']
    
    #get the keys that were passed to know what variable are specified
    kss = kwargs.keys()
    vars_passed = list(kwargs.keys())
    
    #check that the conversion was valid
    if solve_lig not in acceptable_inputs:
        raise Exception(f"Invalid input to convert_ligand_concentration for solve_lig. Input {solve_lig} was passed. Acceptable values are: {acceptable_inputs}\n")
    
    #check the kwargs were passed okay
    accept_keys = acceptable_inputs.append('M_total')
    # for var_name in vars_passed:
    #     if var_name not in accept_keys:
    #         raise Exception(f"{var_name} is not an acceptable input type. Acceptable inputs are: {acceptable_inputs}")
    
    
    #determine which quantity will be solved for
    if solve_lig == 'X_total':
        #check if X_bound or X_bar was specified
        if 'X_bound' in vars_passed:
            #use total = bound + free
            out = kwargs.get('X_bound') + kwargs.get('X_free')
        elif 'X_bar' in vars_passed:
            #use total = M*Bar + free
            out = kwargs.get('X_free') + kwargs.get('M_total')*kwargs.get('X_bar')
    elif solve_lig == 'X_free':
        if 'X_bound' in vars_passed:
            #free  = total - bound
            out = kwargs.get('X_total') - kwargs.get('X_bound')
        elif 'X_bar' in vars_passed:
            #free = total - M*Bar
            out =kwargs.get('X_total') - kwargs.get('M_total')*kwargs.get('X_bar')
    elif solve_lig == 'X_bound':
        if 'X_bar' in vars_passed:
            #bound = M * Bar
            out = kwargs.get('M_total') * kwargs.get('X_bar')
        elif 'X_free' in vars_passed:
            #bound = total - free
            out = kwargs.get('X_total') - kwargs.get('X_free')
    elif solve_lig == 'X_bar':
        if 'X_bound' in vars_passed:
            #bar = bound / M
            out=kwargs.get('X_bound') / kwargs.get('M_total')
        elif 'X_free' in vars_passed:
            #bar = (total - free)/M
            out = (kwargs.get('X_total') - kwargs.get('X_free')) / kwargs.get('M_total')
    else:
        out = None
        print('Ligand type was not found...\n')
        
    return out

def titrate_macromolecule_sigM(MT1, XT1: np.array, dS1: np.array, MT2, XT2:np.array, dS2:np.array):
    '''
    This function assumes:
    No change in oligermerization state and is the simple case of titrating the macromolecule.
    The signal is coming from the macromolecule.
    '''