# Universal input

## Usage:
``` bash
usage: python create_universal_HDF5.py -i [input file] [-ihdf5 [input archive]] -ohdf5 [output archive] -g [the group with inputs] [-override]

The input archive is optional, output archive is a copy of the input archive with the inputs added.
The code cannot by default add to an existing group. Using '-override' flag allows this option. Existing datasets are replaced (former are unlinked, consider repacking if applied).

If task requires investigation of Gauss-Bessel beams, then you have to compile additionally
python writing_init_field.py
python cmplxer_from_hdf5_wrtnn_field.py

This will create file initial_field_compexified.h5, which will be used by preprocessor, creating complexified Gauss-Bessel beam in file result.h5
```
The arguments need to be given except optional. There is no need to order them.

## The Free Form Format Input
The input lines then have following form:

### 1: standard lines

| Name of the variable | Value for this variable | Type  |  Units | Comments |
| ------ | ------ | ------ | ------ | ------ |
| single string (letters and underscores) | valid python number | [I/R/S] | [string] | # ... |

#### Example:
| Name of the variable | Value for this variable | Type  |  Units | Comments | 
| ------ | ------ | ------ | ------ | ------ |
| `radius_for_diagnostics` | `0.1e0` | `R` | `[mm]` | `# Radius for ... ` |

### 2: special 
Using keywords defined by $. 
- `$array` It works as the usual variable except there is multiple values provided until the end of line or comment started with `#`. Example:

`$array myrarrray R SI	3.14 2.71 1.0 # this is the only allowed commenting way`

- `$matrix` There is a driving line specifiyng the propaeties of the matrix. There are dimensions of the matrix (number of rows x number of columns) and this line is followed by the matrix. Example:


>$matrix	mymatrixreal	R	SI	3	4 \
1	2	3	4\
5	6	7	8\
9	10	11	12

- `$matrixtr` The same as `$matrix`, but the matrix is transposed in the HDF5 archive (the input form is exactly the same).

- `$multiparametric` This is an advanced operation to generate a bunch of starting hdf5-files for a list of varying parmeters. This input consists of multiple lines. First line is the keyword followed by the total amount of parameter combinations. Next lines specify: **names**, **types** and **units**. These values are stored at two places:
    1) In the usual output archive, all parameters are stored as arrays defined by respective columns.
    2) In the directory ***multiparameters***, there are copies of the original archive enumerated by rows and each of these copies contais only the respective row.

    There is an example of the input file, see also details in the next paragraph.
>$multiparametric	6 \
a	b	c	\
R	I	R	\
SI	SI	SI	\
0.000000E+00 0.000000E+00 0.100000E+01\
0.500000E+00 0.000000E+00 0.100000E+01\
0.100000E+01 0.000000E+00 0.100000E+01\
0.000000E+00 0.100000E+01 0.100000E+01\
0.500000E+00 0.100000E+01 0.100000E+01\
0.100000E+01 0.100000E+01 0.100000E+01

- `$multiparametric_grouped` The same as the previous, but the second line specifies groups.
>$multiparametric	6 \
a	b	c	\
group1	group2	group1	\
R	I	R	\
SI	SI	SI	\
0.000000E+00 0.000000E+00 0.100000E+01\
0.500000E+00 0.000000E+00 0.100000E+01\
0.100000E+01 0.000000E+00 0.100000E+01\
0.000000E+00 0.100000E+01 0.100000E+01\
0.500000E+00 0.100000E+01 0.100000E+01\
0.100000E+01 0.100000E+01 0.100000E+01

- `$change_group` This changes the group where the results are stored, the same policy (`override`) is applied for all groups. Reaccessing a group means openning an existing group.
## Multiparametric studies
There is a supplementary script `process_multiparametric.py`. This script uses one FORTRAN program designed to generate all possible combinations of parameters from given ranges. The FORTRAN program is compiled by `compile_and_copy_multiparam.sh`. The generated executable is needed for the script. The additional input for this script are the definition of the desired variables with their ranges. The form is:
| Name of the variable | Type | Units  |  minimum | maximum | # of intermediate points|
| ------ | ------ | ------ | ------ | ------ | ------ |
a|	R|	SI|	0	|1	|1
b|	I|	SI|	0	|1	|0
c|	R|	SI|	0	|1	|-1

The special value of "-1" of intermediate points takes the variable as not varying and only the *maximum* is considered.


