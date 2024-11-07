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

import time
import unittest
import os.path as osp

from medconverter.engine import Fmt
from medconverter.utilities import data_path
from utils_test import get_datafile_path, deep_test_conversion


class TestPerf(unittest.TestCase):
    def setUp(self):
        self._start_time = time.perf_counter()

    def tearDown(self):
        t = time.perf_counter() - self._start_time
        test_name = self.id().split(".")[-1]
        print("%s in %.3f sec" % (test_name, t))

    def test_systus_perf(self):
        testname = "SYSTUS_DONN408"
        filename = get_datafile_path(f"{testname}.ASC")
        jsonfile = osp.join(data_path(), "json", f"{testname}.json")
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_abaqus_perf(self):
        testname = "ABAQUS_PERF"
        filename = get_datafile_path(f"{testname}.inp")
        jsonfile = osp.join(data_path(), "json", f"{testname}.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_surface(self):
        testname = "ABAQUS_PERF"
        filename = osp.join(data_path(), f"{testname}.inp")
        jsonfile = osp.join(data_path(), "json", f"{testname}.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_hoj(self):
        testname = "ABAQUS_HOJ"
        folder = "ABAQUS_HOJ"
        filename = get_datafile_path("%s/%s" % (folder, "ABAQUS_Ad_E_Full_ELSE_BE_DAMP.txt"))
        filename = get_datafile_path("%s/%s" % (folder, "ABAQUS_HOJ_ASSEMBLY.txt"))
        filename = get_datafile_path("%s/%s" % (folder, "ABAQUS_HOJ_MASS_Ad_FULL.txt"))
        filename = get_datafile_path("%s/%s" % (folder, "ABAQUS_HOJ_MATERIAL_SEISMIC.txt"))
        filename = get_datafile_path("%s/%s" % (folder, "ABAQUS_HOJ_PART.txt"))
        filename = get_datafile_path(
            "%s/%s" % (folder, "ABAQUS_HOJ_Seismic_Spring_Gen_BE_Full_Emb_assembly.txt")
        )
        filename = get_datafile_path("%s/%s" % (folder, "ABAQUS_HOJ_v07_sets.txt"))
        filename = get_datafile_path("%s/%s" % (folder, "ABAQUS_HOJ_Spectra.txt"))
        filename = get_datafile_path("%s/%s" % (folder, "ABAQUS_HOJ_Ad_E_Full_RS_Y_BE.inp"))
        jsonfile = osp.join(data_path(), "json", f"{testname}.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_ansys_perf(self):
        testname = "ANSYS_PERF"
        filename = get_datafile_path(f"{testname}.cdb")
        jsonfile = osp.join(data_path(), "json", f"{testname}.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)


if __name__ == "__main__":
    unittest.main()
