# -*- coding: utf-8 -*-
"""
Created on Sun May 29 17:26:38 2022

@author: Richard
"""


import numpy as np



def analytic_solution(t, c0, k):
    t = np.array(t).flatten()
    c0 = np.array(c0).flatten()
    k = np.array(k).flatten()
    
    args = (t, c0, k)
    return t, np.array([cAt(*args), cSt(*args), cTt(*args), cRt(*args)])



def cAt(t, c0, k):
    cA0, cS0, cT0, cR0 = c0
    k1, k2, k3, k4, k5 = k
    return cA0 * np.exp(-(k1 + k2 + k3) * t)



# TODO: cT0 and cS0 are hardcoded to be 0. This may not always be true and should be changed
# TODO: maybe split all the solutions in homogenous and particular solutions, which may also make some
# solutions simpler 
def cSt(t, c0, k):
    cA0, cS0, cT0, cR0 = c0
    k1, k2, k3, k4, k5 = k
    return cA0 * k1/(k4-k1-k2-k3) * (np.exp(-(k1 + k2 + k3) * t) - np.exp(-k4 * t))
    

    
def cTt(t, c0, k): 
    cA0, cS0, cT0, cR0 = c0
    k1, k2, k3, k4, k5 = k
    return cA0 * k3/(k5-k1-k2-k3) * (np.exp(-(k1 + k2 + k3) * t) - np.exp(-k5 * t))

    
    
def cRt(t, c0, k):    
    return _cRt_homo(t, c0, k) + _cRt_part(t, c0, k)



def _cRt_homo(t, c0, k):
    cA0, cS0, cT0, cR0 = c0
    
    cR_homo = cR0 - _cRt_part(0, c0, k)
    return cR_homo

    

def _cRt_part(t, c0, k):    
    cA0, cS0, cT0, cR0 = c0
    k1, k2, k3, k4, k5 = k
    
    k123 = k1 + k2 + k3
    exp_k123t = np.exp(-k123 * t)
    
    cA_influx = cA0 * k2 * exp_k123t/(-k123)
    cS_influx = cA0 * k1*k4 / (k4 - k123) * (exp_k123t/(-k123) - np.exp(-k4*t)/(-k4))
    cT_influx = cA0 * k3*k5 / (k5 - k123) * (exp_k123t/(-k123) - np.exp(-k5*t)/(-k5))
    
    cR_part = cA_influx + cS_influx + cT_influx
    return cR_part