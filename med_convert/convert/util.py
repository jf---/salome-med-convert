#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Conversion d'un fichier du format externe vers le format MED

Fonctions utilitaires.

Copyright EDF 2019
Gérald NICOLAS
+33.1.78.19.43.52
"""
#
__revision__ = "V3.02"
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
  if verbose:
    laux = sorted(caract_maille.keys())
    texte = ""
    for type_maille in laux:
      texte += "\n... Type '%5s' : nombre de noeuds = %2d, code medcoupling = %3d, dimension = %d" % (type_maille, caract_maille[type_maille][0], caract_maille[type_maille][1], caract_maille[type_maille][2])
    print (texte)
#
  return caract_maille
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def get_l_type_mailles (verbose=False):
  """Création des dictionnaires des types de mailles par dimension

Entrées :
Sorties :
  :l_type_mailles: dictionnaire des types de mailles
    . clé : le dimension
    . valeur : la liste des types de mailles associés
  """
#
  nom_fonction = __name__ + "/get_l_type_mailles"
  blabla = "\nDans " + nom_fonction
  if verbose:
    print (blabla)
#
# 1. Récupération des caractéristiques des mailles
#
  caract_maille = get_caract_mailles (verbose)
#
# 2. Classement
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
  l_type_mailles = dict()
  l_type_mailles[0] = l_type_mailles_p
  l_type_mailles[1] = l_type_mailles_s
  l_type_mailles[2] = l_type_mailles_f
  l_type_mailles[3] = l_type_mailles_v
#
  return l_type_mailles
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def print_bilan ( sdim, nbr_entites, verbose=False ) :
  """Affichage des bilans

Entrées :
  :sdim: dimension de l'espace
  :nbr_entites: dictionnaire du nombre d'entités par type
Sorties:
  :nbr_mailles_dim: nombre de mailles par dimension
  """
#
  nom_fonction = __name__ + "/print_bilan"
  blabla = "\nDans " + nom_fonction
  if verbose:
    print (blabla)
#
# 1. Récupération des des listes des types de mailles par dimension
#
  l_type_mailles = get_l_type_mailles ()
#
# 2. tri
#
  nbr_mailles_dim = dict()
#
  for ndim in range(sdim+1):
    print_bilan_0 ( sdim, nbr_entites, ndim, l_type_mailles, nbr_mailles_dim, verbose )
#
#
  return nbr_mailles_dim
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def print_bilan_0 ( sdim, nbr_entites, ndim, l_type_mailles, nbr_mailles_dim, verbose=False ) :
  """Affichage des bilans pour une dimension donnée

Entrées :
  :sdim: dimension de l'espace
  :nbr_entites: dictionnaire du nombre d'entités par type
  :ndim: dimension à traiter
  :l_type_mailles: liste des types de mailles pour la dimension courante
Entrées/Sorties:
  :nbr_mailles_dim: nombre de mailles par dimension
  """
#
  nom_fonction = __name__ + "/print_bilan_0"
  blabla = "\nDans " + nom_fonction
  if verbose:
    print (blabla)
#
# 1. Messages
#
  d_aux = dict()
  d_aux[3] = "volumes       "
  d_aux[2] = "faces         "
  d_aux[1] = "segments      "
  d_aux[0] = "mailles-points"
#
# 2. Décompte
#
  nbr_mailles_dim[ndim] = 0
  if ( sdim >= ndim ) :
    for type_maille in l_type_mailles[ndim] :
      if type_maille in nbr_entites:
        nbr_mailles_dim[ndim] += nbr_entites[type_maille]
    if verbose:
      print ( ".. Nombre de %14s : %8d" % (d_aux[ndim], nbr_mailles_dim[ndim]) )
#
#
  return
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def cree_maillage_par_niveau ( maillage_nom, sdim, nbr_noeuds, nbr_mailles_dim, coordinates, verbose ) :
  """Création de la structure des maillages

Entrées:
  :maillage_nom: nom du maillage
  :sdim: dimension de l'espace
  :nbr_noeuds: nombre de noeuds
  :nbr_mailles_dim: nombre de mailles par dimension
  :coordinates: les coordonnées
Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
  :le_maillage_niveau: dictionnaire des maillages par niveau
  :d_niveau: dictionnaire des niveau par dimension
  """
#
  nom_fonction = __name__ + "/cree_maillage_par_niveau"
  blabla = "\nDans " + nom_fonction
  if verbose:
    print (blabla)
#
# 1. Les coordonnées
#
  les_coords = ml.DataArrayDouble(coordinates, nbr_noeuds, sdim)
#
# 2. Les maillages par niveau
#
  le_maillage_niveau = dict()
#
  niveau = 1
  d_niveau = dict()
  for ndim in range (sdim, 0, -1 ) :
#
    if ( nbr_mailles_dim[ndim] > 0 ) :
#
      if ( niveau > 0 ) :
        niveau = 0
#
      cree_maillage_par_niveau_0 ( maillage_nom, niveau, ndim, les_coords, nbr_mailles_dim, d_niveau, le_maillage_niveau, verbose )
#
    if ( niveau <= 0 ) :
      niveau -= 1
#
#
  return le_maillage_niveau, d_niveau
#
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def cree_maillage_par_niveau_0 ( maillage_nom, niveau, ndim, les_coords, nbr_mailles_dim, d_niveau, le_maillage_niveau, verbose=False ) :
  """Création du maillage d'un niveau

Entrées:
  :maillage_nom: nom du maillage
  :niveau: niveau du maillage
  :ndim: dimension du maillage
  :les_coords: les coordonnées
  :nbr_mailles_dim: nombre de mailles par dimension
Entrées/Sorties :
  :le_maillage_niveau: dictionnaire des maillages par niveau
  :d_niveau: dictionnaire des niveau par dimension
  """
#
  nom_fonction = __name__ + "/cree_maillage_par_niveau_0"
  blabla = "\nDans " + nom_fonction
  if verbose:
    print (blabla)
#
  if verbose:
    texte = "\n... Création du maillage de dimension %d" % ndim
    texte += " sous le nom '%s'" % maillage_nom
    print (texte)
#
  d_niveau[ndim] = niveau
  le_maillage_niveau[niveau] = ml.MEDCouplingUMesh(maillage_nom, 2)
  le_maillage_niveau[niveau].setMeshDimension(ndim)
#
  #print (les_coords)
  if verbose:
    texte = "... Enregistrement des coordonnées dans le maillage du niveau %d" % niveau
    print (texte)
  le_maillage_niveau[niveau].setCoords(les_coords)
#
  if verbose:
    texte = "... Allocation pour %d cellules" % nbr_mailles_dim[ndim]
    texte += " dans le maillage du niveau %d" % niveau
    print (texte)
  le_maillage_niveau[niveau].allocateCells(nbr_mailles_dim[ndim])
#
  return
#
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
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
    VERBOSE = True
    CARACT_MAILLE = get_caract_mailles (VERBOSE)
    print ("CARACT_MAILLE :\n", CARACT_MAILLE)
#
# ==============================================================
#
    print ("\nTest de get_l_type_mailles :")
#
    VERBOSE = False
    L_TYPE_MAILLES = get_l_type_mailles (VERBOSE)
    print ("L_TYPE_MAILLES_V :", L_TYPE_MAILLES[0])
    print ("L_TYPE_MAILLES_F :", L_TYPE_MAILLES[1])
    print ("L_TYPE_MAILLES_S :", L_TYPE_MAILLES[2])
    print ("L_TYPE_MAILLES_P :", L_TYPE_MAILLES[3])
#
# ==============================================================
#
    print ("\nTest de print_bilan :")
#
    VERBOSE = True
    SDIM = 3
    NBR_ENTITES = dict()
    NBR_ENTITES["TETR4"] = 1960
    NBR_ENTITES["TRIA6"] = 271983
    NBR_MAILLES_DIM = print_bilan (SDIM, NBR_ENTITES, VERBOSE)
    print ("NBR_MAILLES_DIM :\n", NBR_MAILLES_DIM)
#
# ==============================================================
#
    break
#
  if not ERREUR :
    print ("Fin normale")
