# -*- coding: utf-8 -*-
"""
Created on Fri May 27 17:02:51 2022

@author: Richard
"""

import numpy as np
from scipy.integrate._ivp.ivp import prepare_events




def odeIELinear(coeff_matrix, t, y0, events=None):
    """Implicit Euler solver for linear systems of ODEs. 
    Expects a coefficient matrix instead of a modelfunction, contrary to other ODE solvers.
    """
    
    timevalues = np.array(t).flatten()
    timedeltas = np.diff(timevalues)
    
    y0 = np.array(y0).reshape([-1, 1])
    y = np.zeros([y0.size, timevalues.size])
    yi = y0
    I = np.identity(y0.size)
    
    for ti, dt in (iterator:=np.nditer([timevalues[..., :-1], timedeltas], flags=['c_index'])):
        i = iterator.index
        y[:, i, np.newaxis] = yi
        yi = np.linalg.inv(I - coeff_matrix*dt) @ yi
    
    y[:, i+1, np.newaxis] = yi
    return timevalues, y
