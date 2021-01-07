# Two files: expected input file + input for multiparameteric
import sys
import os
import subprocess

arguments = sys.argv
intermediate_filename = 'multiparam.tmp'
run_args = ['python3', os.environ['UNIV_INPUT_PATH']+'/create_universal_HDF5.py', '-i', intermediate_filename]

def help():
    print("usage: python create_universal_HDF5.py -i-reg [Free-form input] -i-mp [multiparam FORTRAN input] [-keep-intermediate]\n"
          "                                       -univ-inps [usual inputs]\n"
          "       The inputs are the free-form input file and the driving file for FORTRAN, all the inputs of the universal input \n"
          '       (except the input file) must be placed as last arguments after the flag "-univ-inps".\n'
          '       ("-keep-intermediate" is a debugging flag to keep intermediate files.)')
    exit(0)

## Treat arguments
if (arguments[1] == "--help" or arguments[1] == "-h"):
    help()
else:
    arg_index = arguments.index("-i-reg")
    inputfilename = arguments[arg_index+1]
    arg_index = arguments.index("-i-mp")
    inputfilenamemp = arguments[arg_index+1]
    arg_index = arguments.index("-univ-inps")
    run_args = run_args + arguments[(arg_index+1):]
    keep_intermadiate = ("-keep-intermediate" in arguments)
    grouped = ("-multiparam-groups" in arguments)


## Prepare files for the FORTRAN code
with open(inputfilenamemp, "r") as InputMP:
    lines = InputMP.readlines()
names = ''
dtypes = ''
units = ''
groups = ''
if grouped:
    shift = 1
else:
    shift = 0
firstline = True
n_params = 0
for line in lines:
    sep_line = line.split()  # separate the line
    if ((len(sep_line) == 0) or (sep_line[0] == '#') or (sep_line[0] == '##')):
        pass  # print('empty or commented line')
    else:
        n_params = n_params + 1
        names = names + sep_line[0] + '\t'
        if grouped: groups = groups + sep_line[1] + '\t'
        dtypes = dtypes + sep_line[shift+1] + '\t'
        units = units + sep_line[shift+2] + '\t'
        if firstline:
            content = sep_line[shift+3] + '\t' + sep_line[shift+4] + '\t' + sep_line[shift+5]
            firstline = False
        else:
            content = content + '\n' + sep_line[shift+3] + '\t' + sep_line[shift+4] + '\t' + sep_line[shift+5]

with open('multiparam_FORTRAN.inp','w') as f:
    f.write(content)

## run FORTRAN
program_path = os.environ['UNIV_INPUT_PATH']+'/all_combinations.e'
# print(program_path)
subprocess.run(program_path)
if (not keep_intermadiate): os.remove('multiparam_FORTRAN.inp')

## append FORTRAN output to the universal-input driving file
with open('list_of_combinations_FORTRAN.dat') as f:
    content = f.read()
if (not keep_intermadiate): os.remove('list_of_combinations_FORTRAN.dat')

if grouped:
    content = '$multiparametric_grouped\t' + str(content.count('\n')) + '\n' + names + '\n'
    content = content + groups + '\n'
else:
    content = '$multiparametric\t' + str(content.count('\n')) + '\n' + names + '\n'

content = content + dtypes + '\n' + units + '\n' + content

with open(intermediate_filename,'w') as f_tmp, open(inputfilename,'r') as f_reg:
    f_tmp.write(f_reg.read()+'\n'+content)

## run the universal-input
subprocess.run(run_args)
if (not keep_intermadiate): os.remove(intermediate_filename)
# https://stackoverflow.com/questions/7152340/using-a-python-subprocess-call-to-invoke-a-python-script