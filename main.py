# -*- coding: utf-8 -*-
"""
Created on Thu May 26 16:32:39 2022

@author: Richard 
"""
# cA0 = 0.185, 0.2, 0.17, 0.19, 0.180 for group IDs 1 to 5


import numpy as np
import matplotlib.pyplot as plt
# plt.close("all")

from odeEE import odeEE
from odeIE import odeIE
from odeRK import odeRK
from odeIELinear import odeIELinear

from reaction_model_func import reaction_model_func as mfunc
from analytic_solution import analytic_solution as asol


TOTAL_TIME = 500
N_TIME_STEPS = 50

k1 = 0.007
k2 = 0.0108
k3 = 0.0027
k4 = 0.0099
k5 = 0.0163

cA0 = 0.185
cT0 = cS0 = cR0 = 0

coeff_matrix = np.array(
    [
        [-(k1+k2+k3), 0,   0, 0],
        [k1,        -k4,   0, 0],
        [k3,          0, -k5, 0],
        [k2,         k4,  k5, 0]
    ]
)

t = np.linspace(0, TOTAL_TIME, N_TIME_STEPS)
y0 = np.array([cA0, cS0, cT0, cR0])
k = np.array([k1, k2, k3, k4, k5])


methods = {
    "Explicit Euler": odeEE(mfunc, t, y0), 
    "General Implicit Euler": odeIE(mfunc, t, y0), 
    #"Linear Implicit Euler": odeIELinear(coeff_matrix, t, y0), 
    #"Runge Kutta": odeRK(mfunc, t, y0),
    "Analytic Solution": asol(t, y0, k)
}


components = ["c(A)", "c(S)", "c(T)", "c(R)"]

fig, axs = plt.subplots(4, 1)
for method_name, solution in methods.items():
    t, y = solution
    for row in range(y0.size):
        ci = y[row, :]
        component = components[row]
        
        ax = axs[row]
        ax.plot(t.flatten(), ci, label=f"{component} {method_name}")
        ax.set_ylabel(component)
        ax.set_xlabel("time [s]")
        ax.legend(loc="upper right")
        ax.grid(True)        
        
    print(f"{method_name} c(A): {y[0, -1]}")
        
        