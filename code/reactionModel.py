# -*- coding: utf-8 -*-
"""
Created on Thu May 26 18:16:04 2022

@author: Richard
@author: Carmen
"""

__all__ = ["ReactionModel", "InjectionTermination", "InjectionStateModifier"]


from abc import ABC
import numpy as np

from constants import cA_REINJECT_START, cA_REINJECT_END, N_REINJECTIONS, coeff_matrix


class ReactionModel:
    
    def model_func(self, t, y):
        return coeff_matrix @ y    


class Event(ABC):
    """
    Base class for different Event-callables. Defines the __call__-function that returns 'False'
    when c_i(A) falls under c_reinject(A), triggering the event. Actions taken upon events
    are to be defined by the solvers, but can be implemented in the subclasses of 'Event' if the 
    ODE solver supports them.
    """
    
    def __call__(self, t, y):
        """
        Event function utilized by ODE-Solvers. Returns False if c_i(A) falls under c_reinject(A).
        
        Solvers recognize triggered events when calling the event returns a value close to 0, which
        the boolean 'False' fulfills.
        """
        return y[0] > cA_REINJECT_START
    

    
    
class InjectionTermination(Event):
    """ 
    Class serving as event-calable utilized by ODE-solvers. Has 'terminal'-attribrute set to 'True'
    and returns a boolean indicating if c_i(A) > c_reinject(A), forcing a termination of integration
    by the solver if c_i(A) is falling under the reinjection concentration.
    """
    
    def __init__(self):
        self.terminal = True

    
    
    
class InjectionStateModifier(Event):
    """ 
    Class serving as event-calable utilized by ODE-solvers. Has 'state_modifier'-attribrute set to 'True'
    and returns a boolean indicating if c_i(A) > c_reinject(A), forcing a change in the state-vector
    ('reinjection of component A')
    by the solver if c_i(A) is falling under the reinjection concentration.
    """

    
    def __init__(self):
        self.state_modifier = True
        self.injection_count = 0
    
    
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
    

