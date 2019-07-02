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

from __future__ import unicode_literals

import salome_pluginsmanager

# pragma pylint: disable=invalid-name

from convmail.gui.utilities import translate
from convmail.gui.gui import start

try:
    title = translate("ConvMail",
                      "Mesh Converter")
    description = translate("ConvMail",
                            "GUI plugin to convert meshes")
    salome_pluginsmanager.AddFunction(title, description, start)
except: # pragma pylint: disable=bare-except
    error = translate("ConvMail",
                      "ERROR: ConvMail plugin is unavailable")
    salome_pluginsmanager.logger.info(error)
