# -*- coding: utf-8 -*-
"""
Created on Thu May 26 16:32:39 2022

@author: Richard 
"""

# DONE: analytic solution should be evaluated and plotted finer, no matter what the
# resolution of the numeric solutions is

import numpy as np
import matplotlib.pyplot as plt
# plt.close("all")

from odeEE import odeEE
from odeIE import odeIE
from odeRK import odeRK
from odeIELinear import odeIELinear

from reaction_model_func import ReactionModel
from analytic_solution import analytic_solution as asol
from constants import TOTAL_TIME, N_TIME_STEPS, cA0, cS0, cT0, cR0, k1, k2, k3, k4, k5, coeff_matrix


t_num = np.linspace(0, TOTAL_TIME, N_TIME_STEPS)
t_anal = np.linspace(0, TOTAL_TIME, 1000)
y0 = np.array([cA0, cS0, cT0, cR0])
k = np.array([k1, k2, k3, k4, k5])

mfunc = ReactionModel().reaction_model_func
mfunc2 = ReactionModel().reaction_model_func
mfunc3 = ReactionModel().reaction_model_func

methods = {
    "Explicit Euler": odeEE(mfunc, t_num, y0), 
    #"General Implicit Euler": odeIE(mfunc2, t_num, y0), 
    #"Linear Implicit Euler": odeIELinear(coeff_matrix, t_num, y0), 
    #"Runge Kutta": odeRK(mfunc3, t_num, y0),
    #"Analytic Solution": asol(t_anal, y0, k)
}


components = ["c(A)", "c(S)", "c(T)", "c(R)"]

fig, axs = plt.subplots(4, 1, figsize=(10, 10))
for method_name, solution in methods.items():
    t, y = solution
    for row in range(y0.size):
        ci = y[row, :]
        component = components[row]
        
        ax = axs[row]
        ax.plot(t.flatten(), ci, label=f"{component} {method_name}")
        ax.set_ylabel(component)
        ax.set_xlabel("time [s]")
        ax.grid(True)
    print(f"{method_name} c(A): {y[0, -1]}, c(S): {y[1, -1]}, c(T): {y[2, -1]}, c(R): {y[3, -1]}")

axs[-1].legend(loc='lower center', bbox_to_anchor=(0.5, -1), ncol=3, fancybox=True, shadow=True)
fig.suptitle("Concentration vs time comparison over the system's reaction")
fig.tight_layout()
fig.savefig("results_2.png")
