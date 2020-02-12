# -*- coding: utf-8 -*-

# Copyright 2018 EDF R&D
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
Auxiliary utilities for *medconverter* plugin.
"""

import os
import os.path as osp
import sys
from PyQt5 import Qt as Q
from ..utilities import resources_path, docs_path

def mandatory_suffix():
    """
    Get suffix to be shown for mandatory parameters.

    Returns:
        str: Suffix for label.
    """
    return ' (*)'


def debug_mode():
    """
    Check if application is working in debug mode.

    Returns:
        bool: *True* if we are in debug mode; *False* otherwise.
    """
    try:
        return int(os.getenv('DEBUG', 0)) > 0
    except ValueError:
        pass
    return False


def debug_message(*args):
    """
    Print debug message.

    While this function is mainly dedicated for printing textual
    message, you may pass any printable object(s) as parameter.

    Note: message is only printed if application is running in debug
    mode. See `debug_mode()`.

    Arguments:
        *args: Variable length argument list.
    """
    if debug_mode():
        if args:
            stream = sys.stdout
            stream.write('medconverter_plugin:')
            for arg in args:
                stream.write(' ' + str(arg))
            stream.write('\n')
            stream.flush()

def connect(signal, slot, connection_type=Q.Qt.UniqueConnection):
    """
    Shortcut function for signal / slot connection.

    Arguments:
        signal (pyqtSignal): Signal object.
        slot (function): Slot function.
        connection_type (Optional[Qt.ConnectionType]): Connection type.
            Defaults to *Qt.UniqueConnection*.
    """
    if signal is not None and slot is not None:
        signal.connect(slot, connection_type)


def disconnect(signal, slot=None):
    """
    Shortcut function for signal / slot disconnection.

    If *slot* is *None*, removes all connections from *signal*.

    Arguments:
        signal (pyqtSignal): Signal object.
        slot (Optional[function]): Slot function. Defaults to *None*.
    """
    if signal is not None:
        try:
            signal.disconnect(slot) if slot else signal.disconnect()
        except TypeError: # prevent exception when there's no connection
            pass


def get_dir_name(parent, title, url):
    """
    Show standard file dialog, to select a directory.

    Arguments:
        parent (QWidget): Parent widget.
        title (str): Dialog's title.
        url (str): Initial file path.

    Returns:
        str: Selected directory or *None* if operation is cancelled.
    """
    dlg = Q.QFileDialog(parent)

    dlg.setWindowTitle(title)

    urls = []
    urls.append(Q.QDir.homePath())
    urls.append(osp.dirname(Q.QApplication.arguments()[0]))
    dlg.setSidebarUrls([Q.QUrl.fromLocalFile(i) for i in urls])

    accept_mode = Q.QFileDialog.AcceptOpen
    dlg.setAcceptMode(accept_mode)

    file_mode = Q.QFileDialog.Directory
    dlg.setFileMode(file_mode)

    # Uncomment below to disable using the system dialog
    # That would make ExistingFile mode effective
    # dlg.setOption(Q.QFileDialog.DontUseNativeDialog)

    dlg.selectFile(url)

    return dlg.selectedFiles()[0] if dlg.exec_() else None

def get_file_name(parent, mode, title, url, filters, suffix=None,
                  default_filter=None):
    """
    Show standard file dialog, to select a file to open or save.

    Arguments:
        parent (QWidget): Parent widget.
        mode (int): File mode: 0 for Save; 1 for Open.
        title (str): Dialog's title.
        url (str): Initial file path.
        filters (list[str], str): File patterns by list or
            one pattern by string.
        suffix (Optional[str]): Default extension to be automatically
            appended to the file name. Defaults to *None*.
        default_filter (Optional[str]): File pattern that will be set as
            current file filter. Defaults to *None*: first pattern.

    Returns:
        str: Selected file or *None* if operation is cancelled.
    """
    dlg = Q.QFileDialog(parent)

    dlg.setWindowTitle(title)

    urls = []
    urls.append(Q.QDir.homePath())
    urls.append(osp.dirname(Q.QApplication.arguments()[0]))
    dlg.setSidebarUrls([Q.QUrl.fromLocalFile(i) for i in urls])

    accept_mode = Q.QFileDialog.AcceptOpen if mode \
        else Q.QFileDialog.AcceptSave
    dlg.setAcceptMode(accept_mode)

    file_mode = Q.QFileDialog.ExistingFile if mode else Q.QFileDialog.AnyFile
    dlg.setFileMode(file_mode)

    # Uncomment below to disable using the system dialog
    # That would make ExistingFile mode effective
    # dlg.setOption(Q.QFileDialog.DontUseNativeDialog)

    dlg.setNameFilters(to_list(filters))
    if default_filter is None and filters:
        default_filter = filters[0]
    if default_filter is not None:
        dlg.selectNameFilter(default_filter)

    if suffix:
        dlg.setDefaultSuffix(suffix)

    dlg.selectFile(url)

    return dlg.selectedFiles()[0] if dlg.exec_() else None


def to_list(*args):
    """
    Return input value(s) as a list.

    Each input argument is treated as follows:

    - Tuple or list is converted to list;
    - For dict, its keys are added to result;
    - Simple value is converted to a list with a single item;
    - *None* values are ignored (thrown away).

    Note:
        Treating of complex values from arguments list is not done: i.e.
        tuple of lists will not be converted to single plain list of
        items from all lists enclosed to tuple.

    Arguments:
        *args: Variable length argument list of input values.

    Returns:
        list: List created from input value(s).
    """
    result = []
    for value in args:
        if isinstance(value, (list, tuple, dict)):
            result.extend(value)
        elif value is not None:
            result.append(value)
    return [i for i in result if i is not None]


def publish_meshes(medfile):
    """Import meshes from a med file into SMESH.

    Arguments:
        medfile (str): Path to the med file.

    Returns:
        list[Mesh]: List of SMESH Mesh objects.
    """
    from salome.smesh import smeshBuilder
    smesh = smeshBuilder.New()
    objs, _ = smesh.CreateMeshesFromMED(medfile)
    return objs
