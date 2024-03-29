# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:52:09 2022

@author: Richard
"""

import numpy as np
from scipy.integrate._ivp.ivp import prepare_events


def odeEE(fun, t, y0, events=None):
    """Explicit Euler ODE solver"""
    timevalues = np.array(t).flatten()
    timedeltas = np.diff(timevalues)
    
    events, is_terminal, event_dir = prepare_events(events)


    y0 = np.array(y0).reshape([-1, 1])
    y = np.zeros([y0.size, timevalues.size])
    yi = y0
    
    for ti, dt in (iterator:=np.nditer([timevalues[..., :-1], timedeltas], flags=['c_index'])):
        i = iterator.index
        y[:, i, np.newaxis] = yi
        fi = fun(ti, yi)
        yi = yi + fi*dt
    
    y[:, i+1, np.newaxis] = yi
    return timevalues, y