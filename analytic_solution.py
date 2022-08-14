# -*- coding: utf-8 -*-
"""
Created on Sun May 29 17:26:38 2022

@author: Richard
"""

import matplotlib.pyplot as plt
import numpy as np
    
# TODO: fix analytic solution for cR
# TODO: analytic solution now works with initial concentrations, but initial time has to be 0 still
def analytic_solution(t, c0, k):
    t = np.array(t).flatten()
    c0 = np.array(c0).flatten()
    k = np.array(k).flatten()
    
    args = (t, c0, k)
    return t, np.array([cAt(*args), cSt(*args), cTt(*args), cRt(*args)])


#TODO: finish this function (can be simplified). 
# This function would be simpler if the analytic solution worked with all starting times
def analytic_solution_reinjection(t, c0, k, cA_reinject_start, cA_reinject_end, n_reinject):
    

    args = (t, c0, k)
    t_remain = t.copy()
    partial_times = []
    partial_results = []
    for n in range(n_reinject):
        solution = np.array([cAt(*args), cSt(*args), cTt(*args), cRt(*args)])
        
        cA = solution[0, :]
        injection_index = np.argmin((cA - cA_reinject_start)**2)
        
        t_inject = t_remain[injection_index]
        partial_time = t_remain[:injection_index]
        partial_result = solution[:, :injection_index]
        
        partial_times.append(partial_time)
        partial_results.append(partial_result)
        
        t_remain = t_remain[injection_index:]
        c0 = partial_result[:, -1]
        c0[0] = cA_reinject_end
        args = (t_remain - t_inject, c0, k)
        
    
    solution_remain = np.array([cAt(*args), cSt(*args), cTt(*args), cRt(*args)])
    
    partial_times.append(t_remain)
    partial_results.append(solution_remain)   
    t_sol = np.hstack(partial_times)
    result = np.hstack(partial_results)
    return t_sol, result



def cAt(t, c0, k):
    t0 = t[0]
    cA0, cS0, cT0, cR0 = c0
    k1, k2, k3, k4, k5 = k
    return cA0 * np.exp(-(k1 + k2 + k3) * (t-t0))
   

def cSt(t, c0, k):
    return _cSt_homo(t, c0, k) + _cSt_part(t, c0, k)
    

def cTt(t, c0, k): 
    return _cTt_homo(t, c0, k) + _cTt_part(t, c0, k)    

    
def cRt(t, c0, k):    
    return _cRt_homo(t, c0, k) + _cRt_part(t, c0, k)




def _cSt_homo(t, c0, k):
     t0 = t[0]
     cA0, cS0, cT0, cR0 = c0
     k1, k2, k3, k4, k5 = k
     
     const = cS0 - cA0 * k1/(k4-k1-k2-k3) * np.exp((k1 + k2 + k3) * t0)
     cT_homo = const * np.exp(-k4 * t)
     return cT_homo


def _cSt_part(t, c0, k):
     t0 = t[0]
     k1, k2, k3, k4, k5 = k
     k123 = k1 + k2 + k3
     cA0, cS0, cT0, cR0 = c0
     
     const_t = cA0 * k1/(k4-k123) * np.exp((k4-k123)*t + k123*t0)
     return const_t * np.exp(-k4*t)

    

def _cTt_homo(t, c0, k):
    t0 = t[0]
    cA0, cS0, cT0, cR0 = c0
    k1, k2, k3, k4, k5 = k
    
    const = cT0 - cA0 * k3/(k5-k1-k2-k3) * np.exp((k1 + k2 + k3) * t0)
    cT_homo = const * np.exp(-k5 * t)
    return cT_homo


def _cTt_part(t, c0, k):
    t0 = t[0]
    k1, k2, k3, k4, k5 = k
    k123 = k1 + k2 + k3
    cA0, cS0, cT0, cR0 = c0
    
    const_t = cA0 * k3/(k5-k123) * np.exp((k5-k123)*t + k123*t0)
    return const_t * np.exp(-k5*t)




def _cRt_homo(t, c0, k):
    cA0, cS0, cT0, cR0 = c0
    
    cR_homo = cR0 - _cRt_part(np.array([0]), c0, k)
    return cR_homo

    

def _cRt_part(t, c0, k):
    t0 = t[0]
    cA0, cS0, cT0, cR0 = c0
    k1, k2, k3, k4, k5 = k
    k123 = k1 + k2 + k3
    

    
    cA_influx = k2 * cA0 * np.exp(-k123 * (t-t0))/(-k123)
    cS_influx = k4 * ((cS0 - cA0*k1/(k4-k123)*np.exp(k123*t0))*np.exp(-k4*t) /(-k4) + cA0*k1/(k4-k123)*np.exp(-k123*(t-t0)) / (-k123))
    cT_influx = k5 * ((cT0 - cA0*k3/(k5-k123)*np.exp(k123*t0))*np.exp(-k5*t) /(-k5) + cA0*k3/(k5-k123)*np.exp(-k123*(t-t0)) / (-k123))
    
    cR_part = cA_influx + cS_influx + cT_influx
    return cR_part











