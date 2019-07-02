#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Conversion d'un fichier du format externe vers le format MED

Fonctions utilitaires.

Copyright EDF 2019
Gérald NICOLAS
+33.1.78.19.43.52
"""
#
__revision__ = "V2.02"
#
#========================= Les imports - Début ===================================
#
import MEDLoader as ml
#
#========================== Les imports - Fin ====================================
#
#=========================== Début de la fonction ================================
#
def get_caract_mailles (verbose=False):
  """Création des caractéristiques des mailles

Entrées :
Sorties :
  :caract_maille: dictionnaire de caractérisation des mailles
    . la clé est le nom
    . la donnée est le triplet (nombre de noeuds, code medcoupling, dimension)
  """
#
  nom_fonction = __name__ + "/get_caract_mailles"
  blabla = "\nDans " + nom_fonction
  if verbose:
    print (blabla)
#
  caract_maille = dict()
#
  caract_maille["POI"]   = ( 1, ml.NORM_POINT1,  0)
#
  caract_maille["SEG2"]  = ( 2, ml.NORM_SEG2,    1)
  caract_maille["TRIA3"] = ( 3, ml.NORM_TRI3,    2)
  caract_maille["QUAD4"] = ( 4, ml.NORM_QUAD4,   2)
  caract_maille["TETR4"] = ( 4, ml.NORM_TETRA4,  3)
  caract_maille["HEXA8"] = ( 8, ml.NORM_HEXA8,   3)
  caract_maille["PYRA5"] = ( 5, ml.NORM_PYRA5,   3)
  caract_maille["PENT6"] = ( 6, ml.NORM_PENTA6,  3)
#
  caract_maille["SEG3"]  = ( 3, ml.NORM_SEG3,    1)
  caract_maille["TRIA6"] = ( 6, ml.NORM_TRI6,    2)
  caract_maille["QUAD8"] = ( 8, ml.NORM_QUAD8,   2)
  caract_maille["TET10"] = (10, ml.NORM_TETRA10, 3)
  caract_maille["HEX20"] = (20, ml.NORM_HEXA20,  3)
  caract_maille["PYR13"] = (13, ml.NORM_PYRA13,  3)
  caract_maille["PEN15"] = (15, ml.NORM_PENTA15, 3)
#
  return caract_maille
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def get_l_type_mailles (caract_maille, verbose=False):
  """Création des liste des types de mailles par dimension

Entrées :
  :caract_maille: dictionnaire de caractérisation des mailles
    . la clé est le nom
    . la donnée est le triplet (nombre de noeuds, code medcoupling, dimension)
Sorties :
  :l_type_mailles_v: liste des types de mailles de type 'volume'
  :l_type_mailles_f: liste des types de mailles de type 'face'
  :l_type_mailles_s: liste des types de mailles de type 'segement'
  :l_type_mailles_p: liste des types de mailles de type 'point'
  """
#
  nom_fonction = __name__ + "/get_l_type_mailles"
  blabla = "\nDans " + nom_fonction
  if verbose:
    print (blabla)
#
  l_type_mailles_p = list()
  l_type_mailles_s = list()
  l_type_mailles_f = list()
  l_type_mailles_v = list()
#
  for la_cle in caract_maille:
    if ( caract_maille[la_cle][2] == 0 ):
      l_type_mailles_p.append(la_cle)
    elif ( caract_maille[la_cle][2] == 1 ):
      l_type_mailles_s.append(la_cle)
    elif ( caract_maille[la_cle][2] == 2 ):
      l_type_mailles_f.append(la_cle)
    elif ( caract_maille[la_cle][2] == 3 ):
      l_type_mailles_v.append(la_cle)
#
  l_type_mailles_p.sort()
  l_type_mailles_s.sort()
  l_type_mailles_f.sort()
  l_type_mailles_v.sort()
#
  return l_type_mailles_v, l_type_mailles_f, l_type_mailles_s, l_type_mailles_p
#
#===========================  Fin de la fonction =================================
#
#==================================================================================
# Auto-test
#==================================================================================
#
if __name__ == "__main__" :
#
  ERREUR = 0
  while not ERREUR :
#
# ==============================================================
#
    print ("\nTest de get_caract_mailles :")
#
    VERBOSE = False
    CARACT_MAILLE = get_caract_mailles (VERBOSE)
    print ("CARACT_MAILLE :\n", CARACT_MAILLE)
#
# ==============================================================
#
    print ("\nTest de get_l_type_mailles :")
#
    VERBOSE = False
    L_TYPE_MAILLES_V, L_TYPE_MAILLES_F, L_TYPE_MAILLES_S, L_TYPE_MAILLES_P = get_l_type_mailles (CARACT_MAILLE, VERBOSE)
    print ("L_TYPE_MAILLES_V :", L_TYPE_MAILLES_V)
    print ("L_TYPE_MAILLES_F :", L_TYPE_MAILLES_F)
    print ("L_TYPE_MAILLES_S :", L_TYPE_MAILLES_S)
    print ("L_TYPE_MAILLES_P :", L_TYPE_MAILLES_P)
#
    break
#
  if not ERREUR :
    print ("Fin normale")
