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
        log.info("--- To import the ConvMail plugin, you should add `%s`", pypath)
        log.info("    to the environment variables PYTHONPATH and SALOME_PLUGINS_PATH.")
        log.info("    For example:")
        log.info(ENV % { 'pypath' : osp.abspath(pypath), 'prefix' : osp.abspath(PREFIX)})
        return self.alter_install_dir(install_lib.run)

    def get_outputs(self):
        return self.alter_install_dir(install_lib.get_outputs)
    
PKGS = ['convmail', 'convmail.gui']
MODS = ["salome_plugins",]
SCRIPTS = ["bin/convmailGUI",]

DATA = [
    ('bin/salome/test', glob('bin/salome/test/CTestTestfile.cmake')),
    # ('share/salome/resources/meshes', glob('resources/meshes/*')),
    # ('share/salome/resources/references', glob('resources/references/*.*')),
    # ('share/salome/resources/data', glob('resources/data/*.*')),
    # ('share/salome/resources/data/XXX1', glob('resources/data/XXX1/*.*')),
    # ('share/salome/resources/data/MODELE_DC', glob('resources/data/MODELE_DC/*.*')),
    # ('share/salome/resources/data/ForcHydro', glob('resources/data/ForcHydro/*.*')),
    ('share/salome/resources/convmail', glob('resources/translation/ConvMail_msg_fr.qm')),
]

SALOME_DIR = 'salome'
PREFIX = get_prefix(sys.argv)
ENV = """# Environment for the MAC3 plugin

export SALOMEMECA_CONVMAIL_PYDIR=%(pypath)s
export PYTHONPATH=${SALOMEMECA_CONVMAIL_PYDIR}:${PYTHONPATH}
export SALOME_PLUGINS_PATH=${SALOMEMECA_CONVMAIL_PYDIR}:${SALOME_PLUGINS_PATH}

export SALOMEMECA_CONVMAIL_ROOT_DIR=%(prefix)s
export PATH=${SALOMEMECA_CONVMAIL_ROOT_DIR}/bin/:${PATH}

"""

cmdclass = {
    'install_lib' : InstallLibSalome,
}

setup(
    name = 'convmail',
    version = '1.0',
    packages = PKGS,
    scripts = SCRIPTS,
    data_files = DATA,
    py_modules = MODS,
    cmdclass = cmdclass,
)
