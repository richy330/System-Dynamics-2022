# -*- coding: utf-8 -*-
"""
Created on Thu May 26 16:32:39 2022

@author: Richard 
"""
# cA0 = 0.185, 0.2, 0.17, 0.19, 0.180 for group IDs 1 to 5


import numpy as np
import matplotlib.pyplot as plt

from odeEE import odeEE
from reaction_model_func import reaction_model_func as mfunc

TOTAL_TIME = 500
TIME_STEPS = 100

t = np.linspace(0, TOTAL_TIME, TIME_STEPS)
y0 = np.array([0.185, 0, 0, 0])

t, y = odeEE(mfunc, t, y0)




fig, ax = plt.subplots(4, 1)
for row in range(y.shape[0]):
    c = y[np.newaxis, row,:]
    ax[row].plot(t, c, 'rx')
