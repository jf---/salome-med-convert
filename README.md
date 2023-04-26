# Converter MED from/to other formats

This project provides a SALOME plugin to convert mesh files between MED and
other formats.

At this time, only the following format is supported :
- SYSTUS (as known as in 2018 release).
- ABAQUS
- ASTER
- ANSYS
- ZSET

Only the meshes are converted for the moment. It is planned to also convert
results fields.

This plugin requires at least SALOME 9.3.


## Installation

Load environment with PyQt 5 support, for example, by loading the SALOME
environment and type `make`.

``` bash
salome shell -- make
```


# Executing the plugin using the development files

## Using the graphical interface

In stand-alone mode:

``` bash
medconverter gui
```

or in a SALOME graphical session:

``` bash
SALOME_PLUGINS_PATH=$(pwd) salome
```

## Using the command line

Example:

``` bash
medconverter run test/data/MOTIF_DONN1.ASC /tmp/motif.med
```

See `medconverter run --help` for the available arguments.


# Testing

In the source tree, just execute:

``` bash
salome shell -- python test/run_unittest.py
```

or to run a specific test:

``` bash
salome shell -- python test/run_unittest.py -v test_simple.TestSimple.test_abaqus_carre
```

Within a SALOME installation:

``` bash
salome test -L MEDCONVERTER
```
