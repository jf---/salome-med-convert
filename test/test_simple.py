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

from medconverter.utilities import data_path
from utils_test import standard_test_conversion, deep_test_conversion
from medconverter.engine import Fmt

class TestSimple(unittest.TestCase):

    def setUp(self):
        self._start_time = time.perf_counter()
        
    def tearDown(self):
        t = time.perf_counter() - self._start_time
        test_name = self.id().split('.')[-1]
        print('%s in %.3f sec' %(test_name, t))
    
    def test_systus_carre(self):
        filename = osp.join(data_path(),"SYSTUS_CARRE_DONN1.ASC")
        standard_test_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                                 25, 96, ['QUAD8'],
                                 1, 0)

    def test_systus_couronne(self):
        filename = osp.join(data_path(), "SYSTUS_COURONNE_DONN1.ASC")
        standard_test_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                                 216, 720, ['QUAD8'],
                                 1, 0)

    def test_systus_motif(self):
        filename = osp.join(data_path(), "SYSTUS_MOTIF_DONN1.ASC")
        standard_test_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                                 114, 673, ['QUAD8','HEXA20'],
                                 4, 0)
        
    def test_systus_rectangle(self):
        filename = osp.join(data_path(), "SYSTUS_RECTANGLE_DONN1.ASC")
        standard_test_conversion(self, filename, Fmt.Systus, Fmt.Salome,
                                 60, 213, ['QUAD8'],
                                 1, 0)
        
    def test_systus_multi(self):
        filename = osp.join(data_path(), "SYSTUS_MULTI_DONN1.ASC")
        jsonfile = osp.join(data_path(), 'json', "SYSTUS_MULTI_DONN1.json")
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)
        
        filename = osp.join(data_path(), "SALOME_MULTI_DONN1.med")
        standard_test_conversion(self, filename, Fmt.Salome, Fmt.Systus,
                                 17, 61, ['POINT1', 'SEG2', 'SEG3', 'TETRA4', 'PYRA5', 'PENTA6', 'HEXA8', 'TETRA10', 'PYRA13', 'PENTA15', 'HEXA20', 'TRI3', 'QUAD4', 'QUAD8', 'TRI6'],
                                 7, 2)

    def test_abaqus_carre(self):
        filename = osp.join(data_path(), "ABAQUS_CARRE_1.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1, 4, ['QUAD4'],
                                 3, 3)
        
    def test_abaqus_2cubesh20(self):
        filename = osp.join(data_path(), "ABAQUS_2CUBEH20.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 2, 32, ['HEXA20'],
                                 5, 3)

    def test_abaqus_hexa27(self):
        filename = osp.join(data_path(), "ABAQUS_HEXA27.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 4, 90, ['HEXA27'],
                                 4, 6)

    def test_abaqus_meshtet(self):
        filename = osp.join(data_path(), "ABAQUS_MESHTET.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 192, 457, ['TETRA10'],
                                 0,0)

    def test_abaqus_cpe6(self):
        filename = osp.join(data_path(), "ABAQUS_CPE6.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1, 6, ['TRI6'],
                                 1, 1)

    def test_abaqus_cpe8(self):
        filename = osp.join(data_path(), "ABAQUS_CPE8.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1, 8, ['QUAD8'],
                                 1, 1)

    def test_abaqus_pyra5_1element(self):
        filename = osp.join(data_path(), "ABAQUS_PYRA5_1ELEMENT.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1, 5, ['PYRA5'],
                                 0, 0)

    def test_abaqus_TET10(self):
        filename = osp.join(data_path(), "ABAQUS_TET10.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1, 10, ['TETRA10'],
                                 0, 0)

    def test_abaqus_2CUBE(self):
        filename = osp.join(data_path(), "ABAQUS_2CUBE.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 2, 12, ['HEXA8'],
                                 2, 2)

    def test_abaqus_CUBE(self):
        filename = osp.join(data_path(), "ABAQUS_CUBE.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1, 8, ['HEXA8'],
                                 2, 2)

    def test_abaqus_mixt_element(self):
        filename = osp.join(data_path(), "ABAQUS_MIXT_ELEMENT.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 4, 13, ['TETRA4','PYRA5','HEXA8','PENTA6'],
                                 4, 0)

    def test_abaqus_Beam_2(self):
        filename = osp.join(data_path(), "ABAQUS_BEAM2.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1, 2, ['SEG2'],
                                 1, 1)

    def test_abaqus_Beam_3(self):
        filename = osp.join(data_path(), "ABAQUS_BEAM3.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1, 3, ['SEG3'],
                                 1, 1)

    def test_abaqus_CPE3(self):
        filename = osp.join(data_path(), "ABAQUS_CPE3.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1, 3, ['TRI3'],
                                 1, 1)

    def test_abaqus_CPE4(self):
        filename = osp.join(data_path(), "ABAQUS_CPE4.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1, 4, ['QUAD4'],
                                 1, 1)

    def test_abaqus_PENTA6(self):
        filename = osp.join(data_path(), "ABAQUS_PENTA6.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 14, 16, ['PENTA6'],
                                 1, 0)

    def test_abaqus_PENTA15(self):
        filename = osp.join(data_path(), "ABAQUS_PENTA15.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 24, 127, ['PENTA15'],
                                 2, 1)

    def test_abaqus_PENTA15_1cell(self):
        filename = osp.join(data_path(), "ABAQUS_1EltPENTA15.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1, 15, ['PENTA15'],
                                 1, 0)

    def test_abaqus_PENTA15V(self):
        filename = osp.join(data_path(), "ABAQUS_PENTA15V.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 4, 54, ['PENTA18'],
                                 4, 6)

    def test_abaqus_MULTI_PENTA15V(self):
        filename = osp.join(data_path(), "ABAQUS_MULTI_PENTA15V.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_MULTI_PENTA15V.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                             jsonfile)

    def test_abaqus_TET4(self):
        filename = osp.join(data_path(), "ABAQUS_TET4.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1, 4, ['TETRA4'],
                                 2, 2)

    def test_abaqus_BOLT(self):
        filename = osp.join(data_path(), "ABAQUS_BOLTPIPEFLANGE_3D.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_BOLTPIPEFLANGE_3D.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                             jsonfile)

    def test_abaqus_Bending(self):
        filename = osp.join(data_path(), "ABAQUS_THREEPOINTBENDING.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 14600, 14973, ['QUAD4'],
                                 7, 5)

    def test_abaqus_Brake(self):
        filename = osp.join(data_path(), "ABAQUS_BRAKE.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 236, 288, ['QUAD4'],
                                 11, 4)

    def test_abaqus_notchedbeam(self):
        filename = osp.join(data_path(), "ABAQUS_NOTCHED_BEAM.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 165, 556, ['QUAD8'],
                                 2, 2)

    def test_abaqus_stackedassembly(self):
        filename = osp.join(data_path(), "ABAQUS_STACKEDASSEMBLY.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 984, 1117, ['TRI3', 'QUAD4'],
                                 8, 14)

    def test_abaqus_stackedassembly2(self):
        filename = osp.join(data_path(), "ABAQUS_STACKEDASSEMBLY2.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 984, 1117, ['TRI3', 'QUAD4'],
                                 8, 14)

    def test_abaqus_mass(self):
        filename = osp.join(data_path(), "ABAQUS_MASS.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 2, 2, ['POINT1','SEG2'],
                                 1, 2)

    def test_abaqus_spring(self):
        filename = osp.join(data_path(), "ABAQUS_SPRING.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 3, 3, ['POINT1','SEG2'],
                                 3, 2)

    def test_abaqus_smesh0(self):
        filename = osp.join(data_path(), "ABAQUS_SUBMESH_0.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 2, 32, ['HEXA20'],
                                 3, 3)

    def test_abaqus_selfcontact(self):
        filename = osp.join(data_path(), "ABAQUS_SELFCONTACT_BUMP_XPL_CAX3.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 1331, 746, ['POINT1','TRI3'],
                                 2, 6)

    def test_abaqus_adapt1(self):
        filename = osp.join(data_path(), "ABAQUS_ADAT_MESH_1.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 16001, 18492, ['POINT1','HEXA8'],
                                 5, 5)

    def test_abaqus_part(self):
        filename = osp.join(data_path(), "ABAQUS_PART.inp")
        standard_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome,
                                 8, 72, ["POINT1", "SEG2", 'HEXA20'],
                                 4, 5)

    def test_ansys_solid186_01_hexa(self):
        filename = osp.join(data_path(), "ANSYS_SOLID186_01_HEXA.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 20, ['HEXA20'],
                                 0, 0)

    def test_ansys_solid186_02_penta(self):
        filename = osp.join(data_path(), "ANSYS_SOLID186_02_PENTA.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 15, ['PENTA15'],
                                 0, 0)
                                 
    def test_ansys_solid186_03_tetra(self):
        filename = osp.join(data_path(), "ANSYS_SOLID186_03_TETRA.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 10, ['TETRA10'],
                                 0, 0)

    def test_ansys_solid186_04_pyra(self):
        filename = osp.join(data_path(), "ANSYS_SOLID186_04_PYRA.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 13, ['PYRA13'],
                                 0, 0)
                                 
    def test_ansys_beam188_2n(self):
        filename = osp.join(data_path(), "ANSYS_BEAM188_2n.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 2, ['SEG2'],
                                 0, 0)

    def test_ansys_beam188_3n(self):
        filename = osp.join(data_path(), "ANSYS_BEAM188_3n.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 3, ['SEG2'],
                                 0, 0)

    def test_ansys_beam189_3n(self):
        filename = osp.join(data_path(), "ANSYS_BEAM189_3n.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 3, ['SEG3'],
                                 0, 0)

    def test_ansys_beam189_4n(self):
        filename = osp.join(data_path(), "ANSYS_BEAM189_4n.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 4, ['SEG3'],
                                 0, 0)
                              
    def test_ansys_combin14(self):
        filename = osp.join(data_path(), "ANSYS_COMBIN14.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 2, ['SEG2'],
                                 0, 0)

    def test_ansys_link180(self):
        filename = osp.join(data_path(), "ANSYS_LINK180.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 2, ['SEG2'],
                                 0, 0)
                                        
    def test_ansys_pipe288_2n(self):
        filename = osp.join(data_path(), "ANSYS_PIPE288_2n.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 2, ['SEG2'],
                                 0, 0)

    def test_ansys_pipe288_3n(self):
        filename = osp.join(data_path(), "ANSYS_PIPE288_3n.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 3, ['SEG2'],
                                 0, 0)

    def test_ansys_pipe289_3n(self):
        filename = osp.join(data_path(), "ANSYS_PIPE289_3n.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 3, ['SEG3'],
                                 0, 0)

    def test_ansys_pipe289_4n(self):
        filename = osp.join(data_path(), "ANSYS_PIPE289_4n.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 4, ['SEG3'],
                                 0, 0)

    def test_ansys_plane182_01_quad(self):
        filename = osp.join(data_path(), "ANSYS_PLANE182_01_QUAD.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 4, ['QUAD4'],
                                 0, 0)

    def test_ansys_plane182_02_tri(self):
        filename = osp.join(data_path(), "ANSYS_PLANE182_02_TRI.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 3, ['TRI3'],
                                 0, 0)

    def test_ansys_plane183_01_quad(self):
        filename = osp.join(data_path(), "ANSYS_PLANE183_01_QUAD.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 8, ['QUAD8'],
                                 0, 0)

    def test_ansys_plane183_02_tri(self):
        filename = osp.join(data_path(), "ANSYS_PLANE183_02_TRI.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 6, ['TRI6'],
                                 0, 0)
                                 
    def test_ansys_shell181_01_quad(self):
        filename = osp.join(data_path(), "ANSYS_SHELL181_01_QUAD.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 4, ['QUAD4'],
                                 0, 0)

    def test_ansys_shell181_02_tri(self):
        filename = osp.join(data_path(), "ANSYS_SHELL181_02_TRI.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 3, ['TRI3'],
                                 0, 0)

    def test_ansys_shell281_01_quad(self):
        filename = osp.join(data_path(), "ANSYS_SHELL281_01_QUAD.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 8, ['QUAD8'],
                                 0, 0)
                          
    def test_ansys_shell281_02_tri(self):
        filename = osp.join(data_path(), "ANSYS_SHELL281_02_TRI.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 6, ['TRI6'],
                                 0, 0)

    def test_ansys_solid185_01_hexa(self):
        filename = osp.join(data_path(), "ANSYS_SOLID185_01_HEXA.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 8, ['HEXA8'],
                                 0, 0)

    def test_ansys_solid185_02_penta(self):
        filename = osp.join(data_path(), "ANSYS_SOLID185_02_PENTA.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 6, ['PENTA6'],
                                 0, 0)

    def test_ansys_solid185_03_tetra(self):
        filename = osp.join(data_path(), "ANSYS_SOLID185_03_TETRA.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 4, ['TETRA4'],
                                 0, 0)

    def test_ansys_solid185_04_pyra(self):
        filename = osp.join(data_path(), "ANSYS_SOLID185_04_PYRA.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 5, ['PYRA5'],
                                 0, 0)

    def test_ansys_solid187(self):
        filename = osp.join(data_path(), "ANSYS_SOLID187.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 1, 10, ['TETRA10'],
                                 0, 0)
    
    def test_ansys_hexbeam(self):
        filename = osp.join(data_path(), "ANSYS_HexBeam.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 40, 321, ['HEXA20'],
                                 2, 2)
                                 
    def test_ansys_sector(self):
        filename = osp.join(data_path(), "ANSYS_Sector.cdb")
        standard_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome,
                                 105, 655, ['HEXA8', 'PENTA6'],
                                 0, 1)

        
    def test_zset_multi(self):
        filename = osp.join(data_path(), "ZSET_MULTI.geof")
        standard_test_conversion(self, filename, Fmt.Zset, Fmt.Salome,
                                 16, 61, ['SEG2', 'SEG3', 'TETRA4', 'PYRA5', 'PENTA6', 'HEXA8', 'TETRA10', 'PYRA13', 'PENTA15', 'HEXA20', 'TRI3', 'QUAD4', 'QUAD8', 'TRI6'],
                                 6, 2)
        
if __name__ == "__main__":
    unittest.main()
