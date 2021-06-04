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
import json
import tempfile
from functools import wraps
import ssl
import getpass
from urllib.request import urlopen
from urllib.error import HTTPError

from medconverter.engine import Fmt, convert as convert_engine
from medconverter.utilities import MAX_ELTS_CHECK_GROUPS

DEBUG = int(os.getenv("DEBUG", 0))

try:
    from medcoupling import *
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
    force = force or int(os.environ.get("MEDCONVERT_FORCEDOWNLOAD", 0)) == 1

    subdir, filename = osp.split(datafile)
    cachedir = osp.join('/', 'tmp', '_med_convert_cache_%s'%getpass.getuser(), subdir)
    os.makedirs(cachedir, exist_ok=True)

    filepath = osp.join(cachedir, filename)
    if force or not osp.isfile(filename):
        if not download_file(datafile, filepath, insecure=True):
            return None
    return filepath

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
def base_test_conversion(tmpdir, utest, filename, input_format, output_format):
    """Base function to check a mesh conversion.

    In debug mode (DEBUG environment variable set to 1) the result med files
    are written in the current directory.

    Arguments:
        tmpdir (str): Path to the temporary directory.
        utest (*unittest.TestCase*): Test object.
        filename (str): Input mesh file.
        input_format (str) : Type of input mesh (SYSTUS or ABAQUS)
    """
    if not filename:
        print("Test skipped", end="\n")
        return

    utest.assertTrue(osp.isfile(filename), filename)

    wdir = tmpdir if DEBUG != 1 else os.getcwd()
    outfile = osp.join(wdir, osp.splitext(osp.basename(filename))[0] + Fmt.extensions(output_format)[0])
    output_comm = osp.join(wdir, "%s.comm"%osp.splitext(osp.basename(filename))[0])

    if DEBUG != 1:
        utest.assertFalse(osp.isfile(outfile), outfile)

    convert_engine(filename, input_format, outfile, output_format, output_comm, verbose=(DEBUG == 1))

    utest.assertTrue(osp.isfile(outfile))
    if output_format is Fmt.Ansys :
        utest.assertTrue(osp.isfile(output_comm))
        
    if output_format is Fmt.Salome :
        mesh = MEDFileUMesh(outfile)
    else :
        convert_engine(outfile, output_format, '%s.med'%outfile, Fmt.Salome, verbose=(DEBUG == 1))
        mesh = MEDFileUMesh('%s.med'%outfile)

    return mesh

def standard_test_conversion(utest, filename, input_format, output_format,
                             nbcells, nbnodes, cellstypes,
                             nbcellsgrps, nbnodesgrps):
    """Function to check a mesh conversion.

     Arguments:
        utest (*unittest.TestCase*): Test object.
        filename (str): Input mesh file.
        input_format (str) : Type of input mesh (SYSTUS or ABAQUS)
        nbcells (int): Expected number of cells of dimension 0.
        nbnodes (int): Expected number of nodes.
    """

    mesh = base_test_conversion(utest, filename, input_format, output_format)
    utest.assertTrue(isinstance(mesh, MEDFileUMesh))

    convertedcellstypes = [MEDCouplingUMesh.GetReprOfGeometricType(i).strip('NORM_') for lev in mesh.getNonEmptyLevels() for i in mesh.getGeoTypesAtLevel(lev)]
    total_nb_of_cells = sum(mesh.getNumberOfCellsAtLevel(lev) for lev in mesh.getNonEmptyLevels())

    total_nb_of_cells_groups = sum(len(mesh.getGroupsOnSpecifiedLev(lev)) for lev in mesh.getNonEmptyLevels())

    utest.assertEqual(total_nb_of_cells, nbcells)
    utest.assertEqual(mesh.getNumberOfNodes(), nbnodes)
    utest.assertEqual(set(convertedcellstypes), set(cellstypes))
    utest.assertEqual(total_nb_of_cells_groups, nbcellsgrps)
    utest.assertEqual(len(mesh.getGroupsOnSpecifiedLev(1)), nbnodesgrps)


def deep_test_conversion(utest, filename, input_format, output_format,
                         jsonfile):

    """Function to deep check a mesh conversion.

    Arguments:
        utest (*unittest.TestCase*): Test object.
        filename (str): Input mesh file.
        input_format (str) : Type of input mesh (SYSTUS or ABAQUS)
        nbcells (int): Expected number of cells of dimension 0.
        nbnodes (int): Expected number of nodes.
    """

    mesh = base_test_conversion(utest, filename, input_format, output_format)
    utest.assertTrue(isinstance(mesh, MEDFileUMesh))

    with open(jsonfile) as f:
        refe = json.load(f)

    total_nb_of_cells = sum(mesh.getNumberOfCellsAtLevel(lev) for lev in mesh.getNonEmptyLevels())
    convertedcellstypes = [MEDCouplingUMesh.GetReprOfGeometricType(i) for lev in mesh.getNonEmptyLevels() for i in mesh.getGeoTypesAtLevel(lev)]
    total_nb_of_cells_groups = sum(len(mesh.getGroupsOnSpecifiedLev(lev)) for lev in mesh.getNonEmptyLevels())

    utest.assertEqual(total_nb_of_cells, refe['NB_CELLS'])
    utest.assertEqual(total_nb_of_cells_groups, refe['NB_GRP_CELLS'])
    utest.assertEqual(len(mesh.getGroupsOnSpecifiedLev(1)), refe['NB_GRP_NODES'])
    utest.assertEqual(mesh.getNumberOfNodes(), refe['NB_NODES'])
    utest.assertEqual(set(mesh.getNonEmptyLevels()), set(map(int,refe['CELLS'].keys())))

    for n, coords in refe['NODES'].items():
        utest.assertAlmostEqual(mesh.getCoords()[int(n)].getValues(), coords)

    refe_cells_types = []
    for lev, item in refe['CELLS'].items():
        for cell, values in item.items():
            idx = int(cell.split('_')[0].strip('ID'))
            cell_type = "NORM_%s"%cell.split('_')[1]
            refe_cells_types.append(cell_type)
            utest.assertEqual(MEDCouplingUMesh.GetReprOfGeometricType(mesh[int(lev)].getTypeOfCell(idx)), cell_type)
            utest.assertEqual(mesh[int(lev)].getNodeIdsOfCell(idx), values)

    utest.assertEqual(set(convertedcellstypes), set(refe_cells_types))

    for lev, item in refe['GROUPS'].items():
        for name, values in item.items():
            utest.assertEqual(mesh.getGroupArr(int(lev), name).getValues()[:MAX_ELTS_CHECK_GROUPS], values)
