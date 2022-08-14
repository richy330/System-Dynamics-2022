# -*- coding: utf-8 -*-
"""
Created on Thu May 26 16:32:39 2022

@author: Richard 
"""

# DONE: analytic solution should be evaluated and plotted finer, no matter what the
# resolution of the numeric solutions is

# DONE: implement event functions similar to:
# https://github.com/scipy/scipy/blob/651a9b717deb68adde9416072c1e1d5aa14a58a1/scipy/integrate/_ivp/ivp.py


# DONE: Fix analytical solution for cR with cR0 other than 0!

import numpy as np

from odeEE import odeEE
from odeIE import odeIE
from odeRK import odeRK
from odeIELinear import odeIELinear

from analytic_solution import analytic_solution as asol, analytic_solution_reinjection as asol_reinj
from plot_method_results import plot_method_results as plot_results
from reactionModel import ReactionModel as RM, InjectionStateModifier as InjectionEvent
from constants import T_START, T_END, N_TIME_STEPS, cA0, cS0, cT0, cR0, cA_REINJECT_START, cA_REINJECT_END, N_REINJECTIONS, k1, k2, k3, k4, k5, coeff_matrix


T_START = 0

t_num = np.linspace(T_START, T_END, N_TIME_STEPS)
t_anal = np.linspace(T_START, T_END, 1000)

y0 = np.array([cA0, cS0, cT0, cR0])
k = np.array([k1, k2, k3, k4, k5])


mfunc = RM().model_func

#%% numerical and analytical solutions
methods = {
    "Explicit Euler": odeEE(
        mfunc,
        t_num, 
        y0, 
        events=InjectionEvent()
    ), 
    # "General Implicit Euler": odeIE(
    #     mfunc, 
    #     t_num, 
    #     y0, 
    #     events=InjectionEvent()
    # ), 
    # "Linear Implicit Euler": odeIELinear(
    #     coeff_matrix,
    #     t_num, 
    #     y0
    # ), 
    "Runge Kutta": odeRK(
        mfunc, 
        t_num, 
        y0, 
        events=InjectionEvent()
    ), 
    "Analytic Solution": asol_reinj(
        t_anal, 
        y0, 
        k,
        cA_REINJECT_START,
        cA_REINJECT_END,
        n_reinject=N_REINJECTIONS
    ),
    # "Analytic Solution": asol(
    #     t_anal, 
    #     y0, 
    #     k
    # )
}

solution_labels = ["c(A)", "c(S)", "c(T)", "c(R)"]
plot_results(methods, solution_labels)

