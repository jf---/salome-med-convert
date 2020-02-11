# -*- coding: utf-8 -*-

"""
Installation of the Salome-Meca plugin for the calculation of water blades via MAC3
"""

# cf. http://docs.cython.org/src/userguide/source_files_and_compilation.html
#     https://docs.python.org/2/distutils/setupscript.html
#     https://docs.python.org/2/distutils/setupscript.html#listing-whole-packages

#from setuptools import setup, find_packages, Extension
import sys
import os.path as osp
from glob import glob
from distutils import log
from distutils.core import setup
from distutils.command.install_lib import install_lib

def get_prefix(argv):
    "Analyse the given argv, and return the installation prefix"

    prefix = "/usr/local"
    for x in argv :
        if x.startswith("--prefix="):
            prefix = x.split("=")[1]
    return prefix

class InstallLibSalome(install_lib):
    """Modify the install process to suite the salome standards (put
    every things into the *salome* directory which is inside the
    python site package"""
    def alter_install_dir(self, method):
        old_install_dir = self.install_dir
        self.install_dir = osp.join(self.install_dir, SALOME_DIR)
        output = method(self)
        self.install_dir = old_install_dir
        return output

    def run(self):
        pypath = osp.join(self.install_dir, SALOME_DIR)
        log.info("--- To import the MED_CONVERT plugin, you should add `%s`", pypath)
        log.info("    to the environment variables PYTHONPATH and SALOME_PLUGINS_PATH.")
        log.info("    For example:")
        log.info(ENV % { 'pypath' : osp.abspath(pypath), 'prefix' : osp.abspath(PREFIX)})
        return self.alter_install_dir(install_lib.run)

    def get_outputs(self):
        return self.alter_install_dir(install_lib.get_outputs)

PKGS = ['med_convert', 'med_convert.convert', 'med_convert.gui']
MODS = ["salome_plugins",]
SCRIPTS = ["bin/med_convert",]

DATA = [
    ('bin/salome/test', glob('bin/salome/test/CTestTestfile.cmake')),
    ('share/salome/resources/med_convert', glob('resources/med_convert/*.qm') + glob('resources/med_convert/*.ui')),
    ('share/salome/resources/test', glob('test/*.py')),
    ('share/salome/resources/test/data', glob('test/data/*')),
    ('share/doc/salome/gui/med_convert/html', glob('doc/*.html')),
]

SALOME_DIR = 'salome'
PREFIX = get_prefix(sys.argv)
ENV = """# Environment for the MED_CONVERT plugin

export SALOMEMECA_MED_CONVERT_PYDIR=%(pypath)s
export PYTHONPATH=${SALOMEMECA_MED_CONVERT_PYDIR}:${PYTHONPATH}
export SALOME_PLUGINS_PATH=${SALOMEMECA_MED_CONVERT_PYDIR}:${SALOME_PLUGINS_PATH}

export SALOMEMECA_MED_CONVERT_ROOT_DIR=%(prefix)s
export PATH=${SALOMEMECA_MED_CONVERT_ROOT_DIR}/bin/:${PATH}

"""

cmdclass = {
    'install_lib' : InstallLibSalome,
}

setup(
    name = 'med_convert',
    version = '1.0',
    packages = PKGS,
    scripts = SCRIPTS,
    data_files = DATA,
    py_modules = MODS,
    cmdclass = cmdclass,
)
