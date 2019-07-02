# -*- coding: utf-8 -*-

import os
import os.path as osp

def resources_path():
    """
    Get path to plugin's resources folder.

    Returns:
        str: Path to the resources folder.
    """
    
    install_root = os.getenv('SALOMEMECA_CONVMAIL_ROOT_DIR')

    path = os.path.join(install_root, 'share', 'salome',
                        'resources')
    return path

def docs_path():
    """
    Get path to plugin's documentation folder.

    Returns:
        str: Path to the documentation folder.
    """
    path = None
    
    install_root = os.getenv('SALOMEMECA_CONVMAIL_ROOT_DIR')

    install_path = os.path.join(install_root, 'share', 'doc', 'salome',
                                'gui', 'convmail', 'html')
    if os.path.exists(install_path):
        path = install_path
        
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


