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
import os.path as osp

from medconverter.utilities import data_path
from utils_test import standard_conversion
from medconverter.engine import Fmt

class TestSimple(unittest.TestCase):

    def test_carre(self):
        filename = osp.join(data_path(),"CARRE_DONN1.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            25, 96, ['QUAD8'])

    def test_couronne(self):
        filename = osp.join(data_path(), "COURONNE_DONN1.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            216, 720, ['QUAD8'])

    def test_motif(self):
        filename = osp.join(data_path(), "MOTIF_DONN1.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            114, 673, ['QUAD8','HEXA20'])

    def test_rectangle(self):
        filename = osp.join(data_path(), "RECTANGLE_DONN1.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            60, 213, ['QUAD8'])

    def test_multi(self):
        filename = osp.join(data_path(), "MULTI_DONN1.ASC")
        standard_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                            14, 61, ['TETRA4', 'PYRA5', 'PENTA6', 'HEXA8', 'TETRA10', 'PYRA13', 'PENTA15', 'HEXA20', 'TRI3', 'QUAD4', 'QUAD8'])

        filename = osp.join(data_path(), "MULTI_DONN1.med")
        standard_conversion(self, filename, Fmt.Salome, Fmt.Systus,
                            14, 61, ['TETRA4', 'PYRA5', 'PENTA6', 'HEXA8', 'TETRA10', 'PYRA13', 'PENTA15', 'HEXA20', 'TRI3', 'QUAD4', 'QUAD8'])

    def test_carre_abaqus(self):
        filename = osp.join(data_path(), "CARRE_1.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            1, 4, ['QUAD4'])

    def test_2cubesh20_abaqus(self):
        filename = osp.join(data_path(), "2CUBEH20.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            2, 32, ['HEXA20'])

    def test_meshtet_abaqus(self):
        filename = osp.join(data_path(), "meshtet.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            192, 457, ['TETRA10'])

    def test_pyra5_1element_abaqus(self):
        filename = osp.join(data_path(), "pyra5_1element.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            1, 5, ['PYRA5'])

    def test_TET10_abaqus(self):
        filename = osp.join(data_path(), "TET10.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            1, 10, ['TETRA10'])

    def test_2CUBE_abaqus(self):
        filename = osp.join(data_path(), "2CUBE.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            2, 12, ['HEXA8'])

    def test_CUBE_abaqus(self):
        filename = osp.join(data_path(), "CUBE.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            1, 8, ['HEXA8'])

    def test_mixt_element_abaqus(self):
        filename = osp.join(data_path(), "mixt_element.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            4, 13, ['TETRA4','PYRA5','HEXA8','PENTA6'])

    def test_PENTA6_abaqus(self):
        filename = osp.join(data_path(), "PENTA6.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            14, 16, ['PENTA6'])

    def test_TET4_abaqus(self):
        filename = osp.join(data_path(), "TET4.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            1, 4, ['TETRA4'])

    def test_BOLT_abaqus(self):
        filename = osp.join(data_path(), "boltpipeflange_3d.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            2000, 10587, ['HEXA20','PENTA15'])

    def test_Bending_abaqus(self):
        filename = osp.join(data_path(), "ThreePointBending.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            14600, 14973, ['QUAD4'])

    def test_Brake_abaqus(self):
        filename = osp.join(data_path(), "BRAKE.inp")
        standard_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                            236, 288, ['QUAD4'])





if __name__ == "__main__":
    unittest.main()
