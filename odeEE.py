# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:52:09 2022

@author: Richard
"""
import numpy as np



def odeEE(fun, t, y0):
    timevalues = np.array(t).reshape([1, -1])
    timedeltas = np.diff(timevalues)
    
    y0 = np.array(y0).reshape([-1, 1])
    y = np.zeros([y0.size, timevalues.size])
    yi = y[:, 0, np.newaxis] = y0
    
    # this may be cleaned up with a better arrangement of when the y-array as being filled with yi
    iterator = np.nditer([timevalues[..., :-1], timedeltas], flags=['c_index'])
    for ti, dt in iterator:
        i = iterator.index
        fi = fun(ti, yi)
        yi = yi + fi*dt
        y[:, i+1, np.newaxis] = yi
    return timevalues, y