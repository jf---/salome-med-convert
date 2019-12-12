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

from med_convert.utilities import data_path
from med_convert.convert import Fmt, convert

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
            tmpdir = tempfile.mkdtemp(prefix='tmp_medconvert_')
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
def standard_conversion(tmpdir, utest, filename, input_format, nbcells, nbnodes,
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
        print("private test skipped", end="")
        return
    utest.assertTrue(osp.isfile(infile), infile)

    outfile = osp.join(tmpdir if DEBUG != 1 else os.getcwd(),
                       osp.splitext(osp.basename(filename))[0] + ".med")
    if DEBUG != 1:
        utest.assertFalse(osp.isfile(outfile), outfile)

    if input_format == "SYSTUS":
        convert(infile, Fmt.Systus, outfile, Fmt.Med, verbose=(DEBUG == 1))
    elif input_format == "ABAQUS":
        convert(infile, Fmt.Abaqus, outfile, Fmt.Med, verbose=(DEBUG == 1))
    else:
        raise KeyError('Unsupported mesh format %s'%input_format)

    utest.assertTrue(osp.isfile(outfile))
    mesh = MEDLoader.ReadMeshFromFile(outfile)
    if nbcells * nbnodes == 0:
        print("Number of elements:", mesh.getNumberOfCells())
        print("Number of nodes:", mesh.getNumberOfNodes())
    else:
        utest.assertEqual(mesh.getNumberOfCells(), nbcells)
        utest.assertEqual(mesh.getNumberOfNodes(), nbnodes)
