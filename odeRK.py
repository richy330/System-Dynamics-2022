# -*- coding: utf-8 -*-
"""
Created on Sat May 28 14:40:45 2022

@author: Richard
"""


import numpy as np

from constants import nan
from solver_helper_functions import handle_events



def odeRK(fun, t, y0, events=None):
    """Runge Kutta ODE solver"""
    
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
        
        k1 = fun(t, yi)
        k2 = fun(t + dt/2, yi + dt*k1/2)
        k3 = fun(t + dt/2, yi + dt*k2/2)
        k4 = fun(t + dt, yi + dt*k3)
    
        yi = yi + dt * 1/6 * (k1 + 2*k2 + 2*k3 + k4)     
       
    # if a break occured, we would include the last value BEFORE the break 2 times
    else:
        y[:, i+1, np.newaxis] = yi
    return timevalues, y
