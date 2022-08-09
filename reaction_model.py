# -*- coding: utf-8 -*-
"""
Created on Thu May 26 18:16:04 2022

@author: Richard
@author: Carmen
"""
from constants import coeff_matrix, INITIAL_cA, N_REINJECTIONS, REINJECTION_CONC_A

class ReactionModel:
    
    reinjection_counter = 0
    
    def model_func_injection(self, t, y):
        fy = coeff_matrix @ y
        cA = y[0][0]
        print(f"current cA: {cA}")
        if cA <= REINJECTION_CONC_A and self.reinjection_counter < N_REINJECTIONS:
            y[0][0] = INITIAL_cA # re-inject A to its initial c
            self.reinjection_counter += 1
            print("reinjected!")
            print(f"new cA: {y[0][0]}")
        
        return fy
    
    def model_func_standard(self, t, y):
        return coeff_matrix @ y        