# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:52:09 2022

@author: Richard
"""

__all__ = ["odeEE"]


import numpy as np

from constants import nan
from solver_helper_functions import handle_events


def odeEE(fun, t, y0, events=None):
    """Explicit Euler ODE solver"""
    timevalues = np.array(t).flatten()
    timedeltas = np.diff(timevalues)

    y0 = np.array(y0).reshape([-1, 1])
    y = np.full(shape=[y0.size, timevalues.size], fill_value=nan)
    yi = y0
    
    for ti, dt in (iterator:=np.nditer([timevalues[..., :-1], timedeltas], flags=['c_index'])):
        i = iterator.index
        y[:, i, np.newaxis] = yi
        
        termination, yi = handle_events(ti, yi, events)
        if termination:
            break      
        
        fi = fun(ti, yi)
        yi = yi + fi*dt  
        
    # if a break occured, we would include the last value of yi BEFORE the break 2 times
    else:
        y[:, i+1, np.newaxis] = yi
    
    return timevalues[:y.shape[1]], y



    
