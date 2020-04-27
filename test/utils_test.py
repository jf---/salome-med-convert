# coding=utf-8

# Copyright 2019 EDF R&D
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License Version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, you may download a copy of license
# from https://www.gnu.org/licenses/gpl-3.0.

import os
import os.path as osp
import shutil
import sys
import tempfile
from functools import wraps

from medconverter.utilities import data_path
from medconverter.engine import Fmt, convert as convert_engine

DEBUG = int(os.getenv("DEBUG", 0))

try:
    import MEDLoader
except ImportError:
    sys.stderr.write("Please read the README file to execute the unittests "
                     "inside SALOME environment.")
    raise


def tempdir(func):
    """Decorator that executes a function in a temporary directory.
    Expected signature is: `func(tmpdir, ...)`.
    """

    @wraps(func)
    def wrapper(*args, **kwds):
        """wrapper"""
        retcode = None
        try:
            tmpdir = tempfile.mkdtemp(prefix='tmp_medconverter_')
            retcode = func(tmpdir, *args, **kwds)
        except Exception:
            sys.stderr.write("temporary directory is: {0}\n".format(tmpdir))
            raise
        else:
            if osp.exists(tmpdir):
                shutil.rmtree(tmpdir)
        return retcode
    return wrapper


@tempdir
def standard_conversion(tmpdir, utest, filename, input_format, output_format, nbcells, nbnodes,
                        private=False):
    """Function to check a mesh conversion.

    In debug mode (DEBUG environment variable set to 1) the result med files
    are written in the current directory.

    Arguments:
        tmpdir (str): Path to the temporary directory.
        utest (*unittest.TestCase*): Test object.
        filename (str): Basename of the input mesh file.
        input_format (str) : Type of input mesh (SYSTUS or ABAQUS)
        nbcells (int): Expected number of cells of dimension 0.
        nbnodes (int): Expected number of nodes.
        private (bool): *True* for private meshes. *False* otherwise.
    """
    infile = osp.join(data_path(private), filename)
    if private and not osp.isfile(infile):
        print("private test skipped", end="\n")
        return
    utest.assertTrue(osp.isfile(infile), infile)

    outfile = osp.join(tmpdir if DEBUG != 1 else os.getcwd(),
                       osp.splitext(osp.basename(filename))[0] + Fmt.extensions(output_format)[0])
    if DEBUG != 1:
        utest.assertFalse(osp.isfile(outfile), outfile)

    convert_engine(infile, input_format, outfile, output_format, verbose=(DEBUG == 1))
  
    utest.assertTrue(osp.isfile(outfile))

    if output_format is Fmt.Salome :
        mesh = MEDLoader.ReadMeshFromFile(outfile)
    else :
        convert_engine(outfile, output_format, '%s.med'%outfile, Fmt.Salome, verbose=(DEBUG == 1))
        mesh = MEDLoader.ReadMeshFromFile('%s.med'%outfile)
        
    if nbcells * nbnodes == 0:
        print("Number of elements:", mesh.getNumberOfCells())
        print("Number of nodes:", mesh.getNumberOfNodes())
    else:
        utest.assertEqual(mesh.getNumberOfCells(), nbcells)
        utest.assertEqual(mesh.getNumberOfNodes(), nbnodes)
