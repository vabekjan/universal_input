"""
This file computes by initial field it's complexified form 
 and writes as .hdf5 file 
"""

import numpy as np
from field_func import E_init
import h5py

inp0=h5py.File("results.h5","r");
inp=inp0['inputs']
c=299792458.0;
w=np.array(inp["laser_focus_beamwaist_Gaussian"]);
I_0=np.array(inp["laser_focus_intensity_Gaussian"]);
lambd=0.01*np.array(inp["laser_wavelength"]);
omega=2*np.pi*c/lambd;
T=2*np.pi/omega;
tau=np.array(inp["laser_pulse_duration_in_FWHM_Intensity"])*(10**(-15));
T_max=np.array(inp["numerics_length_of_window_for_t_normalized_to_pulse_duration"])*tau;
r_max=np.array(inp["numerics_length_of_window_for_r_normalized_to_beamwaist"])*w;
nr=np.array(inp["numerics_number_of_points_in_r"]);
nt=np.array(inp["numerics_number_of_points_in_t"]);
w_gaus_on_w_bess=2
E_0=np.sqrt(I_0)

rayleigh_width=(omega/c)*(w**2)/2;
rayleigh_time=rayleigh_width/c

tlist=np.arange(-T_max/2,T_max/2,T_max/nt);
rlist=np.arange(0,r_max,r_max/nr);
E_fall_list=[E_init(1,omega,tau,tlist,0,w,w/w_gaus_on_w_bess,rlist[l]) for l in range(0,len(rlist))];


f = h5py.File("initial_field.h5","w")
f["Field"]=E_fall_list
f["timelist"]=tlist
f["rlist"]=rlist
f.close()
inp0.close()
