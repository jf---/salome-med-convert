#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Conversion d'un fichier du format SYSTUS vers le format MED

Copyright EDF 2019
Gérald NICOLAS
+33.1.78.19.43.52
"""
#========================= Les imports - Début ===================================
#

from .logger import logger 

import numpy as np
#
from .util import aggregation_maillage
from .util import cree_maillage_par_niveau_0
from .util import get_caract_mailles
from .util import gettabrecip
from .util import creation_groupe
from .util import print_bilan
#
from .read_asc import read_asc_mesh
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
  :meshmedfile: le maillage total
  """
#
  blabla = "Dans %s.cv_systus_vers_med"%(__name__)
  logger.debug(blabla)
#
  erreur = 0
  message = ""
  meshmedfile = None
#
  while ( not erreur ) :
#
# 1. Exploration des données
#
    erreur, message, d_nro_section, maillage_nom, sdim, nbr_entites, coordinates, tb_renum_node, tb_renum_elem, tb_type_elem = cv_systus_med_1 ( les_lignes, verbose, verbose_max )
    if erreur:
      break
#
# 2. Bilan
#
    nbr_mailles_dim = print_bilan ( sdim, nbr_entites, verbose_max )
#
# 3. Création des maillages par niveau
#
    erreur, message, le_maillage_niveau, d_niveau = cv_systus_med_2 ( les_lignes, d_nro_section, maillage_nom, sdim, nbr_entites, nbr_mailles_dim, coordinates, tb_renum_node, tb_type_elem, verbose, verbose_max )
    if erreur:
      break
#
# 4. Création du contenu des groupes
#
    d_groupes = cv_systus_med_3 ( les_lignes, d_niveau, verbose, verbose_max )
#
# 5. Aggrégation des maillages
#
    meshmedfile = aggregation_maillage ( le_maillage_niveau, d_groupes, verbose_max )
#
#
    break
#
#
  return erreur, message, meshmedfile
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
  

  blabla = "Dans %s.cv_systus_med_1"%(__name__)
  logger.debug(blabla)

  logger.debug(blabla)
#
  erreur = 0
  message = ""
  sdim = np.inf
  nbr_entites = dict()
  coordinates = None
  tb_renum_node = None
  tb_renum_elem = None
  tb_type_elem = None
#
  while ( not erreur ) :
#
# 1. Le nom du maillage
#
    maillage_nom = les_lignes[1].strip()[:-1]
    logger.debug("... maillage_nom = '%s'" % maillage_nom)

    if ( len(maillage_nom) == 0 ):
      maillage_nom = "MAILLAGE"
      texte = "Attention : le nom de maillage est absent dans ce fichier."
      texte += " On impose le nom '%s'" % maillage_nom
      logger.debug(texte)
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
    texte = "\n.. Dimension d'espace : %d" % sdim
    logger.debug(texte)
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
  blabla = "Dans %s.cv_systus_med_1_r"%(__name__)
  logger.debug(blabla)
#
  erreur = 0
  message = ""
#
  while not erreur:
#
# 1. Les lignes de début de section et de fin des sections
#    Remarque : on n'utilise pas la fonction index car on ne sait pas comment est gérée la fin de ligne
#
    d_nro_section = dict()
#
    for iaux, ligne in enumerate(les_lignes) :
#
# 1.1. Stockage du numéro de ligne pour chaque début et fin de rubrique
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
#
# 1.2. Tout est trouvé
#
      if ( len(d_nro_section) == 6 ) :
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

    logger.debug("d_nro_section :")
    for la_cle in d_nro_section:
      logger.debug("%s : %s"%(la_cle, d_nro_section[la_cle]))
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

  blabla = "Dans %s.cv_systus_med_1_n"%(__name__)
  logger.debug(blabla)


# 1. Nombre de noeuds
#
  nbr_noeuds = ifin - ideb
  logger.debug(".. Nombre de noeuds : %d" % nbr_noeuds)

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
  texte = "... Plus petit numéro de noeud : %8d\n" % tb_renum_node.min()
  texte += "... Plus grand numéro de noeud : %8d" % tb_renum_node.max()
  logger.debug(texte)
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

  blabla = "Dans %s.cv_systus_med_1_e"%(__name__)
  logger.debug(blabla)

#
# 1. Nombre d'éléments
#
  nbr_entites["Elements"] = ifin - ideb
  logger.debug(".. Nombre d'éléments : %d" % nbr_entites["Elements"])

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

  texte = "... Plus petit numéro d'éléments : %8d\n" % tb_renum_elem.min()
  texte += "... Plus grand numéro d'éléments : %8d" % tb_renum_elem.max()
  for type_maille in caract_maille:
    texte += "\n... Nombre d'éléments pour le type '%5s' : %8d" % (type_maille,nbr_entites[type_maille])
  logger.debug(texte)

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
  :d_niveau: dictionnaire de la dimension par niveau
  """

  blabla = "Dans %s.cv_systus_med_2"%(__name__)
  logger.debug(blabla)

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
    d_corres_type, num_local_dans_med = cv_systus_med_20 (verbose_max)
#
# 3. Le tableau réciproque de la numérotation des noeuds
#
    d_tab_recip = gettabrecip (tb_renum_node)
#
# 3. Les maillages par niveau
#
    le_maillage_niveau = dict()
    d_niveau = dict()
#
    niveau = 1
    for ndim in range (sdim, 0, -1 ) :
#
      if ( nbr_mailles_dim[ndim] > 0 ) :
#
        texte = "\n.. Création du maillage de dimension %d" % ndim
        texte += " sous le nom '%s'" % maillage_nom
        logger.debug(texte)
#
        if ( niveau > 0 ) :
          niveau = 0
        d_niveau[niveau] = ndim
#
# 3.1. Création de la structure du maillage
#
        cree_maillage_par_niveau_0 ( maillage_nom, niveau, ndim, les_coords, nbr_mailles_dim, le_maillage_niveau, verbose_max )
#
# 3.2. Ajout des mailles du niveau
#
        cv_systus_med_2_0 ( les_lignes[d_nro_section["l_be"]+1:], d_corres_type, num_local_dans_med, ndim, le_maillage_niveau[niveau], tb_type_elem, d_tab_recip, verbose_max )
#
# 3.3. Reordonnancement des mailles par type
#
        _ = le_maillage_niveau[niveau].sortCellsInMEDFileFrmt()
        #tb_o2n = le_maillage_niveau[niveau].sortCellsInMEDFileFrmt()
#
      if ( niveau <= 0 ) :
        niveau -= 1
#
#
    break
#
  return erreur, message, le_maillage_niveau, d_niveau
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def cv_systus_med_2_0 ( les_lignes, d_corres_type, num_local_dans_med, ndim, mail_du_niveau, tb_type_elem, d_tab_recip, verbose=False ) :
  """Ajout des mailles dans le maillage d'un niveau

Entrées:
  :les_lignes: les lignes du fichier à convertir - pour les éléments
  :d_corres_type: dictionnaire de la correspondance
    . clé : le type SYSTUS
    . valeur : (la dimension, le nombre de noeuds, le type medcoupling)
  :num_local_dans_med: dictionnaire de la correspondance de numérotation locale
    . clé : le type medcoupling
    . valeur : liste de la position locale dans la convention MED pour chaque position SYSTUS
  :ndim: dimension du maillage
  :tb_type_elem: tableau de typage des éléments
  :d_tab_recip: tableau réciproque de la renumérotation des noeuds
Entrées/Sorties :
  :mail_du_niveau: le maillage à compléter
  """

  blabla = "Dans %s.cv_systus_med_2_0"%(__name__)
  logger.debug(blabla)
 
#
  texte = "\n... Dimension %d" % ndim
  logger.debug(texte)

#
  tb_nodes = np.zeros(27, dtype=np.int32)
#
# 1. Pour tous les éléments :
#    On filtre sur la bonne dimension
#
  for iaux, t_element in enumerate(tb_type_elem):
#
    if ( d_corres_type[t_element][0] == ndim ):
#
      nbn = d_corres_type[t_element][1]
      type_med = d_corres_type[t_element][2]
#
# 1.1. La liste des noeuds dans la numérotation SYSTUS
#
      laux = les_lignes[iaux].split()
#
# 1.2. La liste des noeuds dans la numérotation MED
#
      for jaux, n_systus in enumerate(laux[-nbn:]):
        tb_nodes[num_local_dans_med[type_med][jaux]] = d_tab_recip[int(n_systus)]

#
# 1.3. Insertion des noeuds dans le maillage medcoupling
#
      mail_du_niveau.insertNextCell(type_med, nbn, ml.DataArrayInt(tb_nodes))
#
# 2. Finalisation des insertions
#
  mail_du_niveau.finishInsertingCells()
#
  return
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def cv_systus_med_20 ( verbose=False ) :
  """Correspondance entre le type SYSTUS et le type mecoupling

Entrées:
Sorties :
  :d_corres_type: dictionnaire de la correspondance
    . clé : le type SYSTUS
    . valeur : (la dimension, le nombre de noeuds, le type medcoupling)
  :num_local_dans_med: dictionnaire de la correspondance de numérotation locale
    . clé : le type medcoupling
    . valeur : liste de la position locale dans la convention MED pour chaque position SYSTUS
  """

  blabla = "Dans %s.cv_systus_med_20"%(__name__)
  logger.debug(blabla)
  
#
# 1. Correspondance entre le type SYSTUS et le type mecoupling
#
  d_corres_type = cv_systus_med_200 ( verbose )
#
# 2. Correspondance entre la numérotation locale SYSTUS et celle de mecoupling
#
  num_local_dans_med = cv_systus_med_201 ( verbose )
#
  return d_corres_type, num_local_dans_med
#
#===========================  Fin de la fonction =================================
#
#=========================== Début de la fonction ================================
#
def cv_systus_med_200 ( verbose=False ) :
  """Correspondance entre le type SYSTUS et le type mecoupling

Entrées:
Sorties :
  :d_corres_type: dictionnaire de la correspondance
    . clé : le type SYSTUS
    . valeur : (la dimension, le nombre de noeuds, le type medcoupling)
  """

  blabla = "Dans %s.cv_systus_med_200"%(__name__)
  logger.debug(blabla)
  
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

  texte  = "d_corres_type :"
  for cle in d_corres_type:
    texte += "\n%4d : dimension = %2d, nombre de noeuds = %2d, type medcoupling = %d" % (cle, d_corres_type[cle][0], d_corres_type[cle][1], d_corres_type[cle][2])
  logger.debug(texte)
#
  return d_corres_type
#
#
#=========================== Début de la fonction ================================
#
def cv_systus_med_201 ( verbose=False ) :
  """Correspondance entre la numérotation locale SYSTUS et celle de mecoupling

Remarque : on préserve les orientations des mailles

Entrées:
Sorties :
  :num_local_dans_med: dictionnaire de la correspondance de numérotation locale
    . clé : le type medcoupling
    . valeur : liste de la position locale dans la convention MED pour chaque position SYSTUS
  """

  
  blabla = "Dans %s.cv_systus_med_201"%(__name__)
  logger.debug(blabla)

#
  num_local_dans_med = dict()
#
# 1. Mailles 0D
#
  num_local_dans_med[ml.NORM_POINT1] = [0]
#
# 2. Mailles 1D
#
  num_local_dans_med[ml.NORM_SEG2] = [0, 1]
#
  num_local_dans_med[ml.NORM_SEG3] = [0, 2, 1]
#
# 3. Mailles 2D
#
  num_local_dans_med[ml.NORM_TRI3] = [0, 1, 2]
  num_local_dans_med[ml.NORM_QUAD4] = [0, 1, 2, 3]
#
  num_local_dans_med[ml.NORM_TRI6] = [0, 3, 1, 4, 2, 5]
  num_local_dans_med[ml.NORM_QUAD8] = [0, 4, 1, 5, 2, 6, 3, 7]
#
# 4. Mailles 3D
#
  num_local_dans_med[ml.NORM_TETRA4] = [0, 2, 1, 3]
  num_local_dans_med[ml.NORM_HEXA8] = [0, 3, 2, 1,   4, 7, 6, 5]
  num_local_dans_med[ml.NORM_PYRA5] = list()
  num_local_dans_med[ml.NORM_PENTA6] = [0, 2, 1,   3, 5, 4]
#
  num_local_dans_med[ml.NORM_TETRA10] = [ 0,  6,  2,  5,  1,  4,    7,  9,  8,   3 ]
  num_local_dans_med[ml.NORM_HEXA20] = [ 0, 11, 3, 10, 2, 9, 1, 8,   16, 19, 18, 17,   4, 15, 7, 14, 6, 13, 5, 12 ]
  num_local_dans_med[ml.NORM_PYRA13] = list()
  num_local_dans_med[ml.NORM_PENTA15] = [ 0, 8, 2, 7, 1, 6,   12, 14, 13,   3, 11, 5, 10, 4, 9]
#

  texte  = "num_local_dans_med :"
  logger.debug(texte)
  for cle in num_local_dans_med:
    logger.debug("%2d : %s"%(cle, num_local_dans_med[cle]))
  
  return num_local_dans_med
#
#=========================== Début de la fonction ================================
#
def cv_systus_med_3 ( les_lignes, d_niveau, verbose, verbose_max ) :
  """Création des groupes

Entrées:
  :les_lignes: les lignes du fichier à convertir
  :d_niveau: dictionnaire de la dimension par niveau
Sorties :
  :d_groupes: dictionnaire des groupes par niveau
  """

  blabla = "Dans %s.cv_systus_med_3"%(__name__)
  logger.debug(blabla)
  

# 1. Récupération des groupes du point de vue de SYSTUS
#  d_gr_elements : dictionnaire des groupes d'éléments en SYSTUS
#    . clé : dimension sous forme "nD"
#    . valeur : dictionnaire des groupes pour la dimension concernée :
#      . clé : nom du groupe
#      . valeur : liste des numéros des noeuds
#  d_gr_noeuds : dictionnaire des groupes de noeuds en SYSTUS
#    . clé : nom du groupe
#    . valeur : liste des numéros des noeuds
#
  _, _, _, _, d_gr_elements, d_gr_noeuds = read_asc_mesh (les_lignes)
#
# 2. Exploration de chaque niveau pour les groupes d'éléments
#
  d_groupes = dict()
#
  for niveau in d_niveau:
#
    d_groupes[niveau] = list()
#
    ndim = "%dD" % d_niveau[niveau]
#
    if ndim in d_gr_elements:
#
      for group_n, l_elem in d_gr_elements[ndim].items():
#
#       Création du DataArrayInt pour ce groupe d'élément
#       et stockage dans d_groupes
#
        creation_groupe (group_n, l_elem, niveau, d_groupes, verbose)
#
# 3. Les groupes de noeuds
#
  d_groupes[1] = list()
#
  for group_n, l_elem in d_gr_noeuds.items():
#
#   Création du DataArrayInt pour ce groupe de noeuds
#   et stockage dans d_groupes
#
    creation_groupe (group_n, l_elem, 1, d_groupes, verbose)
#
#
  return d_groupes
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
    print ("Test de cv_systus_med_201 :")
#
    VERBOSE = True
    D_CORRES_TYPE = cv_systus_med_200 (VERBOSE)
#
# ==============================================================
#
    print ("Test de cv_systus_med_201 :")
#
    VERBOSE = True
    D_NUM_LOCAL = cv_systus_med_201 (VERBOSE)
#
# ==============================================================
#
    break
#
  if not ERREUR :
    print ("Fin normale")
