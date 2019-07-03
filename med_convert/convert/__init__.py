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
This package defines the *engine* of the MED converter plugin.
"""

class Fmt:
    """Enumerator for mesh formats.

    Attributes:
        Systus: Import of Systus files.
    """
    Med = 0x001
    Aster = 0x002
    Systus = 0x004

    @staticmethod
    def name(format):
        """
        Convert format to string representation.

        Arguments:
            format (int): Format value (*Fmt*).

        Returns:
            str: String representation of the format.
        """
        return {
            Fmt.Med: "Med",
            Fmt.Aster: "Aster",
            Fmt.Systus: "Systus",
        }.get(format, "Unknown")


def convert(input_file, format, output_file):
    """Main entry point of the converter.

    Arguments:
        input_file (str): Path to the input file.
        format (str): Format of the input file.
        output_file (str): Path to the output file.

    Returns:
        bool: Status of the conversion: *True* in case of success, *False*
        otherwise.
    """
    return True
