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
# The idea is to create universel input files that can be used accross codes. 
# All the data are now stored in the group 'inputs'. Be carefull with the names of
# variables. If they are chosen correctly, it would be easier to cross-platform it.

import numpy as np
import h5py




#### THE MAIN PROGRAM #####


inputfilename = 'FreeFormInputs.inp'
outputfilename = 'results.h5'
#file1=open(os.path.join(inpath2,'rgrid.dat'),"r")


## load radial grid
#file1=open(inpath2+"rgrid.dat","r")
file1=open(inputfilename,"r")
GeneratedFile = h5py.File(outputfilename, 'w')
grp = GeneratedFile.create_group('inputs')

def adddataset(h_path,sep_line,line):
  if (sep_line[2]=='R'): dset_id = h_path.create_dataset(sep_line[0], data=float(sep_line[1]))
  elif (sep_line[2]=='I'): dset_id = h_path.create_dataset(sep_line[0], data=int(sep_line[1]))
  elif (sep_line[2]=='S'): dset_id = h_path.create_dataset(sep_line[0], data=sep_line[1])
  else: print('warning in the line (type unrecognised and entry skipped): ' + line); return

  if (len(sep_line) < 4): print('warning in the line (missing units ?): ' + line)  
  else: dset_id.attrs['units']=np.string_('['+sep_line[3]+']')

#if file1.mode == "r":
lines = file1.readlines()
for line in lines:
  sep_line= line.split(); # rgrid.append(float(dum[1])); k1=k1+1
  if ( (len(sep_line)==0) or (sep_line[0]=='#') or (sep_line[0]=='##') ): pass #print('empty or commented line')
  else:    
    adddataset(grp,sep_line,line)
    #print("The line is: ", sep_line, len(sep_line))


file1.close()
GeneratedFile.close()


print('done');


# pass statement will be used for skipping
