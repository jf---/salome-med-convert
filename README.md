# Converter MED from/to other formats

This project provides a SALOME plugin to convert mesh files between MED and
other formats.

At this time, only the following format is supported :
- SYSTUS (as known as in 2018 release).

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

In stand-alone mode:

``` bash
./bin/med_convert
```

or in a SALOME graphical session:

``` bash
SALOME_PLUGINS_PATH=$(pwd) salome
```


# Testing

In the source tree, just execute:

``` bash
salome shell -- python test/run_unittest.py
```

or to run a specific test:

``` bash
salome shell -- python test/run_unittest.py -v test_utilities
```

[TODO] Within a SALOME installation:

``` bash
salome test -R MED_CONVERT
```
