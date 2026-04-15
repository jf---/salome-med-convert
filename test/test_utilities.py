# -*- coding: utf-8 -*-

import os.path as osp
import unittest

from medconverter.utilities import data_path, docs_path, resources_path


class TestUtilities(unittest.TestCase):
    def test_paths(self):
        self.assertTrue(osp.isdir(resources_path()), resources_path())
        self.assertTrue(osp.isdir(docs_path()), docs_path())
        self.assertTrue(data_path().endswith("data"), data_path())
        self.assertTrue(osp.isdir(data_path()), data_path())


if __name__ == "__main__":
    unittest.main()
