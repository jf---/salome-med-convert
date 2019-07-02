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

``` bash
INST=$(pwd)/convmail_installed/lib/python3.6/site-packages/salome
PYTHONPATH=$INST SALOME_PLUGINS_PATH=$INST salome
```


``` bash
export SALOMEMECA_CONVMAIL_PYDIR=$(pwd)/convmail_installed/lib/python3.6/site-packages/salome
export PYTHONPATH=${SALOMEMECA_CONVMAIL_PYDIR}:${PYTHONPATH}
export SALOME_PLUGINS_PATH=${SALOMEMECA_CONVMAIL_PYDIR}:${SALOME_PLUGINS_PATH}

export SALOMEMECA_CONVMAIL_ROOT_DIR=$(pwd)/convmail_installed
export PATH=${SALOMEMECA_CONVMAIL_ROOT_DIR}/bin/:${PATH}

salome
```
