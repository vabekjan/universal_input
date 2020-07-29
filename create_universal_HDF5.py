####################################################################################
# Jan Vabek - ELI-Beamlines, CELIA, CTU in Prague (FNSPE) (2020)
#
# the purpose of this code is to generate a universal input HDF5-file,
# it allows to write all the inputs in a free form specified by
#
#	'name'	'value' 'type'	'unit'	'comments, etc. (no effect on the file)'
#
# type is in (R)eal (I)nteger (S)tring
#
# The idea is to create universal input files that can be used accross codes. 
# All the data are now stored in the group 'inputs'. Be carefull with the names of
# variables. If they are chosen correctly, it would be easier to cross-platform it.

import numpy as np
import h5py
import sys
import os
import shutil

#### THE MAIN PROGRAM #####

# Load argument for input file - the name of the file is argument 0, so we want argument 1

def help():
    print("usage: python create_universal_HDF5.py -i [input file] -ihdf5 [input archive] -ohdf5 [output archive] -g [the group with inputs]")
    exit(0)

def verify_input_file(inputfilename):
    print('Given file:', inputfilename)
    if not os.path.exists(inputfilename):
       print("Error: File {file} does not exists.".format(file=inputfilename))
       exit(1)

## dealing with the input arguments
output_file = ""
arguments = sys.argv
# print(arguments)
if len(arguments) == 9: # the input are -i [input file] -ihdf5 [input archive] -ohdf5 [output archive] -g [the group with inputs]
    arg_index = arguments.index("-i")
    inputfilename = arguments[arg_index+1]
    arg_index = arguments.index("-ihdf5")
    source_archive = arguments[arg_index+1]
    arg_index = arguments.index("-ohdf5")
    target_archive = arguments[arg_index+1]
    arg_index = arguments.index("-g")
    groupname = arguments[arg_index+1]
elif arguments[1] == "--help" or arguments[1] == "-h":
        help()
else:
    print("The code now requires precise specification of input arguments")
    exit(1)

verify_input_file(inputfilename)
verify_input_file(source_archive)


# inputfilename = 'FreeFormInputs.inp'
# outputfilename = 'results.h5'

## specify the name of files and datasets

shutil.copyfile(source_archive,target_archive)
InputFile = open(inputfilename, "r")
GeneratedFile = h5py.File(target_archive, 'a')  # access option http://docs.h5py.org/en/stable/high/file.html#file
grp = GeneratedFile.create_group(groupname)


def add_dataset(h_path, sep_line, line):
    if ((0 < len(sep_line)) and (len(sep_line) < 3)):
        print('warning in the line (input too short, entry skipped): ' + line)
        return

    if (sep_line[2] == 'R'):
        dset_id = h_path.create_dataset(sep_line[0], data=float(sep_line[1]))
    elif (sep_line[2] == 'I'):
        dset_id = h_path.create_dataset(sep_line[0], data=int(sep_line[1]))
    elif (sep_line[2] == 'S'):
        dset_id = h_path.create_dataset(sep_line[0], data=np.string_(sep_line[1]))
    else:
        print('warning in the line (type unrecognised and entry skipped): ' + line);
        return

    if (len(sep_line) < 4):
        print('warning in the line (missing units ?): ' + line)
        dset_id.attrs['units'] = np.string_('?')
    else:
        unit = sep_line[3]
        if unit[0] == "[" and unit[-1] == "]":
            dset_id.attrs['units'] = np.string_(sep_line[3])
        else:
            dset_id.attrs['units'] = np.string_('[' + sep_line[3] + ']')


def add_dataset_array(h_path, sep_line, line):
    name = sep_line[1]
    type = sep_line[2]
    unit = sep_line[3]
    k_end = len(sep_line)
    for k1 in range(4, len(sep_line)):
        if (sep_line[k1] == '#'): k_end = k1  # check for comment

    if (type == 'R'):
        data = np.asarray(sep_line[4:k_end], dtype='d')
    elif (type == 'I'):
        data = np.asarray(sep_line[4:k_end], dtype='i')
    elif (type == 'S'):
        data = np.asarray(np.string_(sep_line[4:k_end]))
    else:
        print('warning in the line (type unrecognised and entry skipped): ' + line)
        return
    dset_id = h_path.create_dataset(name, data=data)
    dset_id.attrs['units'] = np.string_('[' + unit + ']')




lines = InputFile.readlines()

for line in lines:
    sep_line = line.split();  # separate the line
    if ((len(sep_line) == 0) or (sep_line[0] == '#') or (sep_line[0] == '##')):
        pass  # print('empty or commented line')
    elif (sep_line[0] == '$array'):
        add_dataset_array(grp, sep_line, line)  # at the moment we need precise alignment
    else:
        add_dataset(grp, sep_line, line)


InputFile.close()
GeneratedFile.close()

print('done');
