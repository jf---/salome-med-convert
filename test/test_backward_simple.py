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

    def test_backward_aster_multi(self):
        filename = osp.join(data_path(), "SALOME_MULTI_DONN1_WITH0D.med")
        jsonfile = osp.join(data_path(), "json", "MESH_MULTI_WITH0D.json")
        deep_test_conversion(self, filename, Fmt.Salome, Fmt.Aster, jsonfile)

    def test_backward_zset_multi(self):
        filename = osp.join(data_path(), "SALOME_MULTI_DONN1_WITHOUT0D.med")
        jsonfile = osp.join(data_path(), "json", "MESH_MULTI_WITHOUT0D.json")
        deep_test_conversion(self, filename, Fmt.Salome, Fmt.Zset, jsonfile)

    def test_backward_systus_multi(self):
        filename = osp.join(data_path(), "SALOME_MULTI_DONN1_WITH0D.med")
        jsonfile = osp.join(data_path(), "json", "MESH_MULTI_WITH0D.json")
        deep_test_conversion(self, filename, Fmt.Salome, Fmt.Systus, jsonfile)


if __name__ == "__main__":
    unittest.main()
