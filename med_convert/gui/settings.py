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
This module implements *MedConvert* settings
"""
from collections import OrderedDict

from ..utilities import translate


class Settings(object):
    """
    Class that stores settings data.
    """

    def __init__(self):
        """
        Create settings with default values.
        """
        self._data = OrderedDict()
        self.from_defaults()

    @property
    def output_file(self):
        """
        str: Attribute that holds output file.
        """
        return self._data.get('Output File')

    @output_file.setter
    def output_file(self, output_file):
        self._data['Output File'] = output_file

    @property
    def input_file(self):
        """
        str: Attribute that holds input file.
        """
        return self._data.get('Input File')

    @input_file.setter
    def input_file(self, input_file):
        self._data['Input File'] = input_file

    def from_defaults(self):
        """
        Reset settings data to default values.

        Arguments:
            settings_file (str): Name of settings file.
        """
        self.input_file = ''
        self.output_file = ''

    def dump(self, stream):
        """
        Dump parameters.

        Arguments:
            stream (object): Writer.
        """
        stream.write('==========================================\n')
        stream.write('MedConvert parameters\n')
        stream.write('==========================================\n')
        title = translate("MedConvert", "Input File")
        stream.write('{:<35}: {}\n'.format(title, self.input_file))
        title = translate("MedConvert", "Output File")
        stream.write('{:<35}: {}\n'.format(title, self.output_file))
