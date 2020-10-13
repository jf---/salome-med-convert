
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

import unittest
import time

from utils_test import standard_conversion, get_datafile_path
from medconverter.engine import Fmt

class TestPrivate(unittest.TestCase):

    def setUp(self):
        self.startTime = time.perf_counter()

    def tearDown(self):
        t = time.perf_counter() - self.startTime
        print('%s in %.3f sec' %(self.id(), t))

    def test_cuve(self):
        filename = get_datafile_path("SYSTUS_01_CUVE_900_DONN20.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            79848, 265476, ['QUAD8', 'HEXA20'],
                            35, 5)

    def test_cuve_revet(self):
        filename = get_datafile_path("SYSTUS_07_CUVE_900_REVET_FISS_DONN20.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            124134, 400604, ['QUAD8','TRI6','PENTA15','SEG3','HEXA20'],
                            62, 12)

    def test_coude(self):
        filename = get_datafile_path("SYSTUS_COUDE_A_DONN1000.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            17714, 57817, ['SEG2', 'QUAD8', 'HEXA20'],
                            68, 1)

    def test_coude_quad(self):
        filename = get_datafile_path("SYSTUS_COUDE_A_QUAD_DONN1000.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            14858, 48433, ['SEG2', 'QUAD8', 'HEXA20'],
                            65, 1)

    def test_piqu_insta(self):
        filename = get_datafile_path("SYSTUS_PIQUAGE_RIS_900_INSTA_DONN1005.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            120116, 454044, ['QUAD8','TRI6','PENTA15','SEG3','HEXA20'],
                            48, 7)

    def test_piqu(self):
        filename = get_datafile_path("SYSTUS_PIQUAGE_RIS_900_SAIN_DONN1005.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            64492, 249292, ['QUAD8', 'HEXA20'],
                            27, 3)

    def test_ehp(self):
        filename = get_datafile_path("SYSTUS_DONN408.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            367220, 1396501, ['QUAD8', 'HEXA20'],
                            4, 0)

    def test_flam(self):
        filename = get_datafile_path("ABAQUS_MAILLE_MF_FLAM-ELAS-CLEAN.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            1872, 1976, ['QUAD4'],
                            9, 8)

    def test_graphite(self):
        filename = get_datafile_path("ABAQUS_HNBR3M.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            35904, 176092, ['HEXA20'],
                            1, 0)

    def test_perf(self):
        filename = get_datafile_path("ABAQUS_PERF.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            600768, 969128, ['HEXA8', 'TETRA10'],
                            14, 17)



if __name__ == "__main__":
    unittest.main()
