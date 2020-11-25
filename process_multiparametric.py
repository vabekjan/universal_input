# Two files: expected input file + input for multiparameteric
import numpy as np
import sys
import os
import shutil
import subprocess


arguments = sys.argv

inputfilenamemp = 'MultiparamInputs.inp'
intermediate_filename = 'multiparam.tmp'

# run_args = ['python3', 'create_universal_HDF5.py', '-i', intermediate_filename]
run_args = ['python3', 'create_universal_HDF5.py']

## Treat arguments
arg_index = arguments.index("-i-reg")
inputfilename = arguments[arg_index+1]
arg_index = arguments.index("-i-mp")
inputfilenamemp = arguments[arg_index+1]
arg_index = arguments.index("-univ-inps")
run_args = run_args + arguments[(arg_index+1):]
print(arguments[(arg_index+1):])

print(run_args)

with open(inputfilenamemp, "r") as InputMP:
    lines = InputMP.readlines()

names = ''
dtypes = ''
units = ''
firstline = True
n_params = 0
for line in lines:
    sep_line = line.split()  # separate the line
    if ((len(sep_line) == 0) or (sep_line[0] == '#') or (sep_line[0] == '##')):
        pass  # print('empty or commented line')
    else:
        n_params = n_params + 1
        names = names + sep_line[0] + '\t'
        dtypes = dtypes + sep_line[1] + '\t'
        units = units + sep_line[2] + '\t'
        if firstline:
            content = sep_line[3] + '\t' + sep_line[4] + '\t' + sep_line[5]
            firstline = False
        else:
            content = content + '\n' + sep_line[3] + '\t' + sep_line[4] + '\t' + sep_line[5]


try:
    os.remove('testfile.dat')
except:
    pass

with open('multiparam_FORTRAN.inp','w') as f:
    f.write(content)


try:
    os.remove('testmp1.h5')
except:
    pass

subprocess.run('./all_combinations.e')
os.remove('multiparam_FORTRAN.inp')

with open('list_of_combinations_FORTRAN.dat') as f:
    content = f.read()
os.remove('list_of_combinations_FORTRAN.dat')

n_lines = content.count('\n')
content = '$multiparametric\t' + str(n_lines) + '\n' + names + '\n' + dtypes + '\n' + units + '\n' + content

with open('new_list_of_combinations2.dat','w') as f_tmp, open(inputfilename,'r') as f_reg:
    f_tmp.write(f_reg.read()+'\n'+content)


with open('list_of_combinations.dat') as f:
    s = f.read()

print(s)

xxx = 'a\n'+s

print(xxx)

with open('new_list_of_combinations.dat','w') as f:
    f.write(xxx)

print('a multiparam')

subprocess.run(run_args)
# subprocess.run(['python3', 'create_universal_HDF5.py', '-i', 'list_of_combinations_ext.dat', '-ohdf5', 'testmp1.h5', '-g', 'inputs'])
# subprocess.run(['python3', 'create_universal_HDF5.py -i list_of_combinations_ext.dat -ohdf5 testmp1.h5 -g inputs'])
# subprocess.run(['python3', 'create_universal_HDF5.py', ['-i', 'list_of_combinations_ext.dat', '-ohdf5', 'testmp1.h5', '-g', 'inputs']])
# python3 create_universal_HDF5.py -i list_of_combinations_ext.dat -ohdf5 testmp1.h5 -g inputs
# https://stackoverflow.com/questions/7152340/using-a-python-subprocess-call-to-invoke-a-python-script