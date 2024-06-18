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
from medconverter.utilities import MAX_ELTS_CHECK_GROUPS, create_test_json_file

DATA_URL = "https://minio.retd.edf.fr/codeaster/tests-data"
DEBUG = int(os.getenv("DEBUG", 0))

try:
    import medcoupling as medc
except ImportError:
    sys.stderr.write(
        "Please read the README file to execute the unittests inside SALOME environment."
    )
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
    url = DATA_URL + "/salome-med-convert/" + datafile
    ctx = ssl._create_unverified_context() if insecure else None
    try:
        with urlopen(url, timeout=timeout, context=ctx) as request:
            with open(dest, "wb") as fobj:
                fobj.write(request.read())
            iret = request.getcode()
        return iret == 200

    except HTTPError:
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
    cachedir = osp.join("/", "tmp", "_med_convert_cache_%s" % getpass.getuser(), subdir)
    os.makedirs(cachedir, exist_ok=True)

    filepath = osp.join(cachedir, filename)
    if force or not osp.isfile(filepath):
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
            tmpdir = tempfile.mkdtemp(prefix="tmp_medconverter_")
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
def base_test_conversion(
    tmpdir, utest, filename, input_format, output_format, commtest=True, skip_types=[]
):
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

    utest.assertTrue(osp.isfile(filename), msg=filename)

    wdir = tmpdir if DEBUG != 1 else os.getcwd()
    outfile = osp.join(
        wdir, osp.splitext(osp.basename(filename))[0] + Fmt.extensions(output_format)[0]
    )

    if commtest:
        output_comm = osp.join(wdir, "%s.comm" % osp.splitext(osp.basename(filename))[0])
    else:
        output_comm = ""

    if DEBUG != 1:
        utest.assertFalse(osp.isfile(outfile), msg=outfile)

    convert_engine(
        filename,
        input_format,
        outfile,
        output_format,
        output_comm,
        skip_types=skip_types,
        verbose=(DEBUG == 1),
    )

    utest.assertTrue(osp.isfile(outfile), msg=outfile)
    if output_format is Fmt.Ansys:
        utest.assertTrue(osp.isfile(output_comm), msg=output_comm)

    if output_format is Fmt.Salome:
        mesh = medc.MEDFileUMesh(outfile)
    else:
        convert_engine(
            outfile,
            output_format,
            "%s.med" % outfile,
            Fmt.Salome,
            skip_types=skip_types,
            verbose=(DEBUG == 1),
        )
        mesh = medc.MEDFileUMesh("%s.med" % outfile)

    make_json = DEBUG == 1
    if make_json:
        jname = "%s.json" % (osp.splitext(osp.split(filename)[-1])[0])
        jpath = osp.join("/", "tmp", "_medconverter_json")
        os.makedirs(jpath, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w") as f:
            mesh.write(f.name, 2)
            create_test_json_file(f.name, osp.join(jpath, jname))

    return mesh


def deep_test_conversion(
    utest, filename, input_format, output_format, jsonfile, commtest=True, skip_types=[]
):
    """Function to deep check a mesh conversion.

    Arguments:
        utest (*unittest.TestCase*): Test object.
        filename (str): Input mesh file.
        input_format (str) : Type of input mesh (SYSTUS or ABAQUS)
        output_format (str) : Type of output mesh
        jsonfile (str) : The json file containing the reference values
    """

    mesh = base_test_conversion(utest, filename, input_format, output_format, commtest, skip_types)
    utest.assertTrue(isinstance(mesh, medc.MEDFileUMesh))

    with open(jsonfile) as f:
        refe = json.load(f)

    total_nb_of_cells = sum(mesh.getNumberOfCellsAtLevel(lev) for lev in mesh.getNonEmptyLevels())
    convertedcellstypes = [
        medc.MEDCouplingUMesh.GetReprOfGeometricType(i)
        for lev in mesh.getNonEmptyLevels()
        for i in mesh.getGeoTypesAtLevel(lev)
    ]
    total_nb_of_cells_groups = sum(
        len(mesh.getGroupsOnSpecifiedLev(lev)) for lev in mesh.getNonEmptyLevels()
    )

    utest.assertEqual(total_nb_of_cells, refe["NB_CELLS"])
    utest.assertEqual(total_nb_of_cells_groups, refe["NB_GRP_CELLS"])
    utest.assertEqual(len(mesh.getGroupsOnSpecifiedLev(1)), refe["NB_GRP_NODES"])
    utest.assertEqual(mesh.getNumberOfNodes(), refe["NB_NODES"])
    utest.assertSetEqual(set(mesh.getNonEmptyLevels()), set(map(int, refe["CELLS"].keys())))

    for n, coords in refe["NODES"].items():
        for c1, c2 in zip(mesh.getCoords()[int(n)].getValues(), coords):
            utest.assertAlmostEqual(c1, c2)

    refe_cells_types = []
    for lev, item in refe["CELLS"].items():
        for cell, values in item.items():
            idx = int(cell.split("_")[0].strip("ID"))
            cell_type = "NORM_%s" % cell.split("_")[1]
            refe_cells_types.append(cell_type)
            utest.assertEqual(
                medc.MEDCouplingUMesh.GetReprOfGeometricType(mesh[int(lev)].getTypeOfCell(idx)),
                cell_type,
            )
            utest.assertListEqual(mesh[int(lev)].getNodeIdsOfCell(idx), values, msg=cell)

    utest.assertSetEqual(set(convertedcellstypes), set(refe_cells_types))

    for lev, item in refe["GROUPS"].items():
        for name, values in item.items():
            utest.assertListEqual(
                mesh.getGroupArr(int(lev), name).getValues()[:MAX_ELTS_CHECK_GROUPS], values
            )
