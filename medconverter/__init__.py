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
Implementation of *medconverter* plugin.
"""

from importlib.metadata import version

from .engine import Fmt as Fmt
from .engine import convert as convert
from .gui import (
    supported_input_formats as supported_input_formats,
)
from .gui import (
    supported_output_formats as supported_output_formats,
)

__version__ = version("medconverter")
