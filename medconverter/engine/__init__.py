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

from .abaqus import MedConverterAbaqus
from .ansys import MedConverterAnsys
from .aster import MedConverterAster
from .systus import MedConverterSystus
from .tetgen import MedConverterTetgen
from .zset import MedConverterZset


class Fmt:
    """Enumerator for mesh formats.

    Attributes:
        Systus
        Abaqus
        Ansys
        Zset
        Salome
        Tetgen
    """

    Null = 0x000
    Salome = 0x001
    Aster = 0x002
    Systus = 0x004
    Abaqus = 0x005
    Ansys = 0x006
    Zset = 0x007
    Tetgen = 0x008

    @classmethod
    def get(cls, format_name):
        """
        Get format from name.

        Arguments:
            format_name (str): Format name.

        Returns:
            Fmt: Format value.
        """
        try:
            name = "null" if format_name == "-" else format_name
            return getattr(cls, name.title())
        except AttributeError:
            msg = "Unknown format '%s'" % format_name
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
            Fmt.Null: "-",
            Fmt.Salome: "Salome",
            Fmt.Aster: "Aster",
            Fmt.Systus: "Systus",
            Fmt.Abaqus: "Abaqus",
            Fmt.Ansys: "Ansys",
            Fmt.Zset: "Zset",
            Fmt.Tetgen: "Tetgen",
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
            Fmt.Salome: (".med",),
            Fmt.Aster: (".mail",),
            Fmt.Systus: (".ASC",),
            Fmt.Abaqus: (".inp",),
            Fmt.Ansys: (".CDB", ".cdb"),
            Fmt.Zset: (".geof",),
            Fmt.Tetgen: (".mesh",),
        }.get(format, "Unknown")

    @staticmethod
    def all():
        return (Fmt.Salome, Fmt.Aster, Fmt.Systus, Fmt.Abaqus, Fmt.Ansys, Fmt.Zset)

    @classmethod
    def name_from_extension(cls, ext):
        for fmt in cls.all():
            if ext in Fmt.extensions(fmt):
                return Fmt.name(fmt)
        return "Unknown"


def convert(
    input_file,
    input_format,
    output_file,
    output_format,
    output_comm=None,
    skip_types=[],
    verbose=False,
):
    """Main entry point of the converter.

    Arguments:
        input_file (str) : Path to the input file.
        input_format (Fmt): Format of the input file.
        output_file (str): Path to the output file.
        output_format (Fmt): Format of the output file.
        output_comm (str): The code_aster setup associated to the conversion.
        skip_types (list[str]): List of cell types ( in origin format ) to skip.
        verbose (bool, optional) : Verbosity.

    Returns:
        bool: Status of the conversion: *True* in case of success, *False* otherwise.

    """

    # SYSTUS -> MED
    if input_format == Fmt.Systus and output_format == Fmt.Salome:
        MedConverterSystus.convert_systus_to_med(input_file, output_file, skip_types, verbose)

    # MED -> SYSTUS
    elif input_format == Fmt.Salome and output_format == Fmt.Systus:
        MedConverterSystus.convert_med_to_systus(input_file, output_file, verbose)

    # ABAQUS -> MED
    elif input_format == Fmt.Abaqus and output_format == Fmt.Salome:
        MedConverterAbaqus.convert_abaqus_to_med(input_file, output_file, verbose)

    # ANSYS -> MED + COMM
    elif input_format == Fmt.Ansys and output_format == Fmt.Salome:
        MedConverterAnsys.convert_ansys_to_med(input_file, output_file, output_comm, verbose)

    # ZSET -> MED
    elif input_format == Fmt.Zset and output_format == Fmt.Salome:
        MedConverterZset.convert_zset_to_med(input_file, output_file, verbose)

    # MED -> ZSET
    elif input_format == Fmt.Salome and output_format == Fmt.Zset:
        MedConverterZset.convert_med_to_zset(input_file, output_file, verbose)

    # ASTER -> MED
    elif input_format == Fmt.Aster and output_format == Fmt.Salome:
        MedConverterAster.convert_aster_to_med(input_file, output_file, verbose)

    # MED -> ASTER
    elif input_format == Fmt.Salome and output_format == Fmt.Aster:
        MedConverterAster.convert_med_to_aster(input_file, output_file, verbose)

    # TETGEN -> MED
    elif input_format == Fmt.Tetgen and output_format == Fmt.Salome:
        MedConverterTetgen.convert_tetgen_to_med(input_file, output_file, output_comm, verbose)

    else:
        raise ValueError("Unsupported format conversion!")

    return True
