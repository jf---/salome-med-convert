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


class TestSimple(unittest.TestCase):

    @tempdir
    def _standard_conversion(self, tmpdir, filename, nbcells, nbnodes):
        infile = osp.join(data_path(), filename)
        outfile = osp.join(tmpdir, "mesh.med")
        self.assertTrue(osp.isfile(infile))
        self.assertFalse(osp.isfile(outfile))

        convert(infile, Fmt.Systus, outfile)

        self.assertTrue(osp.isfile(outfile))
        mesh = MEDLoader.ReadMeshFromFile(outfile)
        self.assertEqual(mesh.getNumberOfCells(), nbcells)
        self.assertEqual(mesh.getNumberOfNodes(), nbnodes)


    def test_carre(self):
        self._standard_conversion("CARRE_DONN1.ASC", 25, 96)

    def test_couronne(self):
        self._standard_conversion("COURONNE_DONN1.ASC", 216, 720)

    @unittest.skip("QUAD8 type not yet supported")
    def test_motif(self):
        self._standard_conversion("MOTIF_DONN1.ASC", 114, 673)

    def test_motif_partial(self):
        # to be removed when test_motif is fixed
        self._standard_conversion("MOTIF_DONN1.ASC", 96, 673)

    def test_rectangle(self):
        self._standard_conversion("RECTANGLE_DONN1.ASC", 60, 213)


if __name__ == "__main__":
    unittest.main()
