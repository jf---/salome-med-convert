# -*- coding: utf-8 -*-

"""
Installation of the Salome-Meca plugin for the calculation of water blades via MAC3
"""

# cf. http://docs.cython.org/src/userguide/source_files_and_compilation.html
#     https://docs.python.org/2/distutils/setupscript.html
#     https://docs.python.org/2/distutils/setupscript.html#listing-whole-packages

#from setuptools import setup, find_packages, Extension
import sys
import os
import os.path as osp
from glob import glob
from distutils import log
from distutils.core import setup
from distutils.command.install_lib import install_lib
import subprocess

def get_prefix(argv):
    "Analyse the given argv, and return the installation prefix"

    prefix = "/usr/local"
    for x in argv :
        if x.startswith("--prefix="):
            prefix = x.split("=")[1]
    return prefix

def get_last_public_changeset():
    last_changeset = subprocess.check_output(['hg','id','-i']).strip().decode()

    local_changes = True if "+" in last_changeset else False
    last_changeset_is_public = True

    hgid, phase = subprocess.check_output(['hg','phase']).strip().decode().split(': ')  
    while phase != 'public' :
        hgid, phase = subprocess.check_output(['hg','phase', "%d"%(int(hgid)-1)]).strip().decode().split(': ')
        last_changeset_is_public = False
        local_changes = True
        
    last_public_changeset = subprocess.check_output(['hg','id','-i','-r %s'%hgid]).strip().decode()
    return last_public_changeset, last_changeset_is_public, local_changes

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
        log.info("--- To import the MEDCONVERTER plugin, you should add `%s`", pypath)
        log.info("    to the environment variables PYTHONPATH and SALOME_PLUGINS_PATH.")
        log.info("    For example:")
        log.info(ENV % { 'pypath' : osp.abspath(pypath), 'prefix' : osp.abspath(PREFIX)})
        return self.alter_install_dir(install_lib.run)

    def get_outputs(self):
        return self.alter_install_dir(install_lib.get_outputs)

PKGS = ['medconverter', 'medconverter.engine', 'medconverter.gui']
MODS = ["salome_plugins",]
SCRIPTS = ["bin/medconverter",]

DATA = [
    ('bin/salome/test', glob('bin/salome/test/CTestTestfile.cmake')),
    ('share/salome/resources/medconverter', glob('resources/medconverter/*.qm') + glob('resources/medconverter/*.ui')),
    ('share/salome/resources/test', glob('test/*.py')),
    ('share/salome/resources/test/data', glob('test/data/*.*')),
    ('share/salome/resources/test/data/json', glob('test/data/json/*.json')),
    ('share/doc/salome/gui/medconverter/html', glob('doc/*.html')),
]

SALOME_DIR = 'salome'
PREFIX = get_prefix(sys.argv)
ENV = """# Environment for the MEDCONVERTER plugin

export SALOMEMECA_MEDCONVERTER_PYDIR=%(pypath)s
export PYTHONPATH=${SALOMEMECA_MEDCONVERTER_PYDIR}:${PYTHONPATH}
export SALOME_PLUGINS_PATH=${SALOMEMECA_MEDCONVERTER_PYDIR}:${SALOME_PLUGINS_PATH}

export SALOMEMECA_MEDCONVERTER_ROOT_DIR=%(prefix)s
export PATH=${SALOMEMECA_MEDCONVERTER_ROOT_DIR}/bin/:${PATH}

"""
   
__version__ = '1.0'
__hgrevid__, last_one_is_public, local_changes = get_last_public_changeset()
__release__ = "%s-%s%s"%(__version__, __hgrevid__, "-dev" if local_changes else "")

with open(os.sep.join(["medconverter","version.py"]),'w') as f:
    f.write("""# This file is automatically added by {}
__version__ = '{}'
__hgrevid__ = '{}'
__release__ = '{}'
""".format(sys.argv[0], __version__, __hgrevid__, __release__))

cmdclass = {
    'install_lib' : InstallLibSalome,
}

setup(
    name = 'medconverter',
    version = __version__,
    packages = PKGS,
    scripts = SCRIPTS,
    data_files = DATA,
    py_modules = MODS,
    cmdclass = cmdclass,
)
