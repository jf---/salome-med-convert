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
This package defines the *engine* of the *medconverter* plugin.
"""

from .systus import MedConverterSystus
from .abaqus import MedConverterAbaqus
from .ansys import MedConverterAnsys

class Fmt:
    """Enumerator for mesh formats.

    Attributes:
        Systus
        Abaqus
        Salome
    """
    Null = 0x000
    Salome = 0x001
    Aster = 0x002
    Systus = 0x004
    Abaqus = 0x005
    Ansys = 0x006

    @classmethod
    def get(cls, format_name):
        """
        Get format from name.

        Arguments:
            format_name (str): Format name.

        Returns:
            Fmt: Format value.
        """
        try :
            name = 'null' if format_name == "-" else format_name
            return getattr(cls, name.title())
        except AttributeError:
            msg = "Unknown format '%s'"%format_name
            raise AttributeError(msg)

    @staticmethod
    def name(format):
        """
        Convert format to string representation.

        Arguments:
            format (Fmt) : Format value.

        Returns:
            str: Format name.
        """
        return {
            Fmt.Null : "-",
            Fmt.Salome : "Salome",
            Fmt.Aster : "Aster",
            Fmt.Systus : "Systus",
            Fmt.Abaqus : "Abaqus",
            Fmt.Ansys : "Ansys",
        }.get(format, "Unknown")

    @staticmethod
    def extensions(format):
        """
        Get format file extensions.
        
        Arguments:
            format (Fmt) : Format value.
        
        Returns:
            tuple: List of format's extensions
        """
        return {
            Fmt.Salome: ('.med',),
            Fmt.Aster:  ('.mail',),
            Fmt.Systus: ('.ASC', '.asc'),
            Fmt.Abaqus: ('.inp',),
            Fmt.Ansys : ('.MESHDAT', '.dat'),
        }.get(format, "Unknown")
    

def convert(input_file, input_format, output_file, output_format, verbose = False):
    """Main entry point of the converter.

    Arguments:
        input_file (str) : Path to the input file.
        input_format (Fmt): Format of the input file.
        output_file (str): Path to the output file.
        output_format (Fmt): Format of the output file.
        verbose (bool, optional) : Verbosity.

    Returns:
        bool: Status of the conversion: *True* in case of success, *False* otherwise.

    """

    if (input_format == Fmt.Systus and output_format == Fmt.Salome):
        MedConverterSystus.convert_systus_to_med(input_file, output_file, verbose)

    elif (input_format == Fmt.Salome and output_format == Fmt.Systus):
        MedConverterSystus.convert_med_to_systus(input_file, output_file, verbose)

    elif (input_format == Fmt.Abaqus and output_format == Fmt.Salome):
        MedConverterAbaqus.convert_abaqus_to_med(input_file, output_file, verbose)

    elif (input_format == Fmt.Salome and output_format == Fmt.Abaqus):
        MedConverterAbaqus.convert_med_to_abaqus(input_file, output_file, verbose)

    elif (input_format == Fmt.Ansys and output_format == Fmt.Salome):
        MedConverterAnsys.convert_ansys_to_med(input_file, output_file, verbose)

    elif (input_format == Fmt.Salome and output_format == Fmt.Ansys):
        MedConverterAnsys.convert_med_to_ansys(input_file, output_file, verbose)

    else :
        raise ValueError("Unsupported format conversion!")

    return True
