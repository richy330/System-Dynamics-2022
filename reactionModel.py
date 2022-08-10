# -*- coding: utf-8 -*-
"""
Created on Thu May 26 18:16:04 2022

@author: Richard
@author: Carmen
"""

__all__ = ["ReactionModel", "injection_termination"]


from constants import coeff_matrix, INITIAL_cA, N_REINJECTIONS, REINJECTION_CONC_A


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
    
    def model_func_standard(self, t, y):
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
        return y[0] > REINJECTION_CONC_A
    
injection_termination = InjectionTermination()