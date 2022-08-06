import numpy as np

TOTAL_TIME = 500
N_TIME_STEPS = 100
REINJECTION_COUNT = 2 #+1 from the first time 
INITIAL_cA = 0.185

k1 = 0.007
k2 = 0.0108
k3 = 0.0027
k4 = 0.0099
k5 = 0.0163

cA0 = 0.185
cT0 = cS0 = cR0 = 0

coeff_matrix = np.array(
    [
        [-(k1+k2+k3),    0,   0, 0],
        [     k1,      -k4,   0, 0],
        [     k3,        0, -k5, 0],
        [     k2,       k4,  k5, 0]
    ]
)