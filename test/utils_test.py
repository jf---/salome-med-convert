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
import ssl
from urllib.request import urlopen
from urllib.error import HTTPError

from medconverter.engine import Fmt, convert as convert_engine

DEBUG = int(os.getenv("DEBUG", 0))

try:
    import MEDLoader
except ImportError:
    sys.stderr.write("Please read the README file to execute the unittests "
                     "inside SALOME environment.")
    raise

def download_file(datafile, dest, insecure=False):
    """Download a testcase datafile from the repository and copy it onto `dest`.
    Arguments:
        datafile (str): Basename of the testcase datafile.
        dest (str): Destination path.
        insecure (bool, optional): Allow connections to TLS sites without certs.
    Returns:
        bool: *True* if it suceeded, *False* otherwise.
    """
    timeout = 10
    repo = "https://nexus.retd.edf.fr/repository/codeaster-archives/tests-data"
    url = repo + "/salome-med-convert/" + datafile
    ctx = ssl._create_unverified_context() if insecure else None
    try :
        with urlopen(url, timeout=timeout, context=ctx) as request:
            with open(dest, "wb") as fobj:
                fobj.write(request.read())
            iret = request.getcode()
        return iret == 200
    
    except HTTPError :
        return None

def get_datafile_path(datafile, force=False):
    """Returns the filename of the testcase datafile.
    Arguments:
        datafile (str): Basename of the testcase datafile.
        force (bool, optional): *True* to force downloading. Can also be
            enabled using MEDCONVERT_FORCEDOWNLOAD=1 environment variable.
    Returns:
        str: Absolute local path of the datafile or *None* if the destination
        file can not be provided.
    """
    cachedir = "/tmp/_med_convert_cache"
    force = force or int(os.environ.get("MEDCONVERT_FORCEDOWNLOAD", 0)) == 1
    os.makedirs(cachedir, exist_ok=True)
    filename = osp.join(cachedir, datafile)
    if force or not osp.isfile(filename):
        if not download_file(datafile, filename, insecure=True):
            return None
    return filename

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
def standard_conversion(tmpdir, utest, filename, input_format, output_format,
                        nbcells, nbnodes, cellstypes):
    """Function to check a mesh conversion.

    In debug mode (DEBUG environment variable set to 1) the result med files
    are written in the current directory.

    Arguments:
        tmpdir (str): Path to the temporary directory.
        utest (*unittest.TestCase*): Test object.
        filename (str): Input mesh file.
        input_format (str) : Type of input mesh (SYSTUS or ABAQUS)
        nbcells (int): Expected number of cells of dimension 0.
        nbnodes (int): Expected number of nodes.
    """
    if not filename:
        print("Test skipped", end="\n")
        return

    utest.assertTrue(osp.isfile(filename), filename)

    outfile = osp.join(tmpdir if DEBUG != 1 else os.getcwd(),
                       osp.splitext(osp.basename(filename))[0] + Fmt.extensions(output_format)[0])
    if DEBUG != 1:
        utest.assertFalse(osp.isfile(outfile), outfile)

    convert_engine(filename, input_format, outfile, output_format, verbose=(DEBUG == 1))
  
    utest.assertTrue(osp.isfile(outfile))

    if output_format is Fmt.Salome :
        mesh = MEDLoader.MEDFileUMesh(outfile)
    else :
        convert_engine(outfile, output_format, '%s.med'%outfile, Fmt.Salome, verbose=(DEBUG == 1))
        mesh = MEDLoader.MEDFileUMesh('%s.med'%outfile)

    convertedcellstypes = [MEDLoader.MEDCouplingUMesh.GetReprOfGeometricType(i).strip('NORM_') for lev in mesh.getNonEmptyLevels() for i in mesh.getGeoTypesAtLevel(lev)]
    total_nb_of_cells = sum(mesh.getNumberOfCellsAtLevel(lev) for lev in mesh.getNonEmptyLevels())

    if nbcells * nbnodes == 0:
        print("Number of elements:", total_nb_of_cells)
        print("Number of nodes:", mesh.getNumberOfNodes())
    else:
        utest.assertEqual(total_nb_of_cells, nbcells)
        utest.assertEqual(mesh.getNumberOfNodes(), nbnodes)
        utest.assertEqual(set(convertedcellstypes), set(cellstypes))
