# -*- coding: utf-8 -*-
"""
Created on Thu May 26 18:16:04 2022

@author: Richard
"""
import numpy as np

k1 = 0.007
k2 = 0.0108
k3 = 0.0027
k4 = 0.0099
k5 = 0.0163

coeff_matrix = np.array(
    [
        [-(k1+k2+k3), 0,   0, 0],
        [k1,        -k4,   0, 0],
        [k3,          0, -k5, 0],
        [k2,         k4,  k5, 0]
    ])

def reaction_model_func(t, y):
    fy = coeff_matrix @ y
    return fy