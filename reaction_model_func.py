# -*- coding: utf-8 -*-
"""
Created on Thu May 26 18:16:04 2022

@author: Richard
@author: Carmen
"""
from constants import coeff_matrix, INITIAL_cA, REINJECTION_COUNT

class ReactionModel:
    reinjections_current_count = 0
    
    def reaction_model_func(self, t, y):
        fy = coeff_matrix @ y
        cA = y[0][0]
        print(f"current cA: {cA}")
        if cA <= (0.5*INITIAL_cA) and self.reinjections_current_count < REINJECTION_COUNT:
            y[0][0] = INITIAL_cA # re-inject A to its initial c
            self.reinjections_current_count += 1
            print("reinjected!")
            print(f"new cA: {y[0][0]}")
        
        return fy