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
#========================= Les imports - Début ===================================
#
# Les imports standard
import os
import sys
#
import MEDLoader as ml
#
from systus_vers_med import cv_systus_vers_med
from med_vers_systus import cv_med_vers_systus
#
from util import aggregation_maillage
#
#========================== Les imports - Fin ====================================
#
#=================================== La classe ===================================
#
class ExterneMED (object) :
#
  """Conversion de fichiers entre les formats externe et MED

Options obligatoires
********************
. Type de maillage externe. A choir entre SYSTUS et MESH (INRIA, Paris VI)
--type_externe=["SYSTUS"|"MESH"]

. Type de conversion
--type_cv=[0|1]
    0 : de externe vers MED
    1 : de MED vers externe

Options obligatoires/facultatives
*********************************
Si conversion d'un format externe vers MED :
. Nom du fichier au format externe.
--ficexterne=ficexterne

. Nom du fichier au format MED à convertir. Par défaut, ce nom est le même que celui au format externe.
--ficmed=ficmed

Ou si conversion de MED vers un format externe :
. Nom du fichier au format MED à convertir.
--ficmed=ficmed

. Nom du fichier au format externe. Par défaut, ce nom est le même que celui au format MED.
Le suffixe dépend du type de maillage externe.
--ficexterne=ficexterne

Options facultatives
********************
. La solution à écrire (rien par defaut)
--n_solution : nom du champ à lire dans le fichier MED à convertir
--v_solution : valeur à affecter sur tous les noeuds

. Numéro d'itération si la solution est lue. Par défaut, -1.
--num_iter=num_iter

. Numéro d'ordre si la solution est lue. Par défaut, -1.
--num_ordre=num_ordre

Exemple :
ExterneMED(["--type_externe=SYSTUS", "--type_cv=0", "--ficexterne=/home/D68518/MAILLAGE/SYSTUS/Conversion_Systus_Aster/Maillages/Maillages_Complexes/COUDES/Coude_A_quad_DONN1000.ASC", "-v"])

  """
#
# A. La base
#
  message_info = ""
  _verbose = 0
  _verbose_max = 0
  _affiche_aide_globale = 0
#
# B. Le type de conversion
# B.1. Le type de maillage externe : "SYSTUS", "MESH"
  _type_externe = None
#
# B.2. Le type de conversion
#    0 : de externe vers MED
#    1 : de MED vers externe
  _type_cv = None
#
# C. Les fichiers
#
# . Le fichier med
  _ficmed = None
#
# . Le fichier externe
  _ficexterne = None
#
# D. La solution
  _solution = None
  _num_iter  = -1
  _num_ordre = -1
#
# E. Variables utiles
# Nombre de noeuds
  nbr_noeuds = 0
# sdim : dimension d'espace
  sdim = 0
# level_a: niveau pour les arêtes
# level_f: niveau pour les faces
  #level_a = np.inf
  #level_f = np.inf
#
#=========================== Début de la méthode =================================
#
  def __init__ ( self, liste_option ) :
#
    """Le constructeur de la classe ExterneMED

Décodage des arguments
On cherche ici les arguments généraux : aide, verbeux
Le reste est stocké dans une liste qui sera décodée plus tard en tant que de besoin
    """
#
    l_arg = list()
#
    for option in liste_option :
#
      #print (option)
      saux = option.upper()
      if saux in ( "-H", "-HELP" ) :
        self._affiche_aide_globale = 1
      elif saux == "-V" :
        self._verbose = 1
      elif saux == "-VMAX" :
        self._verbose = 1
        self._verbose_max = 1
      else :
        l_arg.append(option)
#
    self.commande_arg = l_arg
#
#===========================  Fin de la méthode ==================================
#
#=========================== Début de la méthode =================================
#
  def __del__(self):
    """A la suppression de l'instance de classe"""
    if self._verbose_max :
      print("Suppression de l'instance de la classe.")
#
#===========================  Fin de la méthode ==================================
#
#=========================== Début de la méthode =================================
#
  def _arguments (self) :
    """Décodage des arguments de cette commande

Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
    """
#
# 1. Préalables
#
    nom_fonction = __name__ + "/_arguments"
    blabla = "\nDans " + nom_fonction
    if self._verbose_max :
      print (blabla)
#
    if self._verbose_max :
      print ("arguments :", self.commande_arg)
#
    erreur = 0
    message = ""
#
    while not erreur :
#
# 2. Les arguments specifiques de la commande
#
      for argu in self.commande_arg :
#
        #print ("\n", argu)
        l_aux = argu.split("=")
        #print (l_aux)
        if ( len(l_aux) == 2 ) :
          if l_aux[0] == "--type_externe" :
            self._type_externe = l_aux[1]
          elif l_aux[0] == "--type_cv" :
            self._type_cv = int(l_aux[1])
          elif l_aux[0] == "--ficmed" :
            self._ficmed = l_aux[1]
          elif l_aux[0] == "--ficexterne" :
            self._ficexterne = l_aux[1]
          elif l_aux[0] == "--n_solution" :
            self._solution = l_aux[1]
          elif l_aux[0] == "--v_solution" :
            self._solution = float(l_aux[1])
          elif l_aux[0] == "--num_iter" :
            self._num_iter = int(l_aux[1])
          elif l_aux[0] == "--num_ordre" :
            self._num_ordre = int(l_aux[1])
        else :
          pass
#
# 3. Controle
#
      erreur, message = self._controle_arguments ()
#
      break
#
    return erreur, message
#
#===========================  Fin de la méthode ==================================
#
#=========================== Début de la méthode =================================
#
  def _controle_arguments (self) :
    """Contrôle des arguments

Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
    """
#
# 1. Préalables
#
    nom_fonction = __name__ + "/_controle_arguments"
    blabla = "\nDans " + nom_fonction
    if self._verbose_max :
      print (blabla)
#
    if self._verbose_max :
      print ("arguments :", self.commande_arg)
#
    erreur = 0
    message = ""
#
    while not erreur :
#
      texte = ""
#
# 2. Le type de conversion
#
      texte += "Format externe : %s\n" % self._type_externe
      if ( self._type_externe not in ("SYSTUS", "MESH") ):
        texte += "Ce type de format externe est inconnu."
        erreur = 2
        break
#
# 3. Le type de conversion
#
      if ( self._type_cv == 0 ):
        texte += "Conversion du format %s vers MED" % self._type_externe
      elif ( self._type_cv == 1 ):
        texte += "Conversion de MED vers le format %s" % self._type_externe
      else:
        texte += "Ce type de conversion est inconnu : "
        if isinstance(self._type_cv, int):
          texte += "%d" %self._type_cv
        else:
          texte += "%s" % str(self._type_cv)
        erreur = 2
        break
#
# 4. Controle des fichiers
#
      if ( self._type_cv == 0 ):
#
        if ( self._ficexterne == None ) :
          erreur = 401
        elif ( not os.path.isfile(self._ficexterne) ) :
          message += "\nFichier : %s" % self._ficexterne
          erreur = 402
#
      else:
#
        if ( self._ficmed == None ) :
          erreur = 411
        elif ( not os.path.isfile(self._ficmed) ) :
          message += "\nFichier : %s" % self._ficmed
          erreur = 412
#
      if erreur :
        d_aux = { 0:"externe", 1:"MED" }
        message += "\nFichier %s inconnu." % d_aux[self._type_cv]
        break
#
      break
#
# 5. Informations
#
    if ( erreur or self._verbose_max ) :
      texte += "\n"
      texte += ". ficexterne : %s\n" % self._ficexterne
      texte += ". ficmed    : %s\n" % self._ficmed
      #texte += ". solution  : %s\n" % self._solution
      #texte += ". num_iter  : %d\n" % self._num_iter
      #texte += ". num_ordre : %d" % self._num_ordre
#
    print (texte)
#
    return erreur, message
#
#===========================  Fin de la méthode ==================================
#
#=========================== Début de la méthode =================================
#
  def _cv_maillage ( self ) :
    """Conversion du maillage

Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
    """
#
    nom_fonction = __name__ + "/_cv_maillage"
    blabla = "\nDans %s :\n" % nom_fonction
    if self._verbose_max :
      texte  = blabla
      if self._ficexterne != None :
        texte += ". ficexterne : %s\n" % self._ficexterne
      if self._ficexterne != None :
        texte += ". ficmed     : %s\n" % self._ficmed
      print (texte)
#
# 1. Du format externe externe vers le format MED
#
    if ( self._type_cv == 0 ):
#
      erreur, message = self._cv_externe_vers_med ()
#
# 2. Du format MED vers le format externe
#
    else:
#
      erreur, message = self._cv_med_vers_externe ()
#
    return erreur, message
#
#===========================  Fin de la méthode ==================================
#
#=========================== Début de la méthode =================================
#
  def _cv_externe_vers_med ( self ) :
    """Conversion du maillage du format externe vers MED

Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
    """
#
    nom_fonction = __name__ + "/_cv_externe_vers_med"
    blabla = "\nDans %s :\n" % nom_fonction
    if self._verbose_max :
      texte  = blabla
      texte += ". type_externe : %s\n" % self._type_externe
      print (texte)
#
    erreur = 0
    message = ""
#
    while ( not erreur ) :
#
# 1. Lecture du maillage sous forme de la liste des lignes
#
      texte = "\n. Lecture du fichier :\n%s" % self._ficexterne
      print (texte)
#
      with open (self._ficexterne, "r") as fichier :
        les_lignes = fichier.readlines()
#
# 2. Conversion
# 2.1. A partir de SYSTUS
#
      if ( self._type_externe == "SYSTUS" ):
#
        erreur, message, le_maillage_niveau, d_groupes = cv_systus_vers_med (les_lignes, self._verbose, self._verbose_max)
#
# 2.2. Rien d'autre pour le moment
#
      else:
#
        message = "Le format '%s' n'est pas encore inclus." % self._type_externe
        erreur = 2
        break
#
# 3. Aggrégation du maillage du maillage
#
      meshmedfile = aggregation_maillage (le_maillage_niveau, d_groupes, self._verbose_max)
#
# 4. Ecriture du maillage
#
      texte = "\n. Ecriture du fichier :\n%s" % self._ficmed
      print (texte)
#
      meshmedfile.write(self._ficmed, 2)
#
      break
#
    return erreur, message
#
#===========================  Fin de la méthode ==================================
#
#=========================== Début de la méthode =================================
#
  def _cv_med_vers_externe ( self ) :
    """Conversion du maillage de MED vers le format externe

Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
    """
#
    nom_fonction = __name__ + "/_cv_med_vers_externe"
    blabla = "\nDans %s :\n" % nom_fonction
    if self._verbose_max :
      texte  = blabla
      texte += ". type_externe : %s\n" % self._type_externe
      print (texte)
#
    erreur = 0
    message = ""
#
    while ( not erreur ) :
#
# 1. Lecture du maillage sous forme de structure medcoupling
#
      if self._verbose :
        print (".. Lecture du maillage sur : %s" % self._ficmed)
#
      meshmedfileread = ml.MEDFileMesh.New(self._ficmed)
      if self._verbose_max :
        print (meshmedfileread)
#
# 2. Conversion
# 2.1. Vers SYSTUS
#
      if ( self._type_externe == "SYSTUS" ):
#
        erreur, message, les_lignes = cv_med_vers_systus (meshmedfileread, self._verbose, self._verbose_max)
#
# 2.2. Rien d'autre pour le moment
#
      else:
#
        message = "Le format '%s' n'est pas encore inclus." % self._type_externe
        erreur = 2
        break
#
# 3. Ecriture du maillage
#
      if self._verbose:
        texte = "Ecriture de %s" % self._ficexterne
        print (texte)
#
      with open (self._ficexterne, "w") as fichier :
        fichier.write(les_lignes)
#
      break
#
    return erreur, message
#
#===========================  Fin de la méthode ==================================
#
#=========================== Début de la méthode =================================
#
  def lancement (self) :
#
    """Lancement

Sorties :
  :erreur: code d'erreur
  :message: message d'erreur
    """
#
    nom_fonction = __name__ + "/lancement"
    blabla = "\nDans " + nom_fonction
#
    if self._verbose_max :
      print (blabla)
#
# 1. Préalables
#
    erreur = 0
#
    while not erreur :
#
# 2. Les arguments
#
      erreur, message = self._arguments ()
      if erreur :
        break
      if self._affiche_aide_globale :
        break
#
# 3. La conversion du maillage
#
      erreur, message = self._cv_maillage ()
      if erreur :
        break
#
# 4. La conversion de la solution
#
      #erreur, message = self._cv_solution ()
      #if erreur :
        #break
#
      break
#
# 4. La fin
#
    if ( erreur and self._verbose_max ) :
      print (blabla, message)
#
    return erreur, message
#
#===========================  Fin de la méthode ==================================
#==========================  Fin de la classe ====================================
#
#==================================================================================
# Lancement
#==================================================================================
#
if __name__ == "__main__" :
#
# 1. Options
#
  VERBOSE = 0
  L_OPTIONS = list()
  L_OPTIONS.append("-h")
  if VERBOSE :
    L_OPTIONS.append("-v")
#
# 2. Lancement de la classe
#
  #print ("L_OPTIONS :", L_OPTIONS)
  MED_TO_MESH = ExterneMED(L_OPTIONS)
#
  sys.stdout.write(MED_TO_MESH.__doc__+"\n")
#
  del MED_TO_MESH
#
  sys.exit(0)
