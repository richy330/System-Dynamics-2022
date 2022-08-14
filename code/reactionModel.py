# -*- coding: utf-8 -*-
"""
Created on Thu May 26 18:16:04 2022

@author: Richard
@author: Carmen
"""

__all__ = ["ReactionModel", "InjectionTermination", "InjectionStateModifier"]

import numpy as np

from constants import cA0, cA_REINJECT_START, cA_REINJECT_END, coeff_matrix, N_REINJECTIONS


class ReactionModel:
    
    #%% Deprecated since not working
    # reinjection_counter = 0
    
    # def model_func_injection(self, t, y):
    #     fy = coeff_matrix @ y
    #     cA = y[0][0]
    #     print(f"current cA: {cA}")
    #     if cA <= REINJECTION_CONC_A and self.reinjection_counter < N_REINJECTIONS:
    #         y[0][0] = INITIAL_cA # re-inject A to its initial c
    #         self.reinjection_counter += 1
    #         print("reinjected!")
    #         print(f"new cA: {y[0][0]}")
        
    #     return fy
    #%%
    
    def model_func(self, t, y):
        return coeff_matrix @ y    


    
class InjectionTermination():
    """ 
    Class serving as event-calable utilized by ODE-solvers. Has 'terminal'-attribrute set to 'True'
    and returns the difference between c_i(A) and c_reinject(A), forcing a termination of integration
    by the solver if c_i(A) is coming close to the reinjection concentration.
    """

    
    def __init__(self):
        self.terminal = True
        
        
        
    def __call__(self, t, y):
        """
        Event function utilized by ODE-Solvers. Return the difference between c_i(A) and c_reinject(A).
        """
        return y[0] > cA_REINJECT_START
    
    
    
class InjectionStateModifier():
    """ 
    Class serving as event-calable utilized by ODE-solvers. Has 'state_modifier'-attribrute set to 'True'
    and returns the difference between c_i(A) and c_reinject(A), forcing a change in the state-vector
    ('reinjection of component A')
    by the solver if c_i(A) is coming close to the reinjection concentration.
    """

    
    def __init__(self):
        self.state_modifier = True
        self.injection_count = 0
        
        
        
    def __call__(self, t, y):
        """
        Event function utilized by ODE-Solvers. Returns False if c_i(A) falls under c_reinject(A).
        
        Solvers recognize triggered events when calling the event returns a value close to 0, which
        the boolean 'False' fulfills.
        """
        return y[0] > cA_REINJECT_START
    
    
    
    def modify_state(self, t, y):
        """
        Event function utilized by ODE-Solvers after the event was triggered.
        Adjusts the state vector to reset c(A) to c0(A) if the maximum number of reinjections
        was not yet met.
        """
        
        if self.injection_count < N_REINJECTIONS:
            y = np.array(y).copy()
            y[0] = cA_REINJECT_END
            self.injection_count += 1
        return y
    

