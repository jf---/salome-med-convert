# -*- coding: utf-8 -*-

import os
import os.path as osp

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
    path = osp.abspath(osp.join(install_root, os.pardir, os.pardir,
                                os.pardir, 'share', 'doc', 'salome',
                                'gui', 'convmail', 'html'))
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

    path = osp.join(resources_path(), 'data')
    return path

def references_path():
    """
    Get path to data test folder.

    Returns:
        str: Path to the data test folder.
    """

    path = osp.join(resources_path(), 'references')
    return path

def results_path():
    """
    Get path to the results folder.

    Returns:
        str: Path to the results folder.
    """

    path = os.getenv('SALOMEMECA_CONVMAIL_RESDIR')

    return path
