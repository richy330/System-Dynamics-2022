# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:52:09 2022

@author: Richard
"""

import numpy as np

from helper_functions import prepare_events, evaluate_events
from constants import nan

__all__ = ["odeEE"]

def odeEE(fun, t, y0, events=None):
    """Explicit Euler ODE solver"""
    timevalues = np.array(t).flatten()
    timedeltas = np.diff(timevalues)
    
    events = prepare_events(events)

    y0 = np.array(y0).reshape([-1, 1])
    y = np.full(shape=[y0.size, timevalues.size], fill_value=nan)
    yi = y0
    
    for ti, dt in (iterator:=np.nditer([timevalues[..., :-1], timedeltas], flags=['c_index'])):
        i = iterator.index
        y[:, i, np.newaxis] = yi
        
        if (termination:=evaluate_events(ti, yi, events)):
            break        
        
        fi = fun(ti, yi)
        yi = yi + fi*dt
        
    
    y[:, i+1, np.newaxis] = yi
    return timevalues, y



    
