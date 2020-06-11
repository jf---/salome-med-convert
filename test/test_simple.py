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

from utils_test import standard_conversion
from medconverter.engine import Fmt

class TestSimple(unittest.TestCase):

    def test_carre(self):
        standard_conversion(self, "CARRE_DONN1.ASC", Fmt.Systus, Fmt.Salome,
                            25, 96, ['QUAD8'])

    def test_couronne(self):
        standard_conversion(self, "COURONNE_DONN1.ASC", Fmt.Systus, Fmt.Salome,
                            216, 720, ['QUAD8'])

    def test_motif(self):
        standard_conversion(self, "MOTIF_DONN1.ASC", Fmt.Systus, Fmt.Salome,
                            114, 673, ['QUAD8','HEXA20'])

    def test_rectangle(self):
        standard_conversion(self, "RECTANGLE_DONN1.ASC", Fmt.Systus, Fmt.Salome,
                            60, 213, ['QUAD8'])

    def test_multi(self):
        standard_conversion(self, "MULTI_DONN1.ASC", Fmt.Systus, Fmt.Salome,
                            14, 61, ['TETRA4', 'PYRA5', 'PENTA6', 'HEXA8', 'TETRA10', 'PYRA13', 'PENTA15', 'HEXA20', 'TRI3', 'QUAD4', 'QUAD8'])
        standard_conversion(self, "MULTI_DONN1.med", Fmt.Salome, Fmt.Systus,
                            14, 61, ['TETRA4', 'PYRA5', 'PENTA6', 'HEXA8', 'TETRA10', 'PYRA13', 'PENTA15', 'HEXA20', 'TRI3', 'QUAD4', 'QUAD8'])

    def test_carre_abaqus(self):
        standard_conversion(self, "CARRE_1.inp", Fmt.Abaqus, Fmt.Salome,
                            1, 4, ['QUAD4'])


if __name__ == "__main__":
    unittest.main()
