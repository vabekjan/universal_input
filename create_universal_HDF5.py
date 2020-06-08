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
import os.path

#### THE MAIN PROGRAM #####

# Load argument for input file - the name of the file is argument 0, so we want argument 1

def help():
    print("usage: python create_universal_HDF5.py [-o output_file] [input_file]")
    print("Without any arguments it uses FreeFormInputs.inp in the current directory.")
    exit(0)

def verify_input_file(filename):
    inputfilename = str(arguments[1])    
    print('Given file:', inputfilename)
    if not os.path.exists(inputfilename):
       print("Error: File {file} does not exists.".format(file=inputfilename))
       exit(1)


output_file = ""
arguments = sys.argv
if len(arguments) == 1:
    inputfilename = "FreeFormInputs.inp"
    print("Using default filename:", inputfilename)
elif len(arguments) > 4:
    print('Too many arguments.\nNumber of arguments:', len(arguments))
    exit(1)
elif len(arguments) == 4:
    print("Trying to locate output file.")
    if not "-o" in arguments[1:3]:
        print("Wrong arguments.\n")
        help()
    else:
        o_index = arguments.index("-o")
        o_f_index = o_index+1
        output_file = arguments[o_f_index]
        if os.path.exists(output_file):
            print("file exists")
            answered = False
            while not answered:
                confirmation = input("Do you really want to overwrite an existing file {o_f}? [Y/N]".format(o_f = output_file))
                if confirmation in "yY":
                    answered = True
                elif confirmation in "nN":
                    answered = True
                    output_file = ""
                    print("Output file not selected. It will not be created.")
        if o_index == 1:
            inputfilename = arguments[3]
        else:
            inputfilename = arguments[1]
        verify_input_file(inputfilename)
elif len(arguments) == 3:
    print("You are either missing an argument or you have one extra.\n")
    help()
    exit(1)
else:
    if arguments[1] == "--help" or arguments[1] == "-h":
        help()
    else:
        inputfilename = arguments[1]
        verify_input_file(inputfilename)

# inputfilename = 'FreeFormInputs.inp'
outputfilename = 'results.h5'

## specify the name of files and datasets
InputFile = open(inputfilename, "r")
GeneratedFile = h5py.File(outputfilename, 'w')  # be careful, now it trucates if already exists
grp = GeneratedFile.create_group('inputs')


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


def format_to_freeform(line):
    line = line.strip()
    if bool(line) and not line[0] in "[#":

        # Split the line and find name of the variable with the value
        line = line.lower().split(":")
        if len(line) >= 2:
            if len(line) > 2:
                name = ":".join(line[:-1])
            else:
                name = line[0].strip()
            value = line[-1].strip()

            # Replace all the brackets with square brackets
            brackets = {"(": "[", ")": "]"}
            for b in brackets:
                name = name.replace(b, brackets[b])
    
            # Try to locate units
            unit = ""
            if "[" in name:
                s = name.rfind("[")
                unit = name[s:]
                name = name[:s]
            for b in brackets:
                name = name.replace(brackets[b], b)

            # Try to find the set of numbers where the value belongs
            number_set = "I"
            if len(value) < 1:
                return ""
            if value[0].isalpha() or "_" in value:
                number_set = "S"
            elif (value[0].isnumeric() or (value[0] == "-" and value[1].isnumeric())) and "d" in value:
                number_set = "R"
                if ".d" in value:
                    value = value.replace("d", "0e")
                else:
                    value = value.replace("d", "e")

            # Reformat the name of the variable
            name = name.replace(",", " ")
            name = name.replace(" - ", "-")
            name = name.replace("/", " ")
            name = "_".join(name.split())
            line = " ".join([name, value, number_set, unit])
            
            return line
        else:
            return ""
    else:
        return ""


lines = InputFile.readlines()
variables = []
first = True
formatted = True
out = False

if not output_file == "":
    out = True
    output = open(output_file, "w")
    output.write("[FreeFormFormat]\n")

for line in lines:
    if first:
        first = False
        if not "[FreeFormFormat]" in line:
            print("File not formatted.")
            formatted = False
    if not formatted:
        if not type(line) == type("s"):
            continue
        line = format_to_freeform(line)
        if out:
            output.write(line+"\n")
    sep_line = line.split();  # separate the line
    if ((len(sep_line) == 0) or (sep_line[0] == '#') or (sep_line[0] == '##')):
        pass  # print('empty or commented line')
    elif (sep_line[0] == '$array'):
        add_dataset_array(grp, sep_line, line)  # at the moment we need precise alignment
    else:
        add_dataset(grp, sep_line, line)
if out:
    output.close()

InputFile.close()
GeneratedFile.close()

print('done');
