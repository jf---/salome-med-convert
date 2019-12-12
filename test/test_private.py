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


class TestPrivate(unittest.TestCase):

    def test_cuve(self):
        # total: 79848
        standard_conversion(self, "01_CUVE_900_DONN20.ASC", "SYSTUS",
                            58958, 265476, private=True)

    def test_cuve_revet(self):
        # total: 124134
        standard_conversion(self, "07_CUVE_900_REVET_FISS_DONN20.ASC", "SYSTUS",
                            92094, 400604, private=True)

    def test_coude(self):
        # total: 17714
        standard_conversion(self, "Coude_A_DONN1000.ASC", "SYSTUS",
                            12480, 57817, private=True)

    def test_coude_quad(self):
        # total: 14858
        standard_conversion(self, "Coude_A_quad_DONN1000.ASC", "SYSTUS",
                            10440, 48433, private=True)

    def test_piqu_insta(self):
        standard_conversion(self, "PIQUAGE_RIS_900_INSTA_DONN1005.ASC", "SYSTUS",
                            105666, 454044, private=True)

    def test_piqu(self):
        # total: 64492
        standard_conversion(self, "PIQUAGE_RIS_900_SAIN_DONN1005.ASC", "SYSTUS",
                            56674, 249292, private=True)

    def test_ehp(self):
        # total: 64492
        standard_conversion(self, "DONN408.ASC", "SYSTUS",
                            338100, 1396501, private=True)


if __name__ == "__main__":
    unittest.main()
