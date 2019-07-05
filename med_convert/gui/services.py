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
The module implement *MedConvert* plugin's services.
"""

import traceback

from ..convert import Fmt, convert as convert_engine
from ..utilities import translate


def convert(input_file, output_file, conversion_type):
    """Safe call to the converter.
    """
    if conversion_type != 0:
        return False, translate("MedConvert", "Unsupported format!")
    format = Fmt.Systus
    try :
        convert_engine(input_file, format, output_file)
        return True, ''

    except Exception as err:
        traceback.print_exc()
        return False, err
