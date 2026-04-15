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
Deployment to SALOME.
"""

import salome_pluginsmanager
from PyQt5 import Qt as Q

# pragma pylint: disable=invalid-name

if "fr" in Q.QLocale.system().name():
    title = "salome_meca/Convertisseur de maillage"
    description = "IHM pour la conversion de maillages"
    error = "ERROR: L'outil MedConvert n'est pas disponible"

else:
    title = "salome_meca/Mesh Converter"
    description = "GUI plugin to convert meshes"
    error = "ERROR: MedConvert plugin is unavailable"

try:
    from medconverter.gui import startGUIfromSalome

    salome_pluginsmanager.AddFunction(title, description, startGUIfromSalome)
except:  # pragma pylint: disable=bare-except
    salome_pluginsmanager.logger.info(error)
