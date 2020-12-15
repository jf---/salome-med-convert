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

"""
Convenient utilities for the MED CONVERT plugin.
"""

import os
import os.path as osp
import json
import random

from PyQt5 import Qt as Q
from medcoupling import *

try:
    import salome
    HAS_SALOME = True if salome.hasDesktop() is not None else False
except ImportError:
    HAS_SALOME = False

MAX_ELTS_CHECK_GROUPS = 20

def resources_path():
    """
    Get path to plugin's resources folder.

    Returns:
        str: Path to the resources folder.
    """
    if hasattr(resources_path, 'path'):
        return resources_path.path

    install_root = osp.abspath(osp.dirname(osp.dirname(__file__)))
    path = osp.abspath(osp.join(install_root, os.pardir, os.pardir, os.pardir,
                                os.pardir, 'share', 'salome', 'resources'))
    if not osp.isdir(path):
        path = osp.join(install_root, 'resources')

    resources_path.path = path
    return path


def docs_path():
    """
    Get path to plugin's documentation folder.

    Returns:
        str: Path to the documentation folder.
    """
    if hasattr(docs_path, 'path'):
        return docs_path.path

    install_root = osp.abspath(osp.dirname(osp.dirname(__file__)))
    path = osp.abspath(osp.join(install_root, os.pardir, os.pardir, os.pardir,
                                os.pardir, 'share', 'doc', 'salome',
                                'gui', 'medconverter', 'html'))
    if not osp.isdir(path):
        path = osp.join(install_root, 'doc')

    docs_path.path = path
    return path


def data_path():
    """
    Get path to data test folder.

    Returns:
        str: Path to the data test folder.
    """
    data = 'data'
    if hasattr(data_path, data):
        return getattr(data_path, data)

    install_root = osp.abspath(osp.dirname(osp.dirname(__file__)))
    path = osp.abspath(osp.join(install_root, os.pardir, os.pardir, os.pardir,
                                os.pardir, 'share', 'salome', 'resources',
                                'test', data))
    if not osp.isdir(path):
        path = osp.join(install_root, 'test', data)

    data_path.path = path
    return path


def references_path():
    """
    Get path to data test folder.

    Returns:
        str: Path to the data test folder.
    """
    path = osp.join(resources_path(), 'references')
    return path


def translate(context, source_text, disambiguation=None, num=-1):
    """
    Get translation text for source text.

    Arguments:
        context (str): Context name.
        source_text (str): Text being translated.
        disambiguation (Opional[str]): String identifying text role
            within the same context. Defaults to *None*.
        num (Optional[int]): Number used to support plural forms of
            translation. Defaults to -1 (that means no number feature).

    Returns:
        str: Translation text.
    """
    return Q.QApplication.translate(context, source_text, disambiguation, num)

def create_test_json_file(medfilename, jsonfilename):
    """Function to create the json file suitable for the deep test.

    """

    mm = MEDFileUMesh(medfilename)
    testvalues = {}
    testvalues['NODES'] = {}
    testvalues['CELLS'] = {}
    testvalues['GROUPS'] = {}
    testvalues['NB_NODES'] = mm.getNumberOfNodes()
    testvalues['NB_CELLS'] = sum(mm.getNumberOfCellsAtLevel(lev) for lev in mm.getNonEmptyLevels())
    testvalues['NB_GRP_CELLS'] = sum(len(mm.getGroupsOnSpecifiedLev(lev)) for lev in mm.getNonEmptyLevels())
    testvalues['NB_GRP_NODES'] = len(mm.getGroupsOnSpecifiedLev(1))

    tested_nodes = []
    for lev in mm.getNonEmptyLevels():
        testvalues['CELLS'][lev] = {}
        testvalues['GROUPS'][lev] = {}
        mesh_lev = mm[lev]
        types_at_level = mesh_lev.getAllGeoTypesSorted()
        for medcoupling_cell_type in types_at_level :
            cells_by_type = mesh_lev.giveCellsWithType(medcoupling_cell_type).getValues()
            cell = random.choice(cells_by_type)
            cell_nodes_med = mesh_lev.getNodeIdsOfCell(cell)
            cell_type = MEDCouplingUMesh.GetReprOfGeometricType(medcoupling_cell_type).strip('NORM_')
            cell_code = "ID%d_%s"%(cell, cell_type)
            testvalues['CELLS'][lev][cell_code] = cell_nodes_med
            for i in cell_nodes_med:
                tested_nodes.append(i)

        for group in mm.getGroupsOnSpecifiedLev(lev):
            testvalues['GROUPS'][lev][group] = mm.getGroupArr(lev, group).getValues()[:MAX_ELTS_CHECK_GROUPS]

    if len(mm.getGroupsOnSpecifiedLev(1)) > 0 :
        testvalues['GROUPS'][1] = {}
        for group in mm.getGroupsOnSpecifiedLev(1):
            testvalues['GROUPS'][1][group] = mm.getGroupArr(1, group).getValues()[:MAX_ELTS_CHECK_GROUPS]

    for n in set(tested_nodes):
        testvalues['NODES'][n] = mm.getCoords()[n].getValues()

    with open(jsonfilename, 'w') as fobj:
        json.dump(testvalues, fobj, indent=1, sort_keys=True)



def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
