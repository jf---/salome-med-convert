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

from utils_test import standard_test_conversion, get_datafile_path, deep_test_conversion
from medconverter.engine import Fmt
from medconverter.utilities import data_path

class TestPrivate(unittest.TestCase):
    
    def setUp(self):
        self._start_time = time.perf_counter()
        
    def tearDown(self):
        t = time.perf_counter() - self._start_time
        test_name = self.id().split('.')[-1]
        print('%s in %.3f sec' %(test_name, t))   
    
    def test_cuve(self):
        filename = get_datafile_path("SYSTUS_01_CUVE_900_DONN20.ASC")
        standard_test_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                                 79848, 265476, ['QUAD8', 'HEXA20'],
                                 35, 5)

    def test_cuve_revet(self):
        filename = get_datafile_path("SYSTUS_07_CUVE_900_REVET_FISS_DONN20.ASC")
        jsonfile = osp.join(data_path(), 'json', "SYSTUS_07_CUVE_900_REVET_FISS_DONN20.json")
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)
               
    def test_coude(self):
        filename = get_datafile_path("SYSTUS_COUDE_A_DONN1000.ASC")
        standard_test_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                                 17714, 57817, ['SEG2', 'QUAD8', 'HEXA20'],
                                 68, 1)
        
    def test_coude_quad(self):
        filename = get_datafile_path("SYSTUS_COUDE_A_QUAD_DONN1000.ASC")
        standard_test_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                                 14858, 48433, ['SEG2', 'QUAD8', 'HEXA20'],
                                 65, 1)

    def test_piqu_insta(self):
        filename = get_datafile_path("SYSTUS_PIQUAGE_RIS_900_INSTA_DONN1005.ASC")
        jsonfile = osp.join(data_path(), 'json', "SYSTUS_PIQUAGE_RIS_900_INSTA_DONN1005.json")
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_piqu(self):
        filename = get_datafile_path("SYSTUS_PIQUAGE_RIS_900_SAIN_DONN1005.ASC")
        standard_test_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                                 64492, 249292, ['QUAD8', 'HEXA20'],
                                 27, 3)
        
    def test_ehp(self):
        filename = get_datafile_path("SYSTUS_DONN408.ASC")
        standard_test_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                                 367220, 1396501, ['QUAD8', 'HEXA20'],
                                 4, 0)

    def test_flam(self):
        filename = get_datafile_path("ABAQUS_MAILLE_MF_FLAM-ELAS-CLEAN.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1872, 1976, ['QUAD4'],
                                 9, 8)

    def test_graphite(self):
        filename = get_datafile_path("ABAQUS_HNBR3M.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 35904, 176092, ['HEXA20'],
                                 1, 0)

    def test_perf(self):
        filename = get_datafile_path("ABAQUS_PERF.inp")
        jsonfile = osp.join(data_path(), 'json', "ABAQUS_PERF.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)


    def test_ansys_exemple_01(self):
        filename = get_datafile_path("ANSYS_EXEMPLE_01.cdb")
        jsonfile = osp.join(data_path(), 'json', "ANSYS_EXEMPLE_01.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_exemple_02(self):
        filename = get_datafile_path("ANSYS_EXEMPLE_02.cdb")
        jsonfile = osp.join(data_path(), 'json', "ANSYS_EXEMPLE_02.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)
                                 
    def test_ansys_exemple_03(self):
        filename = get_datafile_path("ANSYS_EXEMPLE_03.cdb")
        jsonfile = osp.join(data_path(), 'json', "ANSYS_EXEMPLE_03.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)
                                 
    def test_ansys_exemple_04(self):
        filename = get_datafile_path("ANSYS_EXEMPLE_04.cdb")
        jsonfile = osp.join(data_path(), 'json', "ANSYS_EXEMPLE_04.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)
 
    def test_ansys_exemple_05(self):
        filename = get_datafile_path("ANSYS_EXEMPLE_05.cdb")
        jsonfile = osp.join(data_path(), 'json', "ANSYS_EXEMPLE_05.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_exemple_06(self):
        filename = get_datafile_path("ANSYS_EXEMPLE_06.cdb")
        jsonfile = osp.join(data_path(), 'json', "ANSYS_EXEMPLE_06.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_perf(self):
        filename = get_datafile_path("ANSYS_PERF.cdb")
        jsonfile = osp.join(data_path(), 'json', "ANSYS_PERF.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

if __name__ == "__main__":
    unittest.main()
