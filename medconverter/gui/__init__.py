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
Implementation of *medconverter* plugin.
"""

import traceback
from ..engine import Fmt, convert as convert_engine


def supported_input_formats():
    return (Fmt.Abaqus, Fmt.Ansys, Fmt.Aster, Fmt.Systus, Fmt.Zset)


def supported_output_formats():
    return (Fmt.Salome, Fmt.Systus, Fmt.Zset, Fmt.Aster)


def convert(*args):
    """Safe call to the converter."""
    try:
        convert_engine(*args)
        return True, ""

    except Exception as err:
        traceback.print_exc()
        return False, err


def startGUIfromSalome(context=None):
    from .gui import start

    start(context=context)
