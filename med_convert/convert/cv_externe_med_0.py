#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Conversion de fichiers entre les formats externe et MED

Copyright EDF 2019
Gérald NICOLAS
+33.1.78.19.43.52
"""
#
__revision__ = "V02.03"
#
# Les imports standard
import sys
import os
#
#================== A PERSONNALISER - DEBUT ==================
#
# REP_EXTERNE = répertoire pour externe
SALOME_HOME = os.environ["SALOME_HOME"]
REP_EXTERNE = os.path.join(SALOME_HOME, "salome-med-convert")
#
#=================== A PERSONNALISER - FIN ==================
#
#============================= Paramétrage =======================================
# REPSCRIPT = répertoire des scripts
REPSCRIPT = os.path.join(REP_EXTERNE, "med_convert", "convert")
sys.path.append(REPSCRIPT)
from cv_externe_med import ExterneMED
#=================================================================================
#
#==================================================================================
# Lancement
#==================================================================================
#
if __name__ == "__main__" :
#
# 1. Options
#
  VERBOSE = True
  VERBOSE = False
  HOME = os.environ["HOME"]
  REP_DATA = os.path.join(HOME, "MAILLAGE", "SYSTUS")
#
  REP_TRAV = os.path.join(REP_DATA, "Conversion_Systus_Aster", "Maillages", "Maillages_Complexes", "CUVE")
  NOM_FICHIER = "01_CUVE_900_DONN20"
  NOM_FICHIER = "07_CUVE_900_REVET_FISS_DONN20"
#
  REP_TRAV = os.path.join(REP_DATA, "Conversion_Systus_Aster", "Maillages", "Maillages_Complexes", "COUDES")
  NOM_FICHIER = "Coude_A_quad_DONN1000"
  NOM_FICHIER = "Coude_A_DONN1000"
#
  REP_TRAV = os.path.join(REP_DATA, "Conversion_Systus_Aster", "Maillages", "Maillages_Complexes", "PIQUAGE")
  NOM_FICHIER = "PIQUAGE_RIS_900_INSTA_DONN1005"
  NOM_FICHIER = "PIQUAGE_RIS_900_SAIN_DONN1005"
#
  REP_TRAV = os.path.join(REP_DATA, "Conversion_Systus_Aster", "Maillages", "Maillages_Simples")
  NOM_FICHIER = "CARRE_DONN1.mod"
  NOM_FICHIER = "RECTANGLE_DONN1"
  NOM_FICHIER = "COURONNE_DONN1"
  NOM_FICHIER = "MOTIF_DONN1"
  NOM_FICHIER = "CARRE_DONN1"
#
  FICEXTERNE = os.path.join(REP_TRAV, NOM_FICHIER+".ASC")
#
  TYPE_EXTERNE = "SYSTUS"
  TYPE_CV = 0
#
  LAUX = list()
  LAUX.append(("type_externe", TYPE_EXTERNE))
  LAUX.append(("type_cv", TYPE_CV))
  LAUX.append(("ficexterne", FICEXTERNE))
  FICMED = os.path.join(REP_TRAV, "maill.med")
  LAUX.append(("ficmed", FICMED))
#
  #print ("LAUX = ", LAUX)
#
  L_OPTIONS = list()
#
  for TAUX in LAUX :
    if isinstance(TAUX, str) :
      SAUX = TAUX
    else :
      if isinstance(TAUX[1], int) :
        SAUX = "%d" % TAUX[1]
      elif isinstance(TAUX[1], float) :
        SAUX = "%f" % TAUX[1]
      else :
        SAUX = TAUX[1]
      SAUX = "--" + TAUX[0] + "=" + SAUX
    L_OPTIONS.append(SAUX)
  if VERBOSE :
    L_OPTIONS.append("-v")
  #L_OPTIONS.append("-vmax")
  #L_OPTIONS.append("-h")
#
# 2. Lancement de la classe
#
  #print ("L_OPTIONS :", L_OPTIONS)
  EXTERNE_MED = ExterneMED(L_OPTIONS)
#
  if ( "-h" in L_OPTIONS ) :
    sys.stdout.write(EXTERNE_MED.__doc__+"\n")
#
  else :
    ERREUR, MESSAGE_ERREUR = EXTERNE_MED.lancement()
#
    sys.stdout.write(EXTERNE_MED.message_info+"\n")
    if not EXTERNE_MED._affiche_aide_globale :
      if ( MESSAGE_ERREUR is not None ) :
        MESSAGE_ERREUR += "\n Code d'erreur : %d\n" % ERREUR
        sys.stderr.write(MESSAGE_ERREUR)
#
  del EXTERNE_MED
#
  #if ( MESSAGE_ERREUR in ("", None) ) :
    #sys.exit(0)
  #else :
    #sys.exit(1)
