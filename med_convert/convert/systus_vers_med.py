#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Conversion d'un fichier du format SYSTUS vers le format MED

Copyright EDF 2019
Gérald NICOLAS
+33.1.78.19.43.52
"""
#
__revision__ = "V03.01"
#
#========================= Les imports - Début ===================================
#
import numpy as np
#
from util import cree_maillage_par_niveau_0
from util import get_caract_mailles
from util import gettabrecip
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
    erreur, message, d_nro_section, maillage_nom, sdim, nbr_entites, coordinates, tb_renum_node, tb_renum_elem, tb_type_elem = cv_systus_med_1 ( les_lignes, verbose, verbose_max)
    if erreur:
      break
#
# 2. Bilan
#
    nbr_mailles_dim = print_bilan ( sdim, nbr_entites, verbose_max )
#
# 3. Création des maillages par niveau
#
    erreur, message, le_maillage_niveau, d_groupes, d_niveau = cv_systus_med_2 ( les_lignes, d_nro_section, maillage_nom, sdim, nbr_entites, nbr_mailles_dim, coordinates, tb_renum_node, tb_type_elem, verbose, verbose_max )
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
def cv_systus_med_1 ( les_lignes, verbose, verbose_max):
  """Décodage des lignes du fichier

Entrées :
  :les_lignes: les lignes du fichier à convertir
Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
  :d_nro_section: dictionnaire des numéros des lignes des repères
    . clé : nom parmi ("l_bn", "l_en", "l_be", "l_ee", "l_bg", "l_eg")
    . valeur : le numéro de la ligne
  :maillage_nom: nom du maillage
  :sdim: dimension de l'espace
  :nbr_entites: dictionnaire du nombre d'entités par type
  :coordinates: les coordonnées
  :tb_renum_node: tableau de renumérotation des noeuds
  :tb_renum_elem: tableau de renumérotation des éléments
  :tb_type_elem: tableau de typage des éléments
  """
#
  nom_fonction = __name__ + "/cv_systus_med_1"
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
      texte = "\n.. Attention : le nom de maillage est absent dans ce fichier."
      texte += " On impose le nom '%s'" % maillage_nom
      print (texte)
#
# 2. Les repères
#
    erreur, message, d_nro_section = cv_systus_med_1_r ( les_lignes, verbose_max)
    if erreur:
      break
#
# 3. Dimension de l'espace
#
    laux = les_lignes[d_nro_section["l_bn"]].split()
    sdim = int(laux[2])
    if verbose:
      texte = "\n.. Dimension d'espace : %d" % sdim
      print (texte)
#
# 3. Noeuds
#
    nbr_entites["Noeuds"], coordinates, tb_renum_node = cv_systus_med_1_n ( les_lignes, d_nro_section["l_bn"]+1, d_nro_section["l_en"], sdim, verbose_max)
#
# 4. Eléments
#
    tb_renum_elem, tb_type_elem = cv_systus_med_1_e ( les_lignes, d_nro_section["l_be"]+1, d_nro_section["l_ee"], nbr_entites, verbose_max)
    if verbose_max:
      break
#
#
    break
#
  return erreur, message, d_nro_section, maillage_nom, sdim, nbr_entites, coordinates, tb_renum_node, tb_renum_elem, tb_type_elem
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def cv_systus_med_1_r ( les_lignes, verbose_max=False):
  """Décodage des lignes du fichier : les repères

Entrées :
  :les_lignes: les lignes du fichier à convertir
Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
  :d_nro_section: dictionnaire des numéros des lignes des repères
    . clé : nom parmi ("l_bn", "l_en", "l_be", "l_ee", "l_bg", "l_eg")
    . valeur : le numéro de la ligne
  """
#
  nom_fonction = __name__ + "/cv_systus_med_1_r"
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
        d_nro_section["l_bn"] = iaux
      elif ( "END_NODES" in ligne ):
        d_nro_section["l_en"] = iaux
      elif ( "BEGIN_ELEMENTS" in ligne ):
        d_nro_section["l_be"] = iaux
      elif ( "END_ELEMENTS" in ligne ):
        d_nro_section["l_ee"] = iaux
      elif ( "BEGIN_GROUPS" in ligne ):
        d_nro_section["l_bg"] = iaux
      elif ( "END_GROUPS" in ligne ):
        d_nro_section["l_eg"] = iaux
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
def cv_systus_med_1_n ( les_lignes, ideb, ifin, sdim, verbose_max=False):
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
  nom_fonction = __name__ + "/cv_systus_med_1_n"
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
def cv_systus_med_1_e ( les_lignes, ideb, ifin, nbr_entites, verbose_max=False):
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
  nom_fonction = __name__ + "/cv_systus_med_1_e"
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
def cv_systus_med_2 ( les_lignes, d_nro_section, maillage_nom, sdim, nbr_entites, nbr_mailles_dim, coordinates, tb_renum_node, tb_type_elem, verbose, verbose_max ) :
  """Création des maillages

Entrées:
  :les_lignes: les lignes du fichier à convertir
  :d_nro_section: dictionnaire des numéros des lignes des repères
    . clé : nom parmi ("l_bn", "l_en", "l_be", "l_ee", "l_bg", "l_eg")
    . valeur : le numéro de la ligne
  :maillage_nom: nom du maillage
  :sdim: dimension de l'espace
  :nbr_entites: dictionnaire du nombre d'entités par type
  :nbr_mailles_dim: nombre de mailles par dimension
  :coordinates: les coordonnées
  :tb_renum_node: tableau de renumérotation des noeuds
  :tb_type_elem: tableau de typage des éléments
Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
  :le_maillage_niveau: dictionnaire des maillages par niveau
  :d_groupes: dictionnaire des groupes par niveau
  :d_niveau: dictionnaire des niveau par dimension
  """
#
  nom_fonction = __name__ + "/cv_systus_med_2"
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
# 2. Les correspondances entre SYSTUS et MED
#
    d_corres_type, d_num_local = cv_systus_med_3 (verbose_max)
#
# 3. Le tableau réciproque de la numérotation des noeuds
#
    d_tab_recip = gettabrecip (tb_renum_node)
#
# 3. Les maillages par niveau
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
          texte = "\n.. Création du maillage de dimension %d" % ndim
          texte += " sous le nom '%s'" % maillage_nom
          print (texte)
#
        if ( niveau > 0 ) :
          niveau = 0
#
# 3.1. Création de la structure du maillage
#
        cree_maillage_par_niveau_0 ( maillage_nom, niveau, ndim, les_coords, nbr_mailles_dim, d_niveau, le_maillage_niveau, verbose_max )
#
# 3.2. Ajout des mailles du niveau
#
        cv_systus_med_2_0 ( les_lignes[d_nro_section["l_be"]+1:], d_corres_type, d_num_local, ndim, le_maillage_niveau[niveau], tb_type_elem, d_tab_recip, verbose_max )
#
      if ( niveau <= 0 ) :
        niveau -= 1
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
def cv_systus_med_2_0 ( les_lignes, d_corres_type, d_num_local, ndim, maillage, tb_type_elem, d_tab_recip, verbose=False ) :
  """Ajout des mailles dans le maillage d'un niveau

Entrées:
  :les_lignes: les lignes du fichier à convertir - pour les éléments
  :d_corres_type: dictionnaire de la correspondance
    . clé : le type SYSTUS
    . valeur : (la dimension, le nombre de noeuds, le type medcoupling)
  :d_num_local: dictionnaire de la correspondance de numérotation locale
    . clé : le type medcoupling
    . valeur : liste de la position locale MED
  :ndim: dimension du maillage
  :tb_type_elem: tableau de typage des éléments
  :d_tab_recip: tableau réciproque de la renumérotation des noeuds
Entrées/Sorties :
  :maillage: le maillage à compléter
  """
#
  nom_fonction = __name__ + "/cv_systus_med_2_0"
  blabla = "\nDans " + nom_fonction
  if verbose:
    print (blabla)
#
  if verbose:
    texte = "\n... Dimension %d" % ndim
    print (texte)
#
  tb_nodes = np.zeros(27, dtype=np.int32)
#
  nrmail = 0
  for iaux, t_element in enumerate(tb_type_elem):
#
# On filtre sur la bonne dimension
#
    if ( d_corres_type[t_element][0] == ndim ):
#
      nbn = d_corres_type[t_element][1]
      type_med = d_corres_type[t_element][2]
#
# 1. La liste des noeuds dans la numérotation SYSTUS
#
      laux = les_lignes[iaux].split()
      #print (laux[-nbn:])
#
# 2. La liste des noeuds dans la numérotation MED
#
      for jaux, n_systus in enumerate(laux[-nbn:]):
        tb_nodes[d_num_local[type_med][jaux]] = d_tab_recip[int(n_systus)]
      #if verbose:
        #print ("... tb_nodes =", tb_nodes)
#
# 3. Insertion des noeuds dans le maillage medcoupling
#
      maillage.insertNextCell(type_med, nbn, ml.DataArrayInt(tb_nodes))
#
      nrmail += 1
#
  return
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def cv_systus_med_3 ( verbose=False ) :
  """Correspondance entre le type SYSTUS et le type mecoupling

Entrées:
Sorties :
  :d_corres_type: dictionnaire de la correspondance
    . clé : le type SYSTUS
    . valeur : (la dimension, le nombre de noeuds, le type medcoupling)
  :d_num_local: dictionnaire de la correspondance de numérotation locale
    . clé : le type medcoupling
    . valeur : liste de la position locale MED
  """
#
  nom_fonction = __name__ + "/cv_systus_med_3"
  blabla = "\nDans " + nom_fonction
  if verbose:
    print (blabla)
#
# 1. Correspondance entre le type SYSTUS et le type mecoupling
#
  d_corres_type = cv_systus_med_30 ( verbose )
#
# 2. Correspondance entre la numérotation locale SYSTUS et celle de mecoupling
#
  d_num_local = cv_systus_med_31 ( verbose )
#
  return d_corres_type, d_num_local
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def cv_systus_med_30 ( verbose=False ) :
  """Correspondance entre le type SYSTUS et le type mecoupling

Entrées:
Sorties :
  :d_corres_type: dictionnaire de la correspondance
    . clé : le type SYSTUS
    . valeur : (la dimension, le nombre de noeuds, le type medcoupling)
  """
#
  nom_fonction = __name__ + "/cv_systus_med_30"
  blabla = "\nDans " + nom_fonction
  if verbose:
    print (blabla)
#
# 1. Dictionnaire de caractérisation des mailles
#    . la clé est le nom
#    . la donnée est le triplet (nombre de noeuds, code medcoupling, dimension)
#
  caract_maille = get_caract_mailles ()
#
# 2. Affectation
#
  d_corres_type = dict()
  for type_maille in caract_maille:
#
    nbn = caract_maille[type_maille][0]
    ndim = caract_maille[type_maille][2]
    for iaux in range(10):
      jaux = ndim*1000 + iaux*100 + nbn
      d_corres_type[jaux] = (ndim, nbn, caract_maille[type_maille][1])
#
  if verbose:
    texte  = "d_corres_type :"
    for cle in d_corres_type:
      texte += "\n%4d : dimension = %2d, nombre de noeuds = %2d, type medcoupling = %d" % (cle, d_corres_type[cle][0], d_corres_type[cle][1], d_corres_type[cle][2])
    print (texte)
#
  return d_corres_type
#
#
#=========================== Début de la fonction ================================
#
def cv_systus_med_31 ( verbose=False ) :
  """Correspondance entre la numérotation locale SYSTUS et celle de mecoupling

Entrées:
Sorties :
  :d_num_local: dictionnaire de la correspondance de numérotation locale
    . clé : le type medcoupling
    . valeur : liste de la position locale MED
  """
#
  nom_fonction = __name__ + "/cv_systus_med_31"
  blabla = "\nDans " + nom_fonction
  if verbose:
    print (blabla)
#
  d_num_local = dict()
#
# 1. Mailles 0D
#
  d_num_local[ml.NORM_POINT1] = [0]
#
# 2. Mailles 1D
#
  d_num_local[ml.NORM_SEG2] = [0, 1]
#
  d_num_local[ml.NORM_SEG3] = [0, 2, 1]
#
# 3. Mailles 2D
#
  d_num_local[ml.NORM_TRI3] = [0, 1, 2]
  d_num_local[ml.NORM_QUAD4] = [0, 1, 3, 2]
#
  d_num_local[ml.NORM_TRI6] = [0, 2, 4, 1, 3, 5]
  d_num_local[ml.NORM_QUAD8] = [0, 4, 1, 5, 2, 6, 3, 7]
#
# 4. Mailles 3D
#
  d_num_local[ml.NORM_TETRA4] = [0, 1, 2, 3]
  d_num_local[ml.NORM_HEXA8] = list()
  d_num_local[ml.NORM_PYRA5] = list()
  d_num_local[ml.NORM_PENTA6] = list()
#
  d_num_local[ml.NORM_TETRA10] = list()
  d_num_local[ml.NORM_HEXA20] = [18, 16, 14, 12, 6, 4, 2, 0, 17, 15, 13, 19, 11, 10, 9, 8, 5, 3, 1, 7]
  d_num_local[ml.NORM_PYRA13] = list()
  d_num_local[ml.NORM_PENTA15] = [0, 2, 4, 9, 11, 13, 1, 3, 5, 6, 7, 8, 10, 12, 14]
#
  if verbose:
    texte  = "d_num_local :"
    print (texte)
    for cle in d_num_local:
      print ("%2d :" % cle, d_num_local[cle])
#
  return d_num_local
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
#
#===========================  Fin de la fonction =================================
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
  ERREUR = 0
  while not ERREUR :
#
# ==============================================================
#
    print ("\nTest de cv_systus_med_31 :")
#
    VERBOSE = True
    D_CORRES_TYPE = cv_systus_med_30 (VERBOSE)
#
# ==============================================================
#
    print ("\nTest de cv_systus_med_31 :")
#
    VERBOSE = True
    D_NUM_LOCAL = cv_systus_med_31 (VERBOSE)
#
# ==============================================================
#
    break
#
  if not ERREUR :
    print ("Fin normale")

