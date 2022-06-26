"""
This part of code just calculates initial field
"""

import scipy.special as sp
import numpy as np


def E_init(E_0, omega, tau, t, t_0, r_gaus,r_bess,r):
    E=E_0*np.exp(-(t-t_0)**2/tau**2)*np.exp(-r**2/r_gaus**2)*np.cos(omega*t)\
    *sp.jn(2,r/r_bess)  
    return E
    