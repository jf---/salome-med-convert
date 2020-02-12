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

from PyQt5 import Qt as Q

try:
    import salome
    HAS_SALOME = True if salome.hasDesktop() is not None else False
except ImportError:
    HAS_SALOME = False

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


def data_path(private=False):
    """
    Get path to data test folder.

    Returns:
        str: Path to the data test folder.
    """
    data = 'data_private' if private else 'data'
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
