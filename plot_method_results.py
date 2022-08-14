# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 16:05:08 2022

@author: Richard
"""

from itertools import count

import matplotlib.pyplot as plt
plt.close("all")


figsize = (20, 15)


def plot_method_results(methods, solution_label):
    fig, axs = plt.subplots(4, 1, figsize=figsize)
    for method_name, solution in methods.items():
        t, y = solution
        for idx, ci, component_conc_specifier in zip(count(), y, solution_label):

            
            ax = axs[idx]
            ax.plot(t.flatten(), ci, label=f"{component_conc_specifier} {method_name}")
            ax.set_ylabel(component_conc_specifier)
            ax.set_xlabel("time [s]")
            ax.grid(True)
        # print(f"{method_name} c(A): {y[0, -1]}, c(S): {y[1, -1]}, c(T): {y[2, -1]}, c(R): {y[3, -1]}")

    axs[-1].legend(loc='lower center', bbox_to_anchor=(0.5, -1), ncol=3, fancybox=True, shadow=True)
    fig.suptitle("Concentration vs time comparison over the system's reaction")
    fig.tight_layout()
    fig.savefig("results.png")