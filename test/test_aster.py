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

    def test_aster_sdll100a(self):
        filename = osp.join(data_path(), "meshaster", "sdll100a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll100a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv143b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv143b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv143b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_shll103a(self):
        filename = osp.join(data_path(), "meshaster", "shll103a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "shll103a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld31b(self):
        filename = osp.join(data_path(), "meshaster", "sdld31b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld31b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz136b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz136b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz136b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl137a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl137a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl137a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll107e(self):
        filename = osp.join(data_path(), "meshaster", "ssll107e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll107e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_comp011c(self):
        filename = osp.join(data_path(), "meshaster", "comp011c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "comp011c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv105a(self):
        filename = osp.join(data_path(), "meshaster", "hsnv105a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv105a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlx400a(self):
        filename = osp.join(data_path(), "meshaster", "sdlx400a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlx400a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_erreu10a(self):
        filename = osp.join(data_path(), "meshaster", "erreu10a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "erreu10a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv122a(self):
        filename = osp.join(data_path(), "meshaster", "hsnv122a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv122a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz127b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz127b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz127b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll128a(self):
        filename = osp.join(data_path(), "meshaster", "sdll128a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll128a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll108a(self):
        filename = osp.join(data_path(), "meshaster", "ssll108a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll108a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz366b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz366b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz366b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz326a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz326a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz326a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz336b18(self):
        filename = osp.join(data_path(), "meshaster", "zzzz336b-18.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz336b-18.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp118c(self):
        filename = osp.join(data_path(), "meshaster", "ssnp118c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp118c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz411a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz411a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz411a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz293a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz293a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz293a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv183a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv183a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv183a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslx100c(self):
        filename = osp.join(data_path(), "meshaster", "sslx100c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslx100c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdls112a22(self):
        filename = osp.join(data_path(), "meshaster", "sdls112a-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdls112a-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd112a(self):
        filename = osp.join(data_path(), "meshaster", "ssnd112a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd112a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld321a(self):
        filename = osp.join(data_path(), "meshaster", "sdld321a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld321a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdls124a(self):
        filename = osp.join(data_path(), "meshaster", "sdls124a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdls124a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslx100f(self):
        filename = osp.join(data_path(), "meshaster", "sslx100f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslx100f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslp01a(self):
        filename = osp.join(data_path(), "meshaster", "sslp01a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslp01a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld02b(self):
        filename = osp.join(data_path(), "meshaster", "sdld02b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld02b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_fdlv112h(self):
        filename = osp.join(data_path(), "meshaster", "fdlv112h.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "fdlv112h.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv118c(self):
        filename = osp.join(data_path(), "meshaster", "ssnv118c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv118c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz405a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz405a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz405a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162m(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162m.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162m.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_fdlv107a20(self):
        filename = osp.join(data_path(), "meshaster", "fdlv107a-20.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "fdlv107a-20.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv173c(self):
        filename = osp.join(data_path(), "meshaster", "ssnv173c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv173c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl112a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl112a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl112a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz122a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz122a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz122a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv163b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv163b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv163b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld27a(self):
        filename = osp.join(data_path(), "meshaster", "sdld27a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld27a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd119a(self):
        filename = osp.join(data_path(), "meshaster", "ssnd119a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd119a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl117b(self):
        filename = osp.join(data_path(), "meshaster", "ssnl117b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl117b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz367a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz367a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz367a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv142f22(self):
        filename = osp.join(data_path(), "meshaster", "ssnv142f-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv142f-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp14f(self):
        filename = osp.join(data_path(), "meshaster", "ssnp14f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp14f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv101a(self):
        filename = osp.join(data_path(), "meshaster", "hsnv101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll117a(self):
        filename = osp.join(data_path(), "meshaster", "ssll117a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll117a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz274e(self):
        filename = osp.join(data_path(), "meshaster", "zzzz274e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz274e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv157b(self):
        filename = osp.join(data_path(), "meshaster", "sslv157b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv157b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv247b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv247b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv247b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz109a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz109a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz109a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz332a17(self):
        filename = osp.join(data_path(), "meshaster", "zzzz332a-17.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz332a-17.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll129a(self):
        filename = osp.join(data_path(), "meshaster", "sdll129a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll129a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_forma11a(self):
        filename = osp.join(data_path(), "meshaster", "forma11a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "forma11a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll02b(self):
        filename = osp.join(data_path(), "meshaster", "sdll02b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll02b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp118d(self):
        filename = osp.join(data_path(), "meshaster", "ssnp118d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp118d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv126a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv126a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv126a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_fdlv112i(self):
        filename = osp.join(data_path(), "meshaster", "fdlv112i.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "fdlv112i.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlx201a(self):
        filename = osp.join(data_path(), "meshaster", "sdlx201a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlx201a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl122a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl122a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl122a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld107a(self):
        filename = osp.join(data_path(), "meshaster", "sdld107a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld107a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz106a14(self):
        filename = osp.join(data_path(), "meshaster", "zzzz106a-14.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz106a-14.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz162b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz162b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz162b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll400a(self):
        filename = osp.join(data_path(), "meshaster", "ssll400a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll400a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll106e(self):
        filename = osp.join(data_path(), "meshaster", "ssll106e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll106e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld27c(self):
        filename = osp.join(data_path(), "meshaster", "sdld27c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld27c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll11g(self):
        filename = osp.join(data_path(), "meshaster", "ssll11g.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll11g.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_erreu01a(self):
        filename = osp.join(data_path(), "meshaster", "erreu01a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "erreu01a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_szlz105b(self):
        filename = osp.join(data_path(), "meshaster", "szlz105b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "szlz105b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll106a(self):
        filename = osp.join(data_path(), "meshaster", "sdll106a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll106a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz222a21(self):
        filename = osp.join(data_path(), "meshaster", "zzzz222a-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz222a-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll117c(self):
        filename = osp.join(data_path(), "meshaster", "ssll117c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll117c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl502c(self):
        filename = osp.join(data_path(), "meshaster", "ssnl502c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl502c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp15d(self):
        filename = osp.join(data_path(), "meshaster", "ssnp15d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp15d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz250a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz250a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz250a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld313a(self):
        filename = osp.join(data_path(), "meshaster", "sdld313a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld313a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv115a(self):
        filename = osp.join(data_path(), "meshaster", "sslv115a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv115a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz111b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz111b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz111b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsns101b(self):
        filename = osp.join(data_path(), "meshaster", "hsns101b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsns101b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld02a(self):
        filename = osp.join(data_path(), "meshaster", "sdld02a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld02a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll150a(self):
        filename = osp.join(data_path(), "meshaster", "sdll150a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll150a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_wtnp116c(self):
        filename = osp.join(data_path(), "meshaster", "wtnp116c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "wtnp116c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz285e20(self):
        filename = osp.join(data_path(), "meshaster", "zzzz285e-20.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz285e-20.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd120a(self):
        filename = osp.join(data_path(), "meshaster", "ssnd120a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd120a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp150b(self):
        filename = osp.join(data_path(), "meshaster", "ssnp150b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp150b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz223a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz223a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz223a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl139a21(self):
        filename = osp.join(data_path(), "meshaster", "sdnl139a-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl139a-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd105c(self):
        filename = osp.join(data_path(), "meshaster", "ssnd105c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd105c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll111b18(self):
        filename = osp.join(data_path(), "meshaster", "ssll111b-18.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll111b-18.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll152a(self):
        filename = osp.join(data_path(), "meshaster", "sdll152a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll152a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz274a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz274a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz274a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssns112b(self):
        filename = osp.join(data_path(), "meshaster", "ssns112b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssns112b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnx100b(self):
        filename = osp.join(data_path(), "meshaster", "sdnx100b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnx100b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssls141f(self):
        filename = osp.join(data_path(), "meshaster", "ssls141f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssls141f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz121c(self):
        filename = osp.join(data_path(), "meshaster", "zzzz121c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz121c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz366c(self):
        filename = osp.join(data_path(), "meshaster", "zzzz366c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz366c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz413d20(self):
        filename = osp.join(data_path(), "meshaster", "zzzz413d-20.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz413d-20.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tplp303f(self):
        filename = osp.join(data_path(), "meshaster", "tplp303f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tplp303f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp144f(self):
        filename = osp.join(data_path(), "meshaster", "ssnp144f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp144f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssls141e(self):
        filename = osp.join(data_path(), "meshaster", "ssls141e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssls141e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld106a(self):
        filename = osp.join(data_path(), "meshaster", "sdld106a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld106a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl105a(self):
        filename = osp.join(data_path(), "meshaster", "sdnl105a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl105a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv140f(self):
        filename = osp.join(data_path(), "meshaster", "hsnv140f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv140f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv169e(self):
        filename = osp.join(data_path(), "meshaster", "ssnv169e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv169e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz326b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz326b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz326b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd123a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd123a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd123a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd116a(self):
        filename = osp.join(data_path(), "meshaster", "ssnd116a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd116a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz297c(self):
        filename = osp.join(data_path(), "meshaster", "zzzz297c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz297c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl139a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl139a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl139a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll101a(self):
        filename = osp.join(data_path(), "meshaster", "sdll101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz394a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz394a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz394a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlx302a(self):
        filename = osp.join(data_path(), "meshaster", "sdlx302a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlx302a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp129a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp129a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp129a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl106e(self):
        filename = osp.join(data_path(), "meshaster", "ssnl106e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl106e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl504c21(self):
        filename = osp.join(data_path(), "meshaster", "ssnl504c-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl504c-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp02b(self):
        filename = osp.join(data_path(), "meshaster", "ssnp02b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp02b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld02d(self):
        filename = osp.join(data_path(), "meshaster", "sdld02d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld02d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv140a(self):
        filename = osp.join(data_path(), "meshaster", "sslv140a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv140a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssna116a(self):
        filename = osp.join(data_path(), "meshaster", "ssna116a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssna116a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162p(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162p.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162p.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv07a19(self):
        filename = osp.join(data_path(), "meshaster", "sslv07a-19.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv07a-19.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz296a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz296a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz296a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz106b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz106b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz106b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv114a22(self):
        filename = osp.join(data_path(), "meshaster", "sslv114a-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv114a-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tplp303e(self):
        filename = osp.join(data_path(), "meshaster", "tplp303e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tplp303e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_wtna110a(self):
        filename = osp.join(data_path(), "meshaster", "wtna110a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "wtna110a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv510a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv510a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv510a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd105b(self):
        filename = osp.join(data_path(), "meshaster", "ssnd105b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd105b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz318a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz318a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz318a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp118a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp118a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp118a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162n(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162n.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162n.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld02c(self):
        filename = osp.join(data_path(), "meshaster", "sdld02c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld02c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll401a(self):
        filename = osp.join(data_path(), "meshaster", "sdll401a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll401a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz101a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tpls302c(self):
        filename = osp.join(data_path(), "meshaster", "tpls302c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tpls302c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd106b(self):
        filename = osp.join(data_path(), "meshaster", "ssnd106b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd106b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz322a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz322a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz322a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv172b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv172b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv172b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl106g18(self):
        filename = osp.join(data_path(), "meshaster", "ssnl106g-18.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl106g-18.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp14b(self):
        filename = osp.join(data_path(), "meshaster", "ssnp14b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp14b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv157a(self):
        filename = osp.join(data_path(), "meshaster", "sslv157a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv157a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_shll101c(self):
        filename = osp.join(data_path(), "meshaster", "shll101c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "shll101c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld110b(self):
        filename = osp.join(data_path(), "meshaster", "sdld110b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld110b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz407a20(self):
        filename = osp.join(data_path(), "meshaster", "zzzz407a-20.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz407a-20.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd100a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd100a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd100a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv172a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv172a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv172a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz318d19(self):
        filename = osp.join(data_path(), "meshaster", "zzzz318d-19.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz318d-19.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv115b(self):
        filename = osp.join(data_path(), "meshaster", "sslv115b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv115b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl112f(self):
        filename = osp.join(data_path(), "meshaster", "ssnl112f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl112f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv01b(self):
        filename = osp.join(data_path(), "meshaster", "sslv01b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv01b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll104a(self):
        filename = osp.join(data_path(), "meshaster", "sdll104a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll104a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll137a24(self):
        filename = osp.join(data_path(), "meshaster", "sdll137a-24.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll137a-24.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz336a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz336a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz336a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv07a23(self):
        filename = osp.join(data_path(), "meshaster", "sslv07a-23.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv07a-23.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tpna300a(self):
        filename = osp.join(data_path(), "meshaster", "tpna300a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tpna300a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tplp303d(self):
        filename = osp.join(data_path(), "meshaster", "tplp303d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tplp303d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz306a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz306a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz306a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd105a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd105a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd105a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv230a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv230a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv230a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz382a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz382a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz382a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp02a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp02a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp02a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv126b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv126b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv126b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll311a(self):
        filename = osp.join(data_path(), "meshaster", "sdll311a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll311a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd106a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd106a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd106a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz285e22(self):
        filename = osp.join(data_path(), "meshaster", "zzzz285e-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz285e-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll118b(self):
        filename = osp.join(data_path(), "meshaster", "ssll118b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll118b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll107g38(self):
        filename = osp.join(data_path(), "meshaster", "ssll107g-38.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll107g-38.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld101a(self):
        filename = osp.join(data_path(), "meshaster", "sdld101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll123a(self):
        filename = osp.join(data_path(), "meshaster", "sdll123a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll123a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz306f(self):
        filename = osp.join(data_path(), "meshaster", "zzzz306f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz306f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld103a(self):
        filename = osp.join(data_path(), "meshaster", "sdld103a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld103a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_comp010j(self):
        filename = osp.join(data_path(), "meshaster", "comp010j.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "comp010j.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll102c(self):
        filename = osp.join(data_path(), "meshaster", "ssll102c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll102c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz304a21(self):
        filename = osp.join(data_path(), "meshaster", "zzzz304a-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz304a-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv121c(self):
        filename = osp.join(data_path(), "meshaster", "hsnv121c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv121c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_shll100a22(self):
        filename = osp.join(data_path(), "meshaster", "shll100a-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "shll100a-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld25a(self):
        filename = osp.join(data_path(), "meshaster", "sdld25a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld25a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdls119b(self):
        filename = osp.join(data_path(), "meshaster", "sdls119b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdls119b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd102a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd102a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd102a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tplp303b(self):
        filename = osp.join(data_path(), "meshaster", "tplp303b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tplp303b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl201d(self):
        filename = osp.join(data_path(), "meshaster", "ssnl201d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl201d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll107g39(self):
        filename = osp.join(data_path(), "meshaster", "ssll107g-39.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll107g-39.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp14e(self):
        filename = osp.join(data_path(), "meshaster", "ssnp14e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp14e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv190b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv190b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv190b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp118m(self):
        filename = osp.join(data_path(), "meshaster", "ssnp118m.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp118m.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tpll100a(self):
        filename = osp.join(data_path(), "meshaster", "tpll100a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tpll100a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll147a(self):
        filename = osp.join(data_path(), "meshaster", "sdll147a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll147a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tpna01e(self):
        filename = osp.join(data_path(), "meshaster", "tpna01e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tpna01e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv143a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv143a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv143a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll152b(self):
        filename = osp.join(data_path(), "meshaster", "sdll152b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll152b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl32a(self):
        filename = osp.join(data_path(), "meshaster", "sdnl32a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl32a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl111b(self):
        filename = osp.join(data_path(), "meshaster", "ssnl111b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl111b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll113c(self):
        filename = osp.join(data_path(), "meshaster", "sdll113c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll113c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz129a21(self):
        filename = osp.join(data_path(), "meshaster", "zzzz129a-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz129a-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ttlp100a(self):
        filename = osp.join(data_path(), "meshaster", "ttlp100a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ttlp100a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_comp001a(self):
        filename = osp.join(data_path(), "meshaster", "comp001a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "comp001a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_wtnv114a(self):
        filename = osp.join(data_path(), "meshaster", "wtnv114a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "wtnv114a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssls100i(self):
        filename = osp.join(data_path(), "meshaster", "ssls100i.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssls100i.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_erreu09a(self):
        filename = osp.join(data_path(), "meshaster", "erreu09a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "erreu09a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv138b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv138b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv138b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_wtnv136c(self):
        filename = osp.join(data_path(), "meshaster", "wtnv136c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "wtnv136c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll144a(self):
        filename = osp.join(data_path(), "meshaster", "sdll144a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll144a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssna117a(self):
        filename = osp.join(data_path(), "meshaster", "ssna117a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssna117a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl104a(self):
        filename = osp.join(data_path(), "meshaster", "sdnl104a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl104a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tplv100b(self):
        filename = osp.join(data_path(), "meshaster", "tplv100b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tplv100b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv100g(self):
        filename = osp.join(data_path(), "meshaster", "hsnv100g.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv100g.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp15h(self):
        filename = osp.join(data_path(), "meshaster", "ssnp15h.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp15h.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld103b(self):
        filename = osp.join(data_path(), "meshaster", "sdld103b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld103b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv160a(self):
        filename = osp.join(data_path(), "meshaster", "sslv160a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv160a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl105a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl105a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl105a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll114a(self):
        filename = osp.join(data_path(), "meshaster", "sdll114a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll114a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv160c(self):
        filename = osp.join(data_path(), "meshaster", "ssnv160c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv160c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz124a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz124a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz124a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl139a19(self):
        filename = osp.join(data_path(), "meshaster", "sdnl139a-19.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl139a-19.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_comp009a(self):
        filename = osp.join(data_path(), "meshaster", "comp009a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "comp009a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv223a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv223a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv223a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv109a(self):
        filename = osp.join(data_path(), "meshaster", "sslv109a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv109a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp101a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll12a(self):
        filename = osp.join(data_path(), "meshaster", "ssll12a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll12a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd125a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd125a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd125a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz266a23(self):
        filename = osp.join(data_path(), "meshaster", "zzzz266a-23.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz266a-23.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl141a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl141a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl141a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz413d21(self):
        filename = osp.join(data_path(), "meshaster", "zzzz413d-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz413d-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz240a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz240a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz240a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd100c(self):
        filename = osp.join(data_path(), "meshaster", "sdnd100c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd100c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162j(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162j.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162j.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd102a(self):
        filename = osp.join(data_path(), "meshaster", "ssnd102a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd102a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz133b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz133b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz133b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd107b(self):
        filename = osp.join(data_path(), "meshaster", "sdnd107b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd107b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl115a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl115a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl115a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv167a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv167a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv167a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162i(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162i.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162i.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd101a(self):
        filename = osp.join(data_path(), "meshaster", "ssnd101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll103b(self):
        filename = osp.join(data_path(), "meshaster", "ssll103b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll103b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl100a(self):
        filename = osp.join(data_path(), "meshaster", "sdnl100a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl100a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp14d(self):
        filename = osp.join(data_path(), "meshaster", "ssnp14d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp14d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlv132a23(self):
        filename = osp.join(data_path(), "meshaster", "sdlv132a-23.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlv132a-23.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd102c(self):
        filename = osp.join(data_path(), "meshaster", "sdnd102c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd102c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz342c(self):
        filename = osp.join(data_path(), "meshaster", "zzzz342c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz342c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_efica01a(self):
        filename = osp.join(data_path(), "meshaster", "efica01a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "efica01a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld313c(self):
        filename = osp.join(data_path(), "meshaster", "sdld313c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld313c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd120a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd120a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd120a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp303a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp303a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp303a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv115c(self):
        filename = osp.join(data_path(), "meshaster", "sslv115c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv115c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl128a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl128a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl128a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162l(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162l.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162l.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz318e19(self):
        filename = osp.join(data_path(), "meshaster", "zzzz318e-19.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz318e-19.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd117a(self):
        filename = osp.join(data_path(), "meshaster", "ssnd117a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd117a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll124a(self):
        filename = osp.join(data_path(), "meshaster", "sdll124a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll124a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld31a(self):
        filename = osp.join(data_path(), "meshaster", "sdld31a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld31a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp164f(self):
        filename = osp.join(data_path(), "meshaster", "ssnp164f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp164f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv121d(self):
        filename = osp.join(data_path(), "meshaster", "hsnv121d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv121d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv113a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv113a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv113a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld33a(self):
        filename = osp.join(data_path(), "meshaster", "sdld33a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld33a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd109a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd109a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd109a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll11b(self):
        filename = osp.join(data_path(), "meshaster", "ssll11b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll11b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv114b(self):
        filename = osp.join(data_path(), "meshaster", "sslv114b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv114b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv100a(self):
        filename = osp.join(data_path(), "meshaster", "hsnv100a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv100a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl143a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl143a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl143a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hplv101b(self):
        filename = osp.join(data_path(), "meshaster", "hplv101b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hplv101b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll101b(self):
        filename = osp.join(data_path(), "meshaster", "sdll101b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll101b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslp200b(self):
        filename = osp.join(data_path(), "meshaster", "sslp200b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslp200b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll118a(self):
        filename = osp.join(data_path(), "meshaster", "ssll118a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll118a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll403a(self):
        filename = osp.join(data_path(), "meshaster", "ssll403a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll403a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tpll101a(self):
        filename = osp.join(data_path(), "meshaster", "tpll101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tpll101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tpls302a(self):
        filename = osp.join(data_path(), "meshaster", "tpls302a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tpls302a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv105b(self):
        filename = osp.join(data_path(), "meshaster", "sslv105b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv105b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll107c(self):
        filename = osp.join(data_path(), "meshaster", "ssll107c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll107c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv176a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv176a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv176a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl131a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl131a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl131a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz341a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz341a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz341a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl501e(self):
        filename = osp.join(data_path(), "meshaster", "ssnl501e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl501e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_comp005b(self):
        filename = osp.join(data_path(), "meshaster", "comp005b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "comp005b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl127e(self):
        filename = osp.join(data_path(), "meshaster", "ssnl127e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl127e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsns102a(self):
        filename = osp.join(data_path(), "meshaster", "hsns102a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsns102a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz306c(self):
        filename = osp.join(data_path(), "meshaster", "zzzz306c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz306c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll102a(self):
        filename = osp.join(data_path(), "meshaster", "ssll102a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll102a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl105b(self):
        filename = osp.join(data_path(), "meshaster", "sdnl105b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl105b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl100a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl100a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl100a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd103a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd103a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd103a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsns101a(self):
        filename = osp.join(data_path(), "meshaster", "hsns101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsns101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv244b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv244b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv244b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv133a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv133a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv133a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz297f(self):
        filename = osp.join(data_path(), "meshaster", "zzzz297f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz297f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz297d(self):
        filename = osp.join(data_path(), "meshaster", "zzzz297d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz297d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz413d22(self):
        filename = osp.join(data_path(), "meshaster", "zzzz413d-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz413d-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz381a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz381a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz381a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv100f(self):
        filename = osp.join(data_path(), "meshaster", "hsnv100f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv100f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd102a21(self):
        filename = osp.join(data_path(), "meshaster", "sdnd102a-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd102a-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll302a(self):
        filename = osp.join(data_path(), "meshaster", "sdll302a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll302a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv124b(self):
        filename = osp.join(data_path(), "meshaster", "hsnv124b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv124b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll126a(self):
        filename = osp.join(data_path(), "meshaster", "sdll126a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll126a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv120a(self):
        filename = osp.join(data_path(), "meshaster", "hsnv120a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv120a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlx105b(self):
        filename = osp.join(data_path(), "meshaster", "sdlx105b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlx105b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz131a50(self):
        filename = osp.join(data_path(), "meshaster", "zzzz131a-50.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz131a-50.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv173e(self):
        filename = osp.join(data_path(), "meshaster", "ssnv173e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv173e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv208a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv208a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv208a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd102b(self):
        filename = osp.join(data_path(), "meshaster", "sdnd102b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd102b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll113a(self):
        filename = osp.join(data_path(), "meshaster", "sdll113a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll113a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl139a22(self):
        filename = osp.join(data_path(), "meshaster", "sdnl139a-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl139a-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_mfron01h(self):
        filename = osp.join(data_path(), "meshaster", "mfron01h.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "mfron01h.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld23a(self):
        filename = osp.join(data_path(), "meshaster", "sdld23a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld23a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp15e(self):
        filename = osp.join(data_path(), "meshaster", "ssnp15e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp15e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz164b21(self):
        filename = osp.join(data_path(), "meshaster", "zzzz164b-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz164b-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl111a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl111a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl111a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp118e(self):
        filename = osp.join(data_path(), "meshaster", "ssnp118e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp118e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz297e(self):
        filename = osp.join(data_path(), "meshaster", "zzzz297e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz297e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv129a(self):
        filename = osp.join(data_path(), "meshaster", "hsnv129a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv129a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz124b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz124b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz124b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_forma30a(self):
        filename = osp.join(data_path(), "meshaster", "forma30a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "forma30a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd100b(self):
        filename = osp.join(data_path(), "meshaster", "sdnd100b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd100b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsns101d(self):
        filename = osp.join(data_path(), "meshaster", "hsns101d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsns101d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv105b22(self):
        filename = osp.join(data_path(), "meshaster", "sslv105b-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv105b-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld102b(self):
        filename = osp.join(data_path(), "meshaster", "sdld102b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld102b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_erreu14a(self):
        filename = osp.join(data_path(), "meshaster", "erreu14a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "erreu14a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv131a(self):
        filename = osp.join(data_path(), "meshaster", "sslv131a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv131a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv142f(self):
        filename = osp.join(data_path(), "meshaster", "ssnv142f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv142f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll137a26(self):
        filename = osp.join(data_path(), "meshaster", "sdll137a-26.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll137a-26.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlv132c21(self):
        filename = osp.join(data_path(), "meshaster", "sdlv132c-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlv132c-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd107a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd107a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd107a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz126a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz126a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz126a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlv121d(self):
        filename = osp.join(data_path(), "meshaster", "sdlv121d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlv121d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv229a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv229a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv229a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv121b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv121b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv121b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll104a(self):
        filename = osp.join(data_path(), "meshaster", "ssll104a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll104a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl139a19(self):
        filename = osp.join(data_path(), "meshaster", "ssnl139a-19.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl139a-19.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv400a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv400a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv400a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz318f19(self):
        filename = osp.join(data_path(), "meshaster", "zzzz318f-19.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz318f-19.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162g(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162g.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162g.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz294d(self):
        filename = osp.join(data_path(), "meshaster", "zzzz294d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz294d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv118b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv118b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv118b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv159a(self):
        filename = osp.join(data_path(), "meshaster", "sslv159a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv159a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv146a(self):
        filename = osp.join(data_path(), "meshaster", "sslv146a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv146a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl106a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl106a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl106a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll106f(self):
        filename = osp.join(data_path(), "meshaster", "ssll106f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll106f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv124b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv124b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv124b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162c(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv159b(self):
        filename = osp.join(data_path(), "meshaster", "sslv159b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv159b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz234e22(self):
        filename = osp.join(data_path(), "meshaster", "zzzz234e-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz234e-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv124a(self):
        filename = osp.join(data_path(), "meshaster", "hsnv124a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv124a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz304a20(self):
        filename = osp.join(data_path(), "meshaster", "zzzz304a-20.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz304a-20.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssla103b(self):
        filename = osp.join(data_path(), "meshaster", "ssla103b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssla103b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz268b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz268b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz268b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz323e(self):
        filename = osp.join(data_path(), "meshaster", "zzzz323e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz323e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld325a(self):
        filename = osp.join(data_path(), "meshaster", "sdld325a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld325a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz366d(self):
        filename = osp.join(data_path(), "meshaster", "zzzz366d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz366d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv195d(self):
        filename = osp.join(data_path(), "meshaster", "ssnv195d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv195d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlv132a22(self):
        filename = osp.join(data_path(), "meshaster", "sdlv132a-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlv132a-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz106a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz106a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz106a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp14g(self):
        filename = osp.join(data_path(), "meshaster", "ssnp14g.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp14g.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz266a22(self):
        filename = osp.join(data_path(), "meshaster", "zzzz266a-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz266a-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_erreu13a(self):
        filename = osp.join(data_path(), "meshaster", "erreu13a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "erreu13a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslx102e(self):
        filename = osp.join(data_path(), "meshaster", "sslx102e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslx102e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd121a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd121a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd121a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssna114a(self):
        filename = osp.join(data_path(), "meshaster", "ssna114a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssna114a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdls100c(self):
        filename = osp.join(data_path(), "meshaster", "sdls100c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdls100c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp126a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp126a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp126a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl102a(self):
        filename = osp.join(data_path(), "meshaster", "sdnl102a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl102a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz118d(self):
        filename = osp.join(data_path(), "meshaster", "zzzz118d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz118d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp113a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp113a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp113a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv102c(self):
        filename = osp.join(data_path(), "meshaster", "ssnv102c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv102c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld400b(self):
        filename = osp.join(data_path(), "meshaster", "sdld400b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld400b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tplp107b(self):
        filename = osp.join(data_path(), "meshaster", "tplp107b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tplp107b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssla200a(self):
        filename = osp.join(data_path(), "meshaster", "ssla200a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssla200a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz191a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz191a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz191a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz407a21(self):
        filename = osp.join(data_path(), "meshaster", "zzzz407a-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz407a-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz111c(self):
        filename = osp.join(data_path(), "meshaster", "zzzz111c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz111c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp160a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp160a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp160a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsna106a(self):
        filename = osp.join(data_path(), "meshaster", "hsna106a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsna106a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162h(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162h.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162h.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_fdlv102c21(self):
        filename = osp.join(data_path(), "meshaster", "fdlv102c-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "fdlv102c-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssna109a(self):
        filename = osp.join(data_path(), "meshaster", "ssna109a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssna109a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz219a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz219a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz219a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv122a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv122a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv122a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlv402a21(self):
        filename = osp.join(data_path(), "meshaster", "sdlv402a-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlv402a-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tpll01a(self):
        filename = osp.join(data_path(), "meshaster", "tpll01a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tpll01a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl504c(self):
        filename = osp.join(data_path(), "meshaster", "ssnl504c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl504c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp306a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp306a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp306a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz111d(self):
        filename = osp.join(data_path(), "meshaster", "zzzz111d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz111d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd101a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv101a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz234a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz234a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz234a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz342a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz342a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz342a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll404a(self):
        filename = osp.join(data_path(), "meshaster", "ssll404a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll404a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tplp303a(self):
        filename = osp.join(data_path(), "meshaster", "tplp303a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tplp303a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsll100a(self):
        filename = osp.join(data_path(), "meshaster", "hsll100a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsll100a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv142b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv142b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv142b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp160b(self):
        filename = osp.join(data_path(), "meshaster", "ssnp160b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp160b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz318a19(self):
        filename = osp.join(data_path(), "meshaster", "zzzz318a-19.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz318a-19.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp305a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp305a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp305a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd105a(self):
        filename = osp.join(data_path(), "meshaster", "ssnd105a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd105a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_erreu02a(self):
        filename = osp.join(data_path(), "meshaster", "erreu02a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "erreu02a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssls141c(self):
        filename = osp.join(data_path(), "meshaster", "ssls141c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssls141c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll141c(self):
        filename = osp.join(data_path(), "meshaster", "sdll141c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll141c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_shll101e(self):
        filename = osp.join(data_path(), "meshaster", "shll101e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "shll101e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_wtnv126b(self):
        filename = osp.join(data_path(), "meshaster", "wtnv126b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "wtnv126b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld27e(self):
        filename = osp.join(data_path(), "meshaster", "sdld27e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld27e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll125c(self):
        filename = osp.join(data_path(), "meshaster", "sdll125c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll125c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_supv001f(self):
        filename = osp.join(data_path(), "meshaster", "supv001f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "supv001f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz297a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz297a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz297a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz352a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz352a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz352a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_wtnv114h(self):
        filename = osp.join(data_path(), "meshaster", "wtnv114h.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "wtnv114h.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl121c(self):
        filename = osp.join(data_path(), "meshaster", "ssnl121c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl121c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll11a(self):
        filename = osp.join(data_path(), "meshaster", "ssll11a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll11a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll119b(self):
        filename = osp.join(data_path(), "meshaster", "ssll119b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll119b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld104b(self):
        filename = osp.join(data_path(), "meshaster", "sdld104b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld104b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_szlz105a(self):
        filename = osp.join(data_path(), "meshaster", "szlz105a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "szlz105a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tplv305a(self):
        filename = osp.join(data_path(), "meshaster", "tplv305a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tplv305a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp15b(self):
        filename = osp.join(data_path(), "meshaster", "ssnp15b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp15b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv101c(self):
        filename = osp.join(data_path(), "meshaster", "hsnv101c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv101c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv191b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv191b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv191b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162d(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssls141a(self):
        filename = osp.join(data_path(), "meshaster", "ssls141a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssls141a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll107d38(self):
        filename = osp.join(data_path(), "meshaster", "ssll107d-38.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll107d-38.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz360a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz360a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz360a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz289c(self):
        filename = osp.join(data_path(), "meshaster", "zzzz289c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz289c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll137a(self):
        filename = osp.join(data_path(), "meshaster", "sdll137a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll137a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz256a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz256a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz256a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hplv101a(self):
        filename = osp.join(data_path(), "meshaster", "hplv101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hplv101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv100c(self):
        filename = osp.join(data_path(), "meshaster", "hsnv100c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv100c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsns101c(self):
        filename = osp.join(data_path(), "meshaster", "hsns101c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsns101c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld110a(self):
        filename = osp.join(data_path(), "meshaster", "sdld110a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld110a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv232b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv232b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv232b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld21b(self):
        filename = osp.join(data_path(), "meshaster", "sdld21b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld21b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld21c(self):
        filename = osp.join(data_path(), "meshaster", "sdld21c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld21c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll146a(self):
        filename = osp.join(data_path(), "meshaster", "sdll146a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll146a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl129b(self):
        filename = osp.join(data_path(), "meshaster", "ssnl129b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl129b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd108a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd108a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd108a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp14c(self):
        filename = osp.join(data_path(), "meshaster", "ssnp14c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp14c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl139b(self):
        filename = osp.join(data_path(), "meshaster", "sdnl139b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl139b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll126d(self):
        filename = osp.join(data_path(), "meshaster", "sdll126d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll126d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl127a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl127a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl127a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssls143a(self):
        filename = osp.join(data_path(), "meshaster", "ssls143a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssls143a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_wtna112a(self):
        filename = osp.join(data_path(), "meshaster", "wtna112a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "wtna112a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssns106a(self):
        filename = osp.join(data_path(), "meshaster", "ssns106a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssns106a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz294c(self):
        filename = osp.join(data_path(), "meshaster", "zzzz294c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz294c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz318c19(self):
        filename = osp.join(data_path(), "meshaster", "zzzz318c-19.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz318c-19.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv140b(self):
        filename = osp.join(data_path(), "meshaster", "hsnv140b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv140b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp302a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp302a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp302a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_forma21b21(self):
        filename = osp.join(data_path(), "meshaster", "forma21b-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "forma21b-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl118a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl118a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl118a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz349a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz349a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz349a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld104a(self):
        filename = osp.join(data_path(), "meshaster", "sdld104a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld104a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_wtnv143f(self):
        filename = osp.join(data_path(), "meshaster", "wtnv143f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "wtnv143f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tpll100b(self):
        filename = osp.join(data_path(), "meshaster", "tpll100b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tpll100b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssns105b(self):
        filename = osp.join(data_path(), "meshaster", "ssns105b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssns105b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162b(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld400a(self):
        filename = osp.join(data_path(), "meshaster", "sdld400a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld400a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd106a(self):
        filename = osp.join(data_path(), "meshaster", "ssnd106a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd106a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld22a(self):
        filename = osp.join(data_path(), "meshaster", "sdld22a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld22a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz384a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz384a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz384a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hpla100b(self):
        filename = osp.join(data_path(), "meshaster", "hpla100b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hpla100b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlv132d(self):
        filename = osp.join(data_path(), "meshaster", "sdlv132d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlv132d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld301a(self):
        filename = osp.join(data_path(), "meshaster", "sdld301a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld301a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz323a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz323a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz323a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll141b(self):
        filename = osp.join(data_path(), "meshaster", "sdll141b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll141b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz289a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz289a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz289a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv103a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv103a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv103a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tpla301a(self):
        filename = osp.join(data_path(), "meshaster", "tpla301a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tpla301a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv146b(self):
        filename = osp.join(data_path(), "meshaster", "sslv146b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv146b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll105a(self):
        filename = osp.join(data_path(), "meshaster", "ssll105a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll105a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll123c(self):
        filename = osp.join(data_path(), "meshaster", "sdll123c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll123c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd116b(self):
        filename = osp.join(data_path(), "meshaster", "ssnd116b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd116b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld29a(self):
        filename = osp.join(data_path(), "meshaster", "sdld29a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld29a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdls100b(self):
        filename = osp.join(data_path(), "meshaster", "sdls100b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdls100b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv104a(self):
        filename = osp.join(data_path(), "meshaster", "sslv104a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv104a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssns100a(self):
        filename = osp.join(data_path(), "meshaster", "ssns100a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssns100a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssls505a(self):
        filename = osp.join(data_path(), "meshaster", "ssls505a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssls505a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl105c(self):
        filename = osp.join(data_path(), "meshaster", "sdnl105c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl105c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp15c(self):
        filename = osp.join(data_path(), "meshaster", "ssnp15c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp15c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv114b22(self):
        filename = osp.join(data_path(), "meshaster", "sslv114b-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv114b-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv169d(self):
        filename = osp.join(data_path(), "meshaster", "ssnv169d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv169d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdls140c(self):
        filename = osp.join(data_path(), "meshaster", "sdls140c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdls140c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlv131a22(self):
        filename = osp.join(data_path(), "meshaster", "sdlv131a-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlv131a-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_fdlv103a(self):
        filename = osp.join(data_path(), "meshaster", "fdlv103a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "fdlv103a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll102d(self):
        filename = osp.join(data_path(), "meshaster", "ssll102d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll102d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162k(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162k.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162k.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz289b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz289b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz289b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162q(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162q.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162q.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssls114i(self):
        filename = osp.join(data_path(), "meshaster", "ssls114i.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssls114i.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll10a(self):
        filename = osp.join(data_path(), "meshaster", "ssll10a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll10a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlv128a21(self):
        filename = osp.join(data_path(), "meshaster", "sdlv128a-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlv128a-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld320a(self):
        filename = osp.join(data_path(), "meshaster", "sdld320a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld320a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_wtnv109c(self):
        filename = osp.join(data_path(), "meshaster", "wtnv109c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "wtnv109c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd103a(self):
        filename = osp.join(data_path(), "meshaster", "ssnd103a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd103a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz127a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz127a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz127a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz306d(self):
        filename = osp.join(data_path(), "meshaster", "zzzz306d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz306d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdls124b(self):
        filename = osp.join(data_path(), "meshaster", "sdls124b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdls124b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlv135b(self):
        filename = osp.join(data_path(), "meshaster", "sdlv135b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlv135b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll107f21(self):
        filename = osp.join(data_path(), "meshaster", "ssll107f-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll107f-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv101b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv101b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv101b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz407a22(self):
        filename = osp.join(data_path(), "meshaster", "zzzz407a-22.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz407a-22.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz249a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz249a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz249a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld109a(self):
        filename = osp.join(data_path(), "meshaster", "sdld109a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld109a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_shll101a(self):
        filename = osp.join(data_path(), "meshaster", "shll101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "shll101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv109b(self):
        filename = osp.join(data_path(), "meshaster", "sslv109b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv109b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdls109f(self):
        filename = osp.join(data_path(), "meshaster", "sdls109f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdls109f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv102b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv102b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv102b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll141a(self):
        filename = osp.join(data_path(), "meshaster", "sdll141a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll141a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssls136a(self):
        filename = osp.join(data_path(), "meshaster", "ssls136a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssls136a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv247a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv247a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv247a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd122a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd122a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd122a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_wtnv100a(self):
        filename = osp.join(data_path(), "meshaster", "wtnv100a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "wtnv100a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp144g(self):
        filename = osp.join(data_path(), "meshaster", "ssnp144g.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp144g.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz102a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz102a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz102a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz323d(self):
        filename = osp.join(data_path(), "meshaster", "zzzz323d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz323d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz381a18(self):
        filename = osp.join(data_path(), "meshaster", "zzzz381a-18.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz381a-18.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssns105a(self):
        filename = osp.join(data_path(), "meshaster", "ssns105a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssns105a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll125a(self):
        filename = osp.join(data_path(), "meshaster", "sdll125a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll125a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl133b(self):
        filename = osp.join(data_path(), "meshaster", "sdnl133b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl133b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld34a(self):
        filename = osp.join(data_path(), "meshaster", "sdld34a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld34a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslp113a(self):
        filename = osp.join(data_path(), "meshaster", "sslp113a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslp113a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld102a(self):
        filename = osp.join(data_path(), "meshaster", "sdld102a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld102a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl103a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl103a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl103a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssls100j(self):
        filename = osp.join(data_path(), "meshaster", "ssls100j.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssls100j.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp118b(self):
        filename = osp.join(data_path(), "meshaster", "ssnp118b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp118b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz323c(self):
        filename = osp.join(data_path(), "meshaster", "zzzz323c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz323c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp505a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp505a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp505a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv151a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv151a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv151a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_hsnv124f(self):
        filename = osp.join(data_path(), "meshaster", "hsnv124f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "hsnv124f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll04a(self):
        filename = osp.join(data_path(), "meshaster", "sdll04a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll04a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl101a(self):
        filename = osp.join(data_path(), "meshaster", "sdnl101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv150a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv150a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv150a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld27d(self):
        filename = osp.join(data_path(), "meshaster", "sdld27d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld27d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ttll301a(self):
        filename = osp.join(data_path(), "meshaster", "ttll301a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ttll301a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll23a(self):
        filename = osp.join(data_path(), "meshaster", "sdll23a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll23a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz297b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz297b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz297b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv226a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv226a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv226a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll123d(self):
        filename = osp.join(data_path(), "meshaster", "sdll123d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll123d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll105e(self):
        filename = osp.join(data_path(), "meshaster", "ssll105e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll105e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz234b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz234b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz234b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll15a(self):
        filename = osp.join(data_path(), "meshaster", "sdll15a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll15a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp02c(self):
        filename = osp.join(data_path(), "meshaster", "ssnp02c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp02c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv159c(self):
        filename = osp.join(data_path(), "meshaster", "sslv159c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv159c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll119a(self):
        filename = osp.join(data_path(), "meshaster", "ssll119a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll119a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv109c(self):
        filename = osp.join(data_path(), "meshaster", "sslv109c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv109c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv149a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv149a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv149a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv154b(self):
        filename = osp.join(data_path(), "meshaster", "ssnv154b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv154b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl117a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl117a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl117a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl106g(self):
        filename = osp.join(data_path(), "meshaster", "ssnl106g.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl106g.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll400a(self):
        filename = osp.join(data_path(), "meshaster", "sdll400a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll400a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz222a20(self):
        filename = osp.join(data_path(), "meshaster", "zzzz222a-20.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz222a-20.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssls121a(self):
        filename = osp.join(data_path(), "meshaster", "ssls121a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssls121a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll102f(self):
        filename = osp.join(data_path(), "meshaster", "ssll102f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll102f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz361a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz361a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz361a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl106d(self):
        filename = osp.join(data_path(), "meshaster", "ssnl106d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl106d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlv132c(self):
        filename = osp.join(data_path(), "meshaster", "sdlv132c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlv132c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlv121e(self):
        filename = osp.join(data_path(), "meshaster", "sdlv121e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlv121e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz114a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz114a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz114a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz118c(self):
        filename = osp.join(data_path(), "meshaster", "zzzz118c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz118c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslx100b(self):
        filename = osp.join(data_path(), "meshaster", "sslx100b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslx100b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz295a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz295a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz295a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl104b(self):
        filename = osp.join(data_path(), "meshaster", "sdnl104b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl104b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd100e(self):
        filename = osp.join(data_path(), "meshaster", "sdnd100e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd100e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv160c(self):
        filename = osp.join(data_path(), "meshaster", "sslv160c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv160c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl112e(self):
        filename = osp.join(data_path(), "meshaster", "ssnl112e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl112e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslv114a(self):
        filename = osp.join(data_path(), "meshaster", "sslv114a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslv114a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll102i(self):
        filename = osp.join(data_path(), "meshaster", "ssll102i.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll102i.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll107f(self):
        filename = osp.join(data_path(), "meshaster", "ssll107f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll107f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdlv402a20(self):
        filename = osp.join(data_path(), "meshaster", "sdlv402a-20.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdlv402a-20.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnd101b(self):
        filename = osp.join(data_path(), "meshaster", "ssnd101b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnd101b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll11c(self):
        filename = osp.join(data_path(), "meshaster", "ssll11c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll11c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll110a(self):
        filename = osp.join(data_path(), "meshaster", "ssll110a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll110a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld30a(self):
        filename = osp.join(data_path(), "meshaster", "sdld30a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld30a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz130a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz130a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz130a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz294a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz294a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz294a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld27b(self):
        filename = osp.join(data_path(), "meshaster", "sdld27b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld27b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz366a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz366a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz366a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp162o(self):
        filename = osp.join(data_path(), "meshaster", "ssnp162o.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp162o.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz365a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz365a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz365a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp108a(self):
        filename = osp.join(data_path(), "meshaster", "ssnp108a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp108a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_shll102a(self):
        filename = osp.join(data_path(), "meshaster", "shll102a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "shll102a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll105a(self):
        filename = osp.join(data_path(), "meshaster", "sdll105a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll105a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv173g(self):
        filename = osp.join(data_path(), "meshaster", "ssnv173g.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv173g.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp118g(self):
        filename = osp.join(data_path(), "meshaster", "ssnp118g.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp118g.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz186a21(self):
        filename = osp.join(data_path(), "meshaster", "zzzz186a-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz186a-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz323b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz323b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz323b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz336a19(self):
        filename = osp.join(data_path(), "meshaster", "zzzz336a-19.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz336a-19.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv121a(self):
        filename = osp.join(data_path(), "meshaster", "ssnv121a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv121a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tpll01h(self):
        filename = osp.join(data_path(), "meshaster", "tpll01h.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tpll01h.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll103a(self):
        filename = osp.join(data_path(), "meshaster", "ssll103a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll103a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_wtnv112c(self):
        filename = osp.join(data_path(), "meshaster", "wtnv112c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "wtnv112c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssns108a(self):
        filename = osp.join(data_path(), "meshaster", "ssns108a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssns108a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll02a(self):
        filename = osp.join(data_path(), "meshaster", "sdll02a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll02a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz250a21(self):
        filename = osp.join(data_path(), "meshaster", "zzzz250a-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz250a-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdld102f(self):
        filename = osp.join(data_path(), "meshaster", "sdld102f.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdld102f.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl139a20(self):
        filename = osp.join(data_path(), "meshaster", "sdnl139a-20.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl139a-20.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssls200a(self):
        filename = osp.join(data_path(), "meshaster", "ssls200a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssls200a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll102h(self):
        filename = osp.join(data_path(), "meshaster", "ssll102h.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll102h.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl101a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll107i(self):
        filename = osp.join(data_path(), "meshaster", "ssll107i.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll107i.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz293a21(self):
        filename = osp.join(data_path(), "meshaster", "zzzz293a-21.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz293a-21.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz418a(self):
        filename = osp.join(data_path(), "meshaster", "zzzz418a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz418a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnv173d(self):
        filename = osp.join(data_path(), "meshaster", "ssnv173d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnv173d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssll102b(self):
        filename = osp.join(data_path(), "meshaster", "ssll102b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssll102b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnl102a(self):
        filename = osp.join(data_path(), "meshaster", "ssnl102a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnl102a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sslp107a(self):
        filename = osp.join(data_path(), "meshaster", "sslp107a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sslp107a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tplv100c(self):
        filename = osp.join(data_path(), "meshaster", "tplv100c.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tplv100c.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_erreu07a(self):
        filename = osp.join(data_path(), "meshaster", "erreu07a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "erreu07a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdls112a20(self):
        filename = osp.join(data_path(), "meshaster", "sdls112a-20.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdls112a-20.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tpls302b(self):
        filename = osp.join(data_path(), "meshaster", "tpls302b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tpls302b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz349b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz349b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz349b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz306e(self):
        filename = osp.join(data_path(), "meshaster", "zzzz306e.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz306e.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_zzzz341b(self):
        filename = osp.join(data_path(), "meshaster", "zzzz341b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "zzzz341b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd105b(self):
        filename = osp.join(data_path(), "meshaster", "sdnd105b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd105b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll23b(self):
        filename = osp.join(data_path(), "meshaster", "sdll23b.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll23b.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnl103a(self):
        filename = osp.join(data_path(), "meshaster", "sdnl103a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnl103a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll112a(self):
        filename = osp.join(data_path(), "meshaster", "sdll112a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll112a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdnd124a(self):
        filename = osp.join(data_path(), "meshaster", "sdnd124a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdnd124a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_sdll117a(self):
        filename = osp.join(data_path(), "meshaster", "sdll117a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "sdll117a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_tplv101a(self):
        filename = osp.join(data_path(), "meshaster", "tplv101a.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "tplv101a.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)

    def test_aster_ssnp164d(self):
        filename = osp.join(data_path(), "meshaster", "ssnp164d.mail")
        jsonfile = osp.join(data_path(), "jsonaster", "ssnp164d.json")
        deep_test_conversion(self, filename, Fmt.Aster, Fmt.Salome, jsonfile)


if __name__ == "__main__":
    unittest.main()
