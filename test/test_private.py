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


class TestPrivate(unittest.TestCase):
    def setUp(self):
        self._start_time = time.perf_counter()

    def tearDown(self):
        t = time.perf_counter() - self._start_time
        test_name = self.id().split(".")[-1]
        print("%s in %.3f sec" % (test_name, t))

    def test_systus_cuve(self):
        testname = "SYSTUS_01_CUVE_900_DONN20"
        filename = get_datafile_path("%s.ASC" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_systus_virole(self):
        testname = "SYSTUS_DONN9_VIROLE"
        filename = get_datafile_path("%s.ASC" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_systus_cuve_revet(self):
        testname = "SYSTUS_07_CUVE_900_REVET_FISS_DONN20"
        filename = get_datafile_path("%s.ASC" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_systus_coude(self):
        testname = "SYSTUS_COUDE_A_DONN1000"
        filename = get_datafile_path("%s.ASC" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_systus_coude_quad(self):
        testname = "SYSTUS_COUDE_A_QUAD_DONN1000"
        filename = get_datafile_path("%s.ASC" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_systus_piqu_insta(self):
        testname = "SYSTUS_PIQUAGE_RIS_900_INSTA_DONN1005"
        filename = get_datafile_path("%s.ASC" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_systus_piqu(self):
        testname = "SYSTUS_PIQUAGE_RIS_900_SAIN_DONN1005"
        filename = get_datafile_path("%s.ASC" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_abaqus_flam(self):
        testname = "ABAQUS_MAILLE_MF_FLAM-ELAS-CLEAN"
        filename = get_datafile_path("%s.inp" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_graphite(self):
        testname = "ABAQUS_HNBR3M"
        filename = get_datafile_path("%s.inp" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_eprouvette(self):
        testname = "ABAQUS_EPROUVETTE"
        filename = get_datafile_path("%s.inp" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_ansys_exemple_01(self):
        testname = "ANSYS_EXEMPLE_01"
        filename = get_datafile_path("%s.cdb" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_exemple_02(self):
        testname = "ANSYS_EXEMPLE_02"
        filename = get_datafile_path("%s.cdb" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_exemple_03(self):
        testname = "ANSYS_EXEMPLE_03"
        filename = get_datafile_path("%s.cdb" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_exemple_04(self):
        testname = "ANSYS_EXEMPLE_04"
        filename = get_datafile_path("%s.cdb" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_exemple_05(self):
        testname = "ANSYS_EXEMPLE_05"
        filename = get_datafile_path("%s.cdb" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_exemple_06(self):
        testname = "ANSYS_EXEMPLE_06"
        filename = get_datafile_path("%s.cdb" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_dynamic(self):
        testname = "ANSYS_Dynamic_Max"
        filename = get_datafile_path("%s.cdb" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_hw_b02(self):
        testname = "ANSYS_HW_B02-B03-Geo"
        filename = get_datafile_path("%s.cdb" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_hd_d2(self):
        testname = "ANSYS_HD_D2_Geo_B9"
        filename = get_datafile_path("%s.cdb" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_tube3d(self):
        testname = "ANSYS_TUBE3D"
        filename = get_datafile_path("%s.cdb" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_barrage(self):
        testname = "ANSYS_BARRAGE"
        filename = get_datafile_path("%s.cdb" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_cpp(self):
        testname = "ANSYS_CPP_N4"
        filename = get_datafile_path("%s.cdb" % testname)
        jsonfile = osp.join(data_path(), "json", "%s.json" % testname)
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile, commtest=False)


if __name__ == "__main__":
    unittest.main()
