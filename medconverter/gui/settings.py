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
This module implements *medconverter* settings
"""
from collections import OrderedDict

from ..utilities import translate
from ..engine import Fmt


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
        return self._data.get("Output File")

    @output_file.setter
    def output_file(self, output_file):
        self._data["Output File"] = output_file

    @property
    def output_comm(self):
        """
        str: Attribute that holds output comm.
        """
        return self._data.get("Output Comm")

    @output_comm.setter
    def output_comm(self, output_comm):
        self._data["Output Comm"] = output_comm

    @property
    def input_file(self):
        """
        str: Attribute that holds input file.
        """
        return self._data.get("Input File")

    @input_file.setter
    def input_file(self, input_file):
        self._data["Input File"] = input_file

    @property
    def input_format(self):
        """
        str: Attribute that holds input format.
        """
        return self._data.get("Input Format")

    @input_format.setter
    def input_format(self, input_format):
        self._data["Input Format"] = input_format

    @property
    def output_format(self):
        """
        str: Attribute that holds output format.
        """
        return self._data.get("Output Format")

    @output_format.setter
    def output_format(self, output_format):
        self._data["Output Format"] = output_format

    @property
    def skip_types(self):
        """
        str: Attribute that holds the cells types to be skipped.
        Cell type is given in the origin format.
        """
        return self._data.get("Skip Types")

    @skip_types.setter
    def skip_types(self, skip_types):
        assert isinstance(skip_types, (tuple, list))
        self._data["Skip Types"] = skip_types

    def from_defaults(self):
        """
        Reset settings data to default values.

        Arguments:
            settings_file (str): Name of settings file.
        """
        self.input_file = ""
        self.input_format = Fmt.Null
        self.output_file = ""
        self.output_format = Fmt.Salome
        self.output_comm = ""
        self.skip_types = []

    def dump(self, stream):
        """
        Dump parameters.

        Arguments:
            stream (object): Writer.
        """
        stream.write("==========================================\n")
        stream.write("medconverter parameters\n")
        stream.write("==========================================\n")
        title = translate("medconverter", "Input File")
        stream.write("{:<35}: {}\n".format(title, self.input_file))
        title = translate("medconverter", "Input Format")
        stream.write("{:<35}: {}\n".format(title, Fmt.name(self.input_format)))
        title = translate("medconverter", "Output File")
        stream.write("{:<35}: {}\n".format(title, self.output_file))
        title = translate("medconverter", "Output Format")
        stream.write("{:<35}: {}\n".format(title, Fmt.name(self.output_format)))
        title = translate("medconverter", "Output Comm")
        stream.write("{:<35}: {}\n".format(title, self.output_comm))
