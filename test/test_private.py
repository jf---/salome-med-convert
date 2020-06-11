
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

from utils_test import standard_conversion, get_datafile_path
from medconverter.engine import Fmt

class TestPrivate(unittest.TestCase):
    
    def test_cuve(self):
        filename = get_datafile_path("01_CUVE_900_DONN20.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            79848, 265476, ['QUAD8', 'HEXA20'])

    def test_cuve_revet(self):
        filename = get_datafile_path("07_CUVE_900_REVET_FISS_DONN20.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            124134, 400604, ['QUAD8','TRI6','PENTA15','SEG3','HEXA20'])

    def test_coude(self):
        filename = get_datafile_path("Coude_A_DONN1000.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            17714, 57817, ['SEG2', 'QUAD8', 'HEXA20'])

    def test_coude_quad(self):
        filename = get_datafile_path("Coude_A_quad_DONN1000.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            14858, 48433, ['SEG2', 'QUAD8', 'HEXA20'])

    def test_piqu_insta(self):
        filename = get_datafile_path("PIQUAGE_RIS_900_INSTA_DONN1005.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            120116, 454044, ['QUAD8','TRI6','PENTA15','SEG3','HEXA20'])

    def test_piqu(self):
        filename = get_datafile_path("PIQUAGE_RIS_900_SAIN_DONN1005.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            64492, 249292, ['QUAD8', 'HEXA20'])

    def test_ehp(self):
        filename = get_datafile_path("DONN408.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            367220, 1396501, ['QUAD8', 'HEXA20'])

    def test_flam(self):
        filename = get_datafile_path("Maille_MF_flam-elas-clean.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            1872, 1975, ['QUAD4'])


if __name__ == "__main__":
    unittest.main()
