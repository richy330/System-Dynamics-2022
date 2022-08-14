import numpy as np

nan = float('nan')


k1 = 0.007
k2 = 0.0108
k3 = 0.0027
k4 = 0.0099
k5 = 0.0163

cA0 = 0.185
cT0 = 0.0
cS0 = 0.0
cR0 = 0.0

cA_REINJECT_START = 0.5 * cA0
cA_REINJECT_END = cA0
T_START = 0
T_END = 500
N_TIME_STEPS = 100
N_REINJECTIONS = 3


coeff_matrix = np.array(
    [
        [-(k1+k2+k3),    0,   0, 0],
        [     k1,      -k4,   0, 0],
        [     k3,        0, -k5, 0],
        [     k2,       k4,  k5, 0]
    ]
)


