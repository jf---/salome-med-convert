# Copyright (C) 2015  CEA/DEN, EDF R&D
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

SET(SALOME_TEST_DRIVER "$ENV{ABSOLUTE_APPLI_PATH}/bin/salome/appliskel/salome_test_driver.py")
SET(COMPONENT_NAME SMECA_MEDCONVERTER)
SET(TIMEOUT        3600)

SET(MEDCONVERTER_TESTDIR "$ENV{SALOMEMECA_MEDCONVERTER_ROOT_DIR}/share/salome/resources/test")

SET(MEDCONVERTER_TEST_FILES
  test_simple.py
  test_backward_simple.py
  test_private.py
  test_perf.py
  test_utilities.py
  )

FOREACH(tfile ${MEDCONVERTER_TEST_FILES})
  SET(TEST_NAME MEDCONVERTER_${tfile})
  ADD_TEST(${TEST_NAME} python ${SALOME_TEST_DRIVER} ${TIMEOUT} ${MEDCONVERTER_TESTDIR}/${tfile})
  SET_TESTS_PROPERTIES(${TEST_NAME} PROPERTIES LABELS "${COMPONENT_NAME};SMECA_INTEGR")
ENDFOREACH()
