# -*- coding: utf-8 -*-

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
