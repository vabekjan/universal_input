# Universal input
This scripts converts input files of two types to HDF5 file.

### Usage:
``` bash
python create_universal_HDF5.py [-o output_file] [input_file]
```

### The Free Form Format Input
#### Format
Every Free Form Format Input file has `[FreeFormFormat]` tag on the very first line.
The input lines then have following form:

| Name of the variable | Value for this variable | Type  |  Units | Comments |
| ------ | ------ | ------ | ------ | ------ |
| single string (letters and underscores) | valid python number | [I/R/S] | [string] | # ... |

#### Example:
| Name of the variable | Value for this variable | Type  |  Units | Comments | 
| ------ | ------ | ------ | ------ | ------ |
| `radius_for_diagnostics` | `0.1e0` | `R` | `[mm]` | `# Radius for ... ` |

## Other supported inputs
### Unformatted Fortran Input file
#### Format <br>

Each line of the format has this form:

`name of variable [units]/(units) : value`

Value is a valid Fortran value: Integer, Real or String.
Any line with different format is ignored.

#### Example

`Physical distance of propagation (m)   : 2.d0 `
