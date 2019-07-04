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
import unittest
from functools import wraps

from med_convert.convert import Fmt, convert
from med_convert.utilities import data_path


try:
    import MEDLoader
except ImportError:
    sys.stderr.write("Please read the README file to execute the unittests "
                     "inside SALOME environment.")
    raise


def tempdir(func):
    """Decorator that executes a method in a temporary directory.
    Expected method signature: `func(self, tmpdir, ...)`.
    """

    @wraps(func)
    def wrapper(self, *args, **kwds):
        """wrapper"""
        retcode = None
        try:
            tmpdir = tempfile.mkdtemp(prefix='tmp_medconvert_')
            retcode = func(self, tmpdir, *args, **kwds)
        except Exception:
            sys.stderr.write("temporary directory is: {0}\n".format(tmpdir))
            raise
        else:
            if osp.exists(tmpdir):
                shutil.rmtree(tmpdir)
        return retcode
    return wrapper


DEBUG = int(os.getenv("DEBUG", 0))

class TestPrivate(unittest.TestCase):

    @tempdir
    def _standard_conversion(self, tmpdir, filename, nbcells, nbnodes):
        infile = osp.join(data_path(), os.pardir, "data_private", filename)
        outfile = osp.join(tmpdir if DEBUG != 1 else os.getcwd(),
                           osp.splitext(osp.basename(filename))[0] + ".med")
        self.assertTrue(osp.isfile(infile))
        if DEBUG != 1:
            self.assertFalse(osp.isfile(outfile))

        convert(infile, Fmt.Systus, outfile, verbose=(DEBUG == 1))

        self.assertTrue(osp.isfile(outfile))
        mesh = MEDLoader.ReadMeshFromFile(outfile)
        if nbcells * nbnodes == 0:
            print("Number of elements:", mesh.getNumberOfCells())
            print("Number of nodes:", mesh.getNumberOfNodes())
        else:
            self.assertEqual(mesh.getNumberOfCells(), nbcells)
            self.assertEqual(mesh.getNumberOfNodes(), nbnodes)


    def test_cuve(self):
        # total: 79848
        self._standard_conversion("01_CUVE_900_DONN20.ASC", 58958, 265476)

    def test_cuve_revet(self):
        # total: 124134
        self._standard_conversion("07_CUVE_900_REVET_FISS_DONN20.ASC", 92094, 400604)

    def test_coude(self):
        # total: 17714
        self._standard_conversion("Coude_A_DONN1000.ASC", 12480, 57817)

    def test_coude_quad(self):
        # total: 14858
        self._standard_conversion("Coude_A_quad_DONN1000.ASC", 10440, 48433)

    def test_piqu_insta(self):
        self._standard_conversion("PIQUAGE_RIS_900_INSTA_DONN1005.ASC", 105666, 454044)

    def test_piqu(self):
        # total: 64492
        self._standard_conversion("PIQUAGE_RIS_900_SAIN_DONN1005.ASC", 56674, 249292)

    def test_ehp(self):
        # total: 64492
        self._standard_conversion("DONN408.ASC", 338100, 1396501)


if __name__ == "__main__":
    unittest.main()
