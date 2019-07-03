# -*- coding: utf-8 -*-

import os
import os.path as osp
import unittest


class TestConfig(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')



if __name__ == "__main__":
    unittest.main()
