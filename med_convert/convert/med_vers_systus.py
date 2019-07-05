#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Conversion d'un fichier du format MED vers le format SYSTUS

Copyright EDF 2019
Gérald NICOLAS
+33.1.78.19.43.52
"""
#
#
#========================= Les imports - Début ===================================
#
from .logger import logger
import numpy as np
#
import MEDLoader as ml
#
#========================== Les imports - Fin ====================================
#
#=========================== Début de la fonction ================================
#
def cv_med_vers_systus (meshmedfileread, verbose, verbose_max=False):
    """Conversion du maillage du format MED vers le format SYSTUS

    Entrées :
    :meshmedfileread: fichier au format MED
    Sorties :
    :erreur: code d'erreur
    :message: message d'erreur
    :les_lignes: les lignes du fichier à écrire
    """
    
    blabla = "Dans %s.cv_med_vers_systus"%(__name__)
    logger.debug(blabla)
    #
    erreur = 0
    message = ""
    les_lignes = ""
    #
    return erreur, message, les_lignes
#
#===========================  Fin de la fonction =================================
#
#
#==================================================================================
# Auto-test
#==================================================================================
#
if __name__ == "__main__" :
#
  pass
