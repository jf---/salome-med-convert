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

"""Unittests of the med_convert package"""

import argparse
import os.path as osp
import sys
import unittest


def _build_suite(testlist):
    """Build the suite of testcases of the package"""
    suite = unittest.TestSuite()
    ldr = unittest.defaultTestLoader
    for test in testlist or []:
        suite.addTests(ldr.loadTestsFromName(test))
    if not testlist:
        suite.addTests(ldr.discover(osp.dirname(__file__), pattern="test_*.py"))
    return suite


def main(verbose, test=None):
    """Run unittests"""
    verb = 1 + int(verbose or 0)
    RET = unittest.TextTestRunner(verbosity=verb).run(_build_suite(test))
    sys.exit(not RET.wasSuccessful())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase verbosity"
    )
    parser.add_argument(
        "test", nargs="*", metavar="TEST", help="test(s) to be executed"
    )
    args = parser.parse_args()
    main(args.verbose, args.test)
