# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 17:21:05 2022

@author: Richard
"""

import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor


from plot_method_results import plot_method_results


sheet_names = [f'Group {n}' for n in range(1, 6)]


raw_data = pd.read_excel(r"../data/data.xlsx", sheet_name=sheet_names, header=1, skiprows=lambda row: row==2)
data_group1 = raw_data["Group 1"].to_numpy()

t_exp = data_group1[:, 0]
cA_exp_grp1 = np.full(t_exp.shape, data_group1[0, 1])
cR_exp_grp1 = data_group1[:, 4]

cA_initial = [raw_data[group_name].to_numpy()[0, 1] for group_name in sheet_names]
cA_initial_extended = np.hstack([np.full(t_exp.shape, cA_initial[i]) for i in range(len(sheet_names))])


t_train = np.hstack([t_exp for _ in sheet_names[1:]])
cA_train = cA_initial_extended[15:]
cR_train = np.hstack([raw_data[group_name].to_numpy()[:, 4] for group_name in sheet_names[1:]])

cA_pred = cA_initial_extended[:15]

t_cA_train = np.vstack([t_train, cA_train]).T
t_cA_pred = np.vstack([t_exp, cA_pred]).T


nn = MLPRegressor(hidden_layer_sizes=[50, 50], max_iter=400, alpha=0.0001)
nn.fit(t_cA_train, cR_train)

cR_pred = nn.predict(t_cA_pred)


results = {
    "Group 1 experimental": (t_exp, cR_exp_grp1),
    "Group 1 neural network prediction" : (t_exp, cR_pred)
    }

solution_labels = ['c(R)']

plot_method_results(results, solution_labels)


