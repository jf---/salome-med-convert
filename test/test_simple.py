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
from med_convert.engine import Fmt

class TestSimple(unittest.TestCase):

    def test_carre(self):
        standard_conversion(self, "CARRE_DONN1.ASC", Fmt.Systus, Fmt.Salome, 25, 96)

    def test_couronne(self):
        standard_conversion(self, "COURONNE_DONN1.ASC", Fmt.Systus, Fmt.Salome, 216, 720)

    def test_motif(self):
        standard_conversion(self, "MOTIF_DONN1.ASC", Fmt.Systus, Fmt.Salome, 96, 673)

    def test_rectangle(self):
        standard_conversion(self, "RECTANGLE_DONN1.ASC", Fmt.Systus, Fmt.Salome, 60, 213)

    def test_multi(self):
        standard_conversion(self, "MULTI_DONN1.ASC", Fmt.Systus, Fmt.Salome, 10, 61)
        standard_conversion(self, "MULTI_DONN1.med", Fmt.Salome, Fmt.Systus, 10, 61)

    def test_carre_abaqus(self):
        standard_conversion(self, "CARRE_1.inp", Fmt.Abaqus, Fmt.Salome, 1, 4)


if __name__ == "__main__":
    unittest.main()
