# Universal input
This scripts converts input files of two types to HDF5 file.

### Usage:
``` bash
usage: python create_universal_HDF5.py -i [input file] -ihdf5 [input archive] -ohdf5 [output archive] -g [the group with inputs]

The input archive is optional, output archive is a copy of the input archive with the inputs added.
The code cannot by default add to an existing group. Using '-override' flag allows this option. Existing datasets are replaced (former are unlinked, consider repacking if applied).
```
The arguments need to be given except optional. There is no need to order them.

### The Free Form Format Input
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
- `$array`. It works as the usual variable except there is multiple values provided until the end of line or comment started with `#`. Example:

`$array myrarrray R SI	3.14 2.71 1.0 # this is the only allowed commenting way`

- `$matrix`. There is a driving line specifiyng the propaeties of the matrix. There are dimensions of the matrix (number of rows x number of columns) and this line is followed by the matrix. Example:


>$matrix	mymatrixreal	R	SI	3	4 \
1	2	3	4\
5	6	7	8\
9	10	11	12

- `$matrixtr`. The same as `$matrix`, but the matrix is transposed in the HDF5 archive (the input form is exactly the same).