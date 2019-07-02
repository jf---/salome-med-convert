# coding=utf-8

"""Unittests of the convmail package"""

import sys
import os.path as osp
import unittest
from optparse import OptionParser

import convmail

def _build_suite(testlist):
    """Build the suite of testcases of the package"""
    suite = unittest.TestSuite()
    ldr = unittest.defaultTestLoader
    for test in testlist or []:
        suite.addTests(ldr.loadTestsFromName(test))
    if not testlist:
        suite.addTests(ldr.discover(osp.dirname(__file__), pattern='*.py'))
    return suite

def _main(verbose, test=None):
    """Run unittests"""
    verb = 1 + int(verbose or 0)
    unittest.TextTestRunner(verbosity=verb).run(_build_suite(test))


if __name__ == '__main__':
    parser = OptionParser(usage=__doc__)
    parser.add_option('-s', '--short',
        action='store_const', const=0, default=1, dest='runlevel',
        help="run only shortest testcases")
    parser.add_option('-l', '--long',
        action='store_const', const=2, dest='runlevel',
        help="run long testcases")
    parser.add_option('--salome_exists',
        action='store_true', dest='salome_exists',
        help="run testcases that require a running SALOME session")
    parser.add_option('-v', '--verbose', action='store_true',
        help="increase verbosity")
    parser.add_option('-g', '--graph', action='store_true', default=False,
        help="enable graph")
    parser.add_option('-t', '--test', dest='testlist', action='append', metavar='TEST',
        help="run one or more unittests (can be repeated)")

    opts, args = parser.parse_args()
    convmail._unittest_level = opts.runlevel
    convmail._unittest_graph = opts.graph
    convmail._unittest_salome = opts.salome_exists
    _main(opts.verbose, opts.testlist)
