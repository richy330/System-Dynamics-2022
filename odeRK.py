# -*- coding: utf-8 -*-
"""
Created on Sat May 28 14:40:45 2022

@author: Richard
"""


import numpy as np
from scipy.integrate._ivp.ivp import prepare_events


def odeRK(fun, t, y0, events=None):
    """Runge Kutta ODE solver"""
    
    timevalues = np.array(t).flatten()
    timedeltas = np.diff(timevalues)
    
    
    y0 = np.array(y0).reshape([-1, 1])
    y = np.zeros([y0.size, timevalues.size])
    yi = y0
    

    for ti, dt in (iterator:=np.nditer([timevalues[..., :-1], timedeltas], flags=['c_index'])):
        i = iterator.index
        y[:, i, np.newaxis] = yi
        
        k1 = fun(t, yi)
        y_new = yi + dt*k1/2
        k2 = fun(t + dt/2, y_new)
        y_new = y_new + dt*k2/2
        k3 = fun(t + dt/2, y_new)
        y_new = y_new + dt*k3
        k4 = fun(t + dt, y_new)
    
        yi = y_new + dt * 1/6 * (k1 + 2*k2 + 2*k3 + k4)
    
    y[:, i+1, np.newaxis] = yi
    return timevalues, y
