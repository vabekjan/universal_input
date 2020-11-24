# Two files: expected input file + input for multiparameteric
import numpy as np
import h5py
import sys
import os
import shutil
import subprocess


try:
    os.remove('testmp1.h5')
except:
    pass

subprocess.run('./all_combinations.e')

with open('list_of_combinations.dat') as f:
    s = f.read()


print(s)

xxx = 'a\n'+s

print(xxx)

with open('new_list_of_combinations.dat','w') as f:
    f.write(xxx)

print('a multiparam')

subprocess.run(['python3', 'create_universal_HDF5.py', '-i', 'list_of_combinations_ext.dat', '-ohdf5', 'testmp1.h5', '-g', 'inputs'])
# subprocess.run(['python3', 'create_universal_HDF5.py -i list_of_combinations_ext.dat -ohdf5 testmp1.h5 -g inputs'])
# subprocess.run(['python3', 'create_universal_HDF5.py', ['-i', 'list_of_combinations_ext.dat', '-ohdf5', 'testmp1.h5', '-g', 'inputs']])
# python3 create_universal_HDF5.py -i list_of_combinations_ext.dat -ohdf5 testmp1.h5 -g inputs
# https://stackoverflow.com/questions/7152340/using-a-python-subprocess-call-to-invoke-a-python-script