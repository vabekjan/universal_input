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
    print("usage: python create_universal_HDF5.py -i [input file] -ihdf5 [input archive] -ohdf5 [output archive] -g [the group with inputs]\n"
          "       [-override]\n"
          "       The input archive is optional, output archive is a copy of the input archive with the inputs added.\n"
          "       The code cannot by default add to an existing group. Using '-override' flag allows this option. Existing\n"
          "       datasets are replaced (former are unlinked, consider repacking if applied).")
    exit(0)

## dealing with the input arguments
output_file = ""
arguments = sys.argv
if ( len(arguments) in [7,8,9,10] ): # the inputs are -i [input file] -ihdf5 [input archive] -ohdf5 [output archive] -g [the group with inputs]
    arg_index = arguments.index("-i")
    inputfilename = arguments[arg_index+1]
    arg_index = arguments.index("-ohdf5")
    target_archive = arguments[arg_index+1]
    if ("-ihdf5" in arguments):
        arg_index = arguments.index("-ihdf5")
        source_archive = arguments[arg_index+1]
        if (source_archive == target_archive):
            copy_archive = False
            print('h5-target archive is the h5-input archive. Inputs will be just added in the respective group.')
        else:
            copy_archive = True
    else:
        copy_archive = False
    arg_index = arguments.index("-g")
    groupname = arguments[arg_index+1]
    override = ("-override" in arguments)

elif arguments[1] == "--help" or arguments[1] == "-h":
        help()
else:
    print("The code now requires precise specification of input arguments")
    exit(1)


## FUNCTIONS TO WORK WITH THE ARCHIVE
def delete_input(h_path,name):
    del h_path[name]
    print('warning: the input ' + name + ' is erased and will be replaced if possible.')


def add_dataset(h_path, sep_line, line):
    if ((0 < len(sep_line)) and (len(sep_line) < 3)):
        print('warning in the line (input too short, entry skipped): ' + line)
        return

    if (sep_line[0] in h_path): delete_input(h_path,sep_line[0])

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

    if (name in h_path): delete_input(h_path, name)

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

def add_dataset_matrix(h_path, aggregated_lines, driving_line):
    sep_line = driving_line.split()
    name = sep_line[1]
    type = sep_line[2]
    unit = sep_line[3]
    Nrow = int(sep_line[4])
    Ncol = int(sep_line[5])
    transpose = (sep_line[0] == '$matrixtr')

    if (name in h_path): delete_input(h_path, name)

    for row in aggregated_lines:
        if (len(row) != Ncol): # check if all lines matches the given length
            print('warning in the matrix given by: ' + driving_line)
            print('wrong length of the line: ' + row)
            print('matrix-entry skipped')
            return

    if (type == 'R'):
        data = np.asarray(aggregated_lines, dtype='d')
    elif (type == 'I'):
        data = np.asarray(aggregated_lines, dtype='i')
    elif (type == 'S'):
        data = np.asarray(np.string_(aggregated_lines))
    else:
        print('warning in the matrix (type unrecognised and matrix-entry skipped): ' + driving_line)
        return
    if transpose: data = np.transpose(data)
    dset_id = h_path.create_dataset(name, data=data)
    dset_id.attrs['units'] = np.string_('[' + unit + ']')


## MAIN PROGRAM
if copy_archive: shutil.copyfile(source_archive,target_archive)


with open(inputfilename, "r") as InputFile, h5py.File(target_archive, 'a') as GeneratedFile: # access option http://docs.h5py.org/en/stable/high/file.html#file
    lines = InputFile.readlines()

    try:
        grp = GeneratedFile.create_group(groupname)
    except:
        if override:
            grp = GeneratedFile[groupname]
            print('warning: group already exists, possible conflicts will be overwritten, consider repacking if applied.')
        else:
            print("Problem creating group, consider '-override' option for adding new inputs into an existing group.")
            exit(1)

    k_agg = 0
    driving_line = []
    aggregated_lines = []
    for line in lines:
        sep_line = line.split();  # separate the line
        if ((len(sep_line) == 0) or (sep_line[0] == '#') or (sep_line[0] == '##')):
            pass  # print('empty or commented line')
        elif (k_agg > 0):
            aggregated_lines.append(sep_line)
            k_agg = k_agg - 1
            if (k_agg == 0):
                add_dataset_matrix(grp, aggregated_lines, driving_line)  # at the moment we need precise alignment
                driving_line = []
                aggregated_lines = []
        elif (sep_line[0] == '$array'):
            add_dataset_array(grp, sep_line, line)  # at the moment we need precise alignment
        elif ((sep_line[0] == '$matrix') or (sep_line[0] == '$matrixtr')):
            driving_line = line
            k_agg = int(sep_line[4])
        else:
            add_dataset(grp, sep_line, line)

print('done');
