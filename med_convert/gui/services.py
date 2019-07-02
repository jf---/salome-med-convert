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

import os
import sys

from glob import glob
import shutil

from PyQt5 import Qt as Q
from med_convert import kernel

#Fonction principale
def convert(input_file, output_file, conversion_type):

    try :
        kernel.convert(input_file, output_file, conversion_type)
        return True, ''

    except Exception as err:
        return False, err
