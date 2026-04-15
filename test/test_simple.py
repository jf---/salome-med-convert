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

import os.path as osp
import time
import unittest

from utils_test import deep_test_conversion

from medconverter.engine import Fmt
from medconverter.utilities import data_path


class TestSimple(unittest.TestCase):
    def setUp(self):
        self._start_time = time.perf_counter()

    def tearDown(self):
        t = time.perf_counter() - self._start_time
        test_name = self.id().split(".")[-1]
        print("%s in %.3f sec" % (test_name, t))

    def test_systus_carre(self):
        filename = osp.join(data_path(), "SYSTUS_CARRE_DONN1.ASC")
        jsonfile = osp.join(data_path(), "json", "SYSTUS_CARRE_DONN1.json")
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_systus_error(self):
        filename = osp.join(data_path(), "SYSTUS_CARRE_ERRORS_DONN1.ASC")
        jsonfile = osp.join(data_path(), "json", "SYSTUS_CARRE_DONN1.json")
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile, skip_types=["1902"])

    def test_systus_couronne(self):
        filename = osp.join(data_path(), "SYSTUS_COURONNE_DONN1.ASC")
        jsonfile = osp.join(data_path(), "json", "SYSTUS_COURONNE_DONN1.json")
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_systus_motif(self):
        filename = osp.join(data_path(), "SYSTUS_MOTIF_DONN1.ASC")
        jsonfile = osp.join(data_path(), "json", "SYSTUS_MOTIF_DONN1.json")
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_systus_rectangle(self):
        filename = osp.join(data_path(), "SYSTUS_RECTANGLE_DONN1.ASC")
        jsonfile = osp.join(data_path(), "json", "SYSTUS_RECTANGLE_DONN1.json")
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_systus_multi(self):
        filename = osp.join(data_path(), "SYSTUS_MULTI_DONN1.ASC")
        jsonfile = osp.join(data_path(), "json", "MESH_MULTI_WITH0D.json")
        deep_test_conversion(self, filename, Fmt.Systus, Fmt.Salome, jsonfile)

    def test_abaqus_carre(self):
        filename = osp.join(data_path(), "ABAQUS_CARRE_1.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_CARRE_1.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_2cubesh20(self):
        filename = osp.join(data_path(), "ABAQUS_2CUBEH20.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_2CUBEH20.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_hexa27(self):
        filename = osp.join(data_path(), "ABAQUS_HEXA27.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_HEXA27.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_meshtet(self):
        filename = osp.join(data_path(), "ABAQUS_MESHTET.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_MESHTET.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_cpe6(self):
        filename = osp.join(data_path(), "ABAQUS_CPE6.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_CPE6.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_cpe8(self):
        filename = osp.join(data_path(), "ABAQUS_CPE8.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_CPE8.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_pyra5_1element(self):
        filename = osp.join(data_path(), "ABAQUS_PYRA5_1ELEMENT.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_PYRA5_1ELEMENT.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_TET10(self):
        filename = osp.join(data_path(), "ABAQUS_TET10.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_TET10.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_2CUBE(self):
        filename = osp.join(data_path(), "ABAQUS_2CUBE.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_2CUBE.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_CUBE(self):
        filename = osp.join(data_path(), "ABAQUS_CUBE.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_CUBE.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_mixt_element(self):
        filename = osp.join(data_path(), "ABAQUS_MIXT_ELEMENT.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_MIXT_ELEMENT.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_Beam_2(self):
        filename = osp.join(data_path(), "ABAQUS_BEAM2.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_BEAM2.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_Beam_3(self):
        filename = osp.join(data_path(), "ABAQUS_BEAM3.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_BEAM3.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_CPE3(self):
        filename = osp.join(data_path(), "ABAQUS_CPE3.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_CPE3.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_CPE4(self):
        filename = osp.join(data_path(), "ABAQUS_CPE4.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_CPE4.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_PENTA6(self):
        filename = osp.join(data_path(), "ABAQUS_PENTA6.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_PENTA6.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_PENTA15(self):
        filename = osp.join(data_path(), "ABAQUS_PENTA15.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_PENTA15.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_PENTA15_1cell(self):
        filename = osp.join(data_path(), "ABAQUS_1EltPENTA15.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_1EltPENTA15.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_PENTA15V(self):
        filename = osp.join(data_path(), "ABAQUS_PENTA15V.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_PENTA15V.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_MULTI_PENTA15V(self):
        filename = osp.join(data_path(), "ABAQUS_MULTI_PENTA15V.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_MULTI_PENTA15V.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_TET4(self):
        filename = osp.join(data_path(), "ABAQUS_TET4.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_TET4.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_BOLT(self):
        filename = osp.join(data_path(), "ABAQUS_BOLTPIPEFLANGE_3D.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_BOLTPIPEFLANGE_3D.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_Bending(self):
        filename = osp.join(data_path(), "ABAQUS_THREEPOINTBENDING.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_THREEPOINTBENDING.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_Brake(self):
        filename = osp.join(data_path(), "ABAQUS_BRAKE.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_BRAKE.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_notchedbeam(self):
        filename = osp.join(data_path(), "ABAQUS_NOTCHED_BEAM.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_NOTCHED_BEAM.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_stackedassembly(self):
        filename = osp.join(data_path(), "ABAQUS_STACKEDASSEMBLY.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_STACKEDASSEMBLY.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_stackedassembly2(self):
        filename = osp.join(data_path(), "ABAQUS_STACKEDASSEMBLY2.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_STACKEDASSEMBLY2.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_mass(self):
        filename = osp.join(data_path(), "ABAQUS_MASS.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_MASS.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_spring(self):
        filename = osp.join(data_path(), "ABAQUS_SPRING.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_SPRING.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_smesh0(self):
        filename = osp.join(data_path(), "ABAQUS_SUBMESH_0.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_SUBMESH_0.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_selfcontact(self):
        filename = osp.join(data_path(), "ABAQUS_SELFCONTACT_BUMP_XPL_CAX3.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_SELFCONTACT_BUMP_XPL_CAX3.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_adapt1(self):
        filename = osp.join(data_path(), "ABAQUS_ADAT_MESH_1.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_ADAT_MESH_1.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_part(self):
        filename = osp.join(data_path(), "ABAQUS_PART.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_PART.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_abaqus_multi_parts(self):
        filename = osp.join(data_path(), "ABAQUS_MULTI_PARTS.inp")
        jsonfile = osp.join(data_path(), "json", "ABAQUS_MULTI_PARTS.json")
        deep_test_conversion(self, filename, Fmt.Abaqus, Fmt.Salome, jsonfile)

    def test_ansys_solid186_01_hexa(self):
        filename = osp.join(data_path(), "ANSYS_SOLID186_01_HEXA.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_SOLID186_01_HEXA.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_solid186_02_penta(self):
        filename = osp.join(data_path(), "ANSYS_SOLID186_02_PENTA.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_SOLID186_02_PENTA.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_solid186_03_tetra(self):
        filename = osp.join(data_path(), "ANSYS_SOLID186_03_TETRA.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_SOLID186_03_TETRA.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_solid186_04_pyra(self):
        filename = osp.join(data_path(), "ANSYS_SOLID186_04_PYRA.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_SOLID186_04_PYRA.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_beam188_2n(self):
        filename = osp.join(data_path(), "ANSYS_BEAM188_2n.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_BEAM188_2n.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_beam188_3n(self):
        filename = osp.join(data_path(), "ANSYS_BEAM188_3n.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_BEAM188_3n.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_beam189_3n(self):
        filename = osp.join(data_path(), "ANSYS_BEAM189_3n.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_BEAM189_3n.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_beam189_4n(self):
        filename = osp.join(data_path(), "ANSYS_BEAM189_4n.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_BEAM189_4n.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_beam189_section_c(self):
        filename = osp.join(data_path(), "ANSYS_BEAM189_section_C.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_BEAM189_section_C.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_beam189_section_hats(self):
        filename = osp.join(data_path(), "ANSYS_BEAM189_section_Hats.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_BEAM189_section_Hats.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_beam189_section_i(self):
        filename = osp.join(data_path(), "ANSYS_BEAM189_section_I.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_BEAM189_section_I.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_beam189_section_l(self):
        filename = osp.join(data_path(), "ANSYS_BEAM189_section_L.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_BEAM189_section_L.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_beam189_section_t(self):
        filename = osp.join(data_path(), "ANSYS_BEAM189_section_T.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_BEAM189_section_T.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_beam189_section_z(self):
        filename = osp.join(data_path(), "ANSYS_BEAM189_section_Z.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_BEAM189_section_Z.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_combin14(self):
        filename = osp.join(data_path(), "ANSYS_COMBIN14.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_COMBIN14.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_link180(self):
        filename = osp.join(data_path(), "ANSYS_LINK180.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_LINK180.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_pipe288_2n(self):
        filename = osp.join(data_path(), "ANSYS_PIPE288_2n.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_PIPE288_2n.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_pipe288_3n(self):
        filename = osp.join(data_path(), "ANSYS_PIPE288_3n.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_PIPE288_3n.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_pipe289_3n(self):
        filename = osp.join(data_path(), "ANSYS_PIPE289_3n.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_PIPE289_3n.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_pipe289_4n(self):
        filename = osp.join(data_path(), "ANSYS_PIPE289_4n.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_PIPE289_4n.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_plane182_01_quad(self):
        filename = osp.join(data_path(), "ANSYS_PLANE182_01_QUAD.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_PLANE182_01_QUAD.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_plane182_02_tri(self):
        filename = osp.join(data_path(), "ANSYS_PLANE182_02_TRI.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_PLANE182_02_TRI.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_plane183_01_quad(self):
        filename = osp.join(data_path(), "ANSYS_PLANE183_01_QUAD.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_PLANE183_01_QUAD.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_plane183_02_tri(self):
        filename = osp.join(data_path(), "ANSYS_PLANE183_02_TRI.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_PLANE183_02_TRI.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_shell181_01_quad(self):
        filename = osp.join(data_path(), "ANSYS_SHELL181_01_QUAD.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_SHELL181_01_QUAD.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_shell181_02_tri(self):
        filename = osp.join(data_path(), "ANSYS_SHELL181_02_TRI.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_SHELL181_02_TRI.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_shell281_01_quad(self):
        filename = osp.join(data_path(), "ANSYS_SHELL281_01_QUAD.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_SHELL281_01_QUAD.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_shell281_02_tri(self):
        filename = osp.join(data_path(), "ANSYS_SHELL281_02_TRI.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_SHELL281_02_TRI.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_solid185_01_hexa(self):
        filename = osp.join(data_path(), "ANSYS_SOLID185_01_HEXA.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_SOLID185_01_HEXA.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_solid185_02_penta(self):
        filename = osp.join(data_path(), "ANSYS_SOLID185_02_PENTA.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_SOLID185_02_PENTA.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_solid185_03_tetra(self):
        filename = osp.join(data_path(), "ANSYS_SOLID185_03_TETRA.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_SOLID185_03_TETRA.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_solid185_04_pyra(self):
        filename = osp.join(data_path(), "ANSYS_SOLID185_04_PYRA.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_SOLID185_04_PYRA.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_solid187(self):
        filename = osp.join(data_path(), "ANSYS_SOLID187.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_SOLID187.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_hexbeam(self):
        filename = osp.join(data_path(), "ANSYS_HexBeam.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_HexBeam.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_sector(self):
        filename = osp.join(data_path(), "ANSYS_Sector.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_Sector.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_link180_cable(self):
        filename = osp.join(data_path(), "ANSYS_LINK180_cable.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_LINK180_cable.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_modele_FE_mixte_v4(self):
        filename = osp.join(data_path(), "ANSYS_Modele_FE_Mixte_v4.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_Modele_FE_Mixte_v4.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_plane183_03_tri(self):
        filename = osp.join(data_path(), "ANSYS_PLANE183_03_TRI.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_PLANE183_03_TRI.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_ansys_cube(self):
        filename = osp.join(data_path(), "ANSYS_CUBE.cdb")
        jsonfile = osp.join(data_path(), "json", "ANSYS_CUBE.json")
        deep_test_conversion(self, filename, Fmt.Ansys, Fmt.Salome, jsonfile)

    def test_zset_multi(self):
        filename = osp.join(data_path(), "ZSET_MULTI.geof")
        jsonfile = osp.join(data_path(), "json", "MESH_MULTI_WITHOUT0D.json")
        deep_test_conversion(self, filename, Fmt.Zset, Fmt.Salome, jsonfile)

    def test_aster_multi(self):
        filename = osp.join(data_path(), "ASTER_MULTI.mail")
        jsonfile = osp.join(data_path(), "json", "MESH_MULTI_WITH0D.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_tetgen_convt01(self):
        filename = osp.join(data_path(), "TETGEN_CONVT01.mesh")
        jsonfile = osp.join(data_path(), "json", "TETGEN_CONVT01.json")
        deep_test_conversion(self, filename, Fmt.Tetgen, Fmt.Salome, jsonfile)

    def test_tetgen_cube325(self):
        filename = osp.join(data_path(), "TETGEN_CUBE325.mesh")
        jsonfile = osp.join(data_path(), "json", "TETGEN_CUBE325.json")
        deep_test_conversion(self, filename, Fmt.Tetgen, Fmt.Salome, jsonfile)

    def test_tetgen_tetra01(self):
        filename = osp.join(data_path(), "TETGEN_TETRA01.mesh")
        jsonfile = osp.join(data_path(), "json", "TETGEN_TETRA01.json")
        deep_test_conversion(self, filename, Fmt.Tetgen, Fmt.Salome, jsonfile)

    def test_tetgen_fvca6_tet1(self):
        filename = osp.join(data_path(), "TETGEN_FVCA6_1.mesh")
        jsonfile = osp.join(data_path(), "json", "TETGEN_FVCA6_1.json")
        deep_test_conversion(self, filename, Fmt.Tetgen, Fmt.Salome, jsonfile)

    def test_salome_systus_empty_level(self):
        filename = osp.join(data_path(), "SALOME_BOX.med")
        jsonfile = osp.join(data_path(), "json", "SALOME_BOX.json")
        deep_test_conversion(self, filename, Fmt.Salome, Fmt.Systus, jsonfile)

    def test_salome_aster_empty_level(self):
        filename = osp.join(data_path(), "SALOME_BOX.med")
        jsonfile = osp.join(data_path(), "json", "SALOME_BOX.json")
        deep_test_conversion(self, filename, Fmt.Salome, Fmt.Aster, jsonfile)


if __name__ == "__main__":
    unittest.main()
