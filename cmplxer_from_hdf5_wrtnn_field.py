import numpy as np
from fourier_trans_2 import complex_list
import h5py

## Importing field from .hdf5 file 
f1 = h5py.File('initial_field.h5', 'r')
field_list=np.array(f1["Field"]);
tlist=np.array(f1["timelist"]);
rlist=np.array(f1["rlist"]);

f2 = h5py.File("initial_field_compexified.h5","w")
f2["rlist"]=rlist
#grp_real=f2.create_group("real")
#grp_imag=f2.create_group("imag")


field_list_compl=[[0 for i in range(0,len(tlist))] for i in range(0,len(rlist))];
for i in range(0,len(rlist)):
    field_list_compl[i]=complex_list(field_list[i], tlist)[0]
    
        
f2["Field_real"]=np.real(field_list_compl)
f2["Field_imag"]=np.imag(field_list_compl)
        
f1.close()
f2.close()


        

    




