# -*- coding: utf-8 -*-
"""
Created on Sat May 28 16:20:40 2022

@author: Richard
"""

import numpy as np
from scipy.integrate._ivp.ivp import prepare_events


N_ITER = 10
TOL_ABS = 0.01
nan = float("nan")


def odeIE(fun, t, y0, events=None):
    """Implicit Euler ODE solver"""
    timevalues = np.array(t).flatten()
    timedeltas = np.diff(timevalues)
    
    y0 = np.array(y0).reshape([-1, 1])
    y = np.zeros([y0.size, timevalues.size])
    yi = y0
    
    for ti, dt in (iterator:=np.nditer([timevalues[..., :-1], timedeltas], flags=['c_index'])):
        i = iterator.index
        y[:, i, np.newaxis] = yi
        yi = y_next_fixed_point_iteration(fun, yi, ti, dt)
    
    y[:, i+1, np.newaxis] = yi
    return timevalues, y


def y_next_fixed_point_iteration(fun, yi, ti, dt):
    fi = fun(ti, yi)
    y_next_new = yi + fi * dt
    yi_next_old = nan
    for _ in range(N_ITER):
        fi = fun(ti, y_next_new)
        y_next_new = y_next_new + fi * dt
        
        
        iterative_change = y_next_new - yi_next_old
        if np.all(np.abs(iterative_change) < TOL_ABS):
            break
        yi_next_old = y_next_new
        
    else:
        print(f"""Conversion issues for fixed point iteration in iterative seach for y_next! 
              y_new - n_old = \n{iterative_change}""")
    return y_next_new