"""
This file calculates Fourier transformation and complexified field
 from some arrays with fields and times
"""

import numpy as np
import h5py
import os

## This part of code calculates discrete Fourier transform  

def four_trans(list, tlist):
    
    # calculating time delay, maximal drequency and frequency difference
    dt=tlist[2]-tlist[1];
    num=len(list);
    max_omega=np.pi/dt;
    delta_omega=2*np.pi/(dt*(num))
    
    om_list=np.arange(-max_omega,max_omega,delta_omega);
    # Cycle over different frequences
    four_trans_list=np.fft.fft(list)
    return [four_trans_list,om_list]


## Function, calculating complexified array
def complex_list(list,tlist):
    
    # Calculating Fourier transform of initial field
    E_fur=four_trans(list,tlist)[0];
    om_list=four_trans(list,tlist)[1];
    E_f_comp=np.fft.ifft(np.array(E_fur)*np.heaviside(-om_list,1/2))
    return  [E_f_comp,tlist]
