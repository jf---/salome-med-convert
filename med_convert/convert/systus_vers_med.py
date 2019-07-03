#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Conversion d'un fichier du format SYSTUS vers le format MED

Copyright EDF 2019
Gérald NICOLAS
+33.1.78.19.43.52
"""
#
__revision__ = "V2.02"
#
#========================= Les imports - Début ===================================
#
import numpy as np
#
from util import get_caract_mailles
from util import print_bilan
#
import MEDLoader as ml
#
#========================== Les imports - Fin ====================================
#
#=========================== Début de la fonction ================================
#
def cv_systus_vers_med (les_lignes, verbose, verbose_max=False):
  """Conversion du maillage

Entrées :
  :les_lignes: les lignes du fichier à convertir
Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
  :le_maillage_niveau: dictionnaire des maillages par niveau
  :d_groupes: dictionnaire des groupes par niveau
  """
#
  nom_fonction = __name__ + "/cv_systus_vers_med"
  blabla = "\nDans " + nom_fonction
  if verbose_max:
    print (blabla)
#
  erreur = 0
  message = ""
  le_maillage_niveau = None
  d_groupes = None
#
  while ( not erreur ) :
#
# 1. Exploration des données
#
    erreur, message, maillage_nom, sdim, nbr_entites, coordinates, tb_renum_node, tb_renum_elem, tb_type_elem = systus_fichier_1 ( les_lignes, verbose, verbose_max)
    if erreur:
      break
#
# 2. Bilan
#
    nbr_mailles_dim = print_bilan ( sdim, nbr_entites, verbose_max )
#
# 3. Création des maillages par niveau
#
    erreur, message, le_maillage_niveau, d_groupes, d_niveau = systus_fichier_2 ( maillage_nom, sdim, nbr_entites, nbr_mailles_dim, coordinates, tb_renum_node, tb_renum_elem, tb_type_elem, verbose, verbose_max )
    if erreur:
      break
#
    break
#
#
  return erreur, message, le_maillage_niveau, d_groupes
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def systus_fichier_1 ( les_lignes, verbose, verbose_max):
  """Décodage des lignes du fichier

Entrées :
  :les_lignes: les lignes du fichier à convertir
Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
  :maillage_nom: nom du maillage
  :sdim: dimension de l'espace
  :nbr_entites: dictionnaire du nombre d'entités par type
  :coordinates: les coordonnées
  :tb_renum_node: tableau de renumérotation des noeuds
  :tb_renum_elem: tableau de renumérotation des éléments
  :tb_type_elem: tableau de typage des éléments
  """
#
  nom_fonction = __name__ + "/systus_fichier_1"
  blabla = "\nDans " + nom_fonction
  if verbose_max:
    texte = blabla
    print (texte)
#
  erreur = 0
  message = ""
  coordinates = None
  nbr_entites = dict()
#
  while ( not erreur ) :
#
# 1. Le nom du maillage
#
    maillage_nom = les_lignes[1].strip()[:-1]
    if verbose_max:
      print ("... maillage_nom = '%s'" % maillage_nom)
    if ( len(maillage_nom) == 0 ):
      maillage_nom = "MAILLAGE"
      print ("Pas de nom de maillage dans le fichier.\nOn impose le nom '%s'" % maillage_nom)
#
# 2. Les repères
#
    erreur, message, d_nro_section = systus_fichier_1_r ( les_lignes, verbose_max)
    if erreur:
      break
#
# 3. Dimension de l'espace
#
    laux = d_nro_section["l_bn"][0].split()
    sdim = int(laux[2])
    if verbose:
      texte = ".. Dimension d'espace : %d" % sdim
      print (texte)
#
# 3. Noeuds
#
    nbr_entites["Noeuds"], coordinates, tb_renum_node = systus_fichier_1_n ( les_lignes, d_nro_section["l_bn"][1]+1, d_nro_section["l_en"][1], sdim, verbose_max)
#
# 4. Eléments
#
    tb_renum_elem, tb_type_elem = systus_fichier_1_e ( les_lignes, d_nro_section["l_be"][1]+1, d_nro_section["l_ee"][1], nbr_entites, verbose_max)
    if verbose_max:
      break
#
#
    break
#
  return erreur, message, maillage_nom, sdim, nbr_entites, coordinates, tb_renum_node, tb_renum_elem, tb_type_elem
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def systus_fichier_1_r ( les_lignes, verbose_max=False):
  """Décodage des lignes du fichier : les repères

Entrées :
  :les_lignes: les lignes du fichier à convertir
Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
  :d_nro_section: dictionnaire des numéros des lignes des repères
    . clé : nom parmi ("l_bn", "l_en", "l_be", "l_ee", "l_bg", "l_eg")
    . valeur : (la ligne, le numéro de la ligne)

  """
#
  nom_fonction = __name__ + "/systus_fichier_1_r"
  blabla = "\nDans " + nom_fonction
  if verbose_max:
    texte = blabla
    print (texte)
#
  erreur = 0
  message = ""
#
  while not erreur:
#
# 1. Les lignes de début de section et de fin des sections
#    Remarque : on suppose que les groupes sont après les noeuds et les mailles
#    Remarque : on n'utilise pas la fonction index car on ne sait pas comment est géré la fin de ligne
#
    d_nro_section = dict()
#
    for iaux, ligne in enumerate(les_lignes) :
#
      if ( "BEGIN_NODES" in ligne ):
        d_nro_section["l_bn"] = (ligne, iaux)
      elif ( "END_NODES" in ligne ):
        d_nro_section["l_en"] = (ligne, iaux)
      elif ( "BEGIN_ELEMENTS" in ligne ):
        d_nro_section["l_be"] = (ligne, iaux)
      elif ( "END_ELEMENTS" in ligne ):
        d_nro_section["l_ee"] = (ligne, iaux)
      elif ( "BEGIN_GROUPS" in ligne ):
        d_nro_section["l_bg"] = (ligne, iaux)
      elif ( "END_GROUPS" in ligne ):
        d_nro_section["l_eg"] = (ligne, iaux)
        break
#
# 2. Contrôle
#
    for n_ligne in ("l_bn", "l_en", "l_be", "l_ee", "l_bg", "l_eg"):
      if ( n_ligne not in d_nro_section ):
        message += "Impossible de trouver la ligne associée à %s\n" % n_ligne
        erreur += 1
#
    if erreur:
      break
#
    if verbose_max:
      print ("d_nro_section :")
      for la_cle in d_nro_section:
        print (la_cle, ":", d_nro_section[la_cle])
#
    break
#
  return erreur, message, d_nro_section
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def systus_fichier_1_n ( les_lignes, ideb, ifin, sdim, verbose_max=False):
  """Décodage des lignes du fichier : les noeuds

Entrées :
  :les_lignes: les lignes du fichier à convertir
  :ideb: indice de la ligne pour le premier noeud
  :ifin: indice de la ligne suivant le dernier noeud
  :sdim: dimension de l'espace
Sorties :
  :nbr_noeuds: nombre de noeuds
  :coordinates: les coordonnées
  :tb_renum_node: tableau de renumérotation des noeuds
  """
#
  nom_fonction = __name__ + "/systus_fichier_1_n"
  blabla = "\nDans " + nom_fonction
  if verbose_max:
    texte = blabla
    print (texte)
#
# 1. Nombre de noeuds
#
  nbr_noeuds = ifin - ideb
  if verbose_max:
    print (".. Nombre de noeuds : %d" % nbr_noeuds)
#
# 2. Tableau de renumérotation des noeuds
#
  tb_renum_node = np.zeros(nbr_noeuds, dtype=np.int)
#
# 3. Stockage
#
  coordinates = list()
  for iaux, ligne in enumerate(les_lignes[ideb:ifin]):
    laux = ligne.split()
    tb_renum_node[iaux] = int(laux[0])
    for s_coo in laux[-sdim:] :
      coordinates.append(float(s_coo))
#
# 4. Information
#
  if verbose_max:
    texte = "... Plus petit numéro de noeud : %8d\n" % tb_renum_node.min()
    texte += "... Plus grand numéro de noeud : %8d" % tb_renum_node.max()
    print (texte)
#
  return nbr_noeuds, coordinates, tb_renum_node
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def systus_fichier_1_e ( les_lignes, ideb, ifin, nbr_entites, verbose_max=False):
  """Décodage des lignes du fichier : les éléments

Entrées :
  :les_lignes: les lignes du fichier à convertir
  :ideb: indice de la ligne pour le premier élément
  :ifin: indice de la ligne suivant le dernier élément
Sorties :
  :tb_renum_elem: tableau de renumérotation des éléments
  :tb_type_elem: tableau de typage des éléments
Entrées/Sorties :
  :nbr_entites: nombre d'entités par type
  """
#
  nom_fonction = __name__ + "/systus_fichier_1_e"
  blabla = "\nDans " + nom_fonction
  if verbose_max:
    texte = blabla
    print (texte)
#
# 1. Nombre d'éléments
#
  nbr_entites["Elements"] = ifin - ideb
  if verbose_max:
    print (".. Nombre d'éléments : %d" % nbr_entites["Elements"])
#
# 2. Tableau de renumérotation des éléments et de typage
#
  tb_renum_elem = np.zeros(nbr_entites["Elements"], dtype=np.int)
  tb_type_elem = np.zeros(nbr_entites["Elements"], dtype=np.int)
#
# 3. Stockage
#
  for iaux, ligne in enumerate(les_lignes[ideb:ifin]):
#
    laux = ligne.split()
    tb_renum_elem[iaux] = int(laux[0])
    tb_type_elem[iaux] = int(laux[1])
#
# 4. Décompte par type
# 4.1. Dictionnaire de caractérisation des mailles
#    . la clé est le nom
#    . la donnée est le triplet (nombre de noeuds, code medcoupling, dimension)
#
  caract_maille = get_caract_mailles ()
#
# 4.2. Décompte
#
  for type_maille in caract_maille:
#
    nbn = caract_maille[type_maille][0]
    ndim = caract_maille[type_maille][2]
#
    nbr_entites[type_maille] = 0
    for iaux in range(10):
      jaux = ndim*1000 + iaux*100 + nbn
      np_aux = (tb_type_elem == jaux).nonzero()
      nbr_entites[type_maille] += len(np_aux[0])
#
# 5. Information
#
  if verbose_max:
    texte = "... Plus petit numéro d'éléments : %8d\n" % tb_renum_elem.min()
    texte += "... Plus grand numéro d'éléments : %8d" % tb_renum_elem.max()
    for type_maille in caract_maille:
      texte += "\n... Nombre d'éléments pour le type '%5s' : %8d" % (type_maille,nbr_entites[type_maille])
    print (texte)
#
  return tb_renum_elem, tb_type_elem
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def systus_fichier_2 ( maillage_nom, sdim, nbr_entites, nbr_mailles_dim, coordinates, tb_renum_node, tb_renum_elem, tb_type_elem, verbose, verbose_max ) :
  """Création des maillages

Entrées:
  :maillage_nom: nom du maillage
  :sdim: dimension de l'espace
  :nbr_entites: dictionnaire du nombre d'entités par type
  :nbr_mailles_dim: nombre de mailles par dimension
  :coordinates: les coordonnées
  :tb_renum_node: tableau de renumérotation des noeuds
  :tb_renum_elem: tableau de renumérotation des éléments
  :tb_type_elem: tableau de typage des éléments
Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
  :le_maillage_niveau: dictionnaire des maillages par niveau
  :d_groupes: dictionnaire des groupes par niveau
  :d_niveau: dictionnaire des niveau par dimension
  """
#
  nom_fonction = __name__ + "/systus_fichier_2"
  blabla = "\nDans " + nom_fonction
  if verbose_max:
    texte = blabla
    print (texte)
#
  erreur = 0
  message = ""
#
  while ( not erreur ) :
#
# 1. Les coordonnées
#
    les_coords = ml.DataArrayDouble(coordinates, nbr_entites["Noeuds"], sdim)
#
# 2. Les maillages par niveau
#
    le_maillage_niveau = dict()
    d_groupes = dict()
#
    niveau = 1
    d_niveau = dict()
    for ndim in range (sdim, 0, -1 ) :
#
      if ( nbr_mailles_dim[ndim] > 0 ) :
#
        if verbose:
          texte = "\n... Création du maillage de dimension %d" % ndim
          texte += " sous le nom '%s'" % maillage_nom
          print (texte)
#
        if ( niveau > 0 ) :
          niveau = 0
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
      if ( niveau <= 0 ) :
        niveau -= 1
#
    #for niveau in le_maillage_niveau :
      #print ("Maillage du niveau %d\n" %niveau, le_maillage_niveau[niveau])
#
#
    break
#
  return erreur, message, le_maillage_niveau, d_groupes, d_niveau
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
#===========================  Fin de la fonction =================================
#
#==================================================================================
# Auto-test
#==================================================================================
#
if __name__ == "__main__" :
#
  pass
