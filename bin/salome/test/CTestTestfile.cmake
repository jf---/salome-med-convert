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
SET(COMPONENT_NAME SMECA_MAC3STATIQUE)
SET(TIMEOUT        150)
SET(MAC3STATIQUE_RUN "$ENV{SALOMEMECA_MAC3STATIQUE_ROOT_DIR}/lib/python2.7/site-packages/salome/mac3statique/run_unittest.py")

SET (GOOD_TESTS 
mac3statique.test
)

FOREACH(tfile ${GOOD_TESTS})
  SET(TEST_NAME MAC3STATIQUE_${tfile})
  ADD_TEST(${TEST_NAME} python ${MAC3STATIQUE_RUN} -t ${tfile})
  SET_TESTS_PROPERTIES(${TEST_NAME} PROPERTIES LABELS "${COMPONENT_NAME};SMECA_INTEGR")
ENDFOREACH()
