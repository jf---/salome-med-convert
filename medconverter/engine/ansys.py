#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os.path as osp
from operator import itemgetter
from medcoupling import *

from .logger import logger
from .medconverter import MedConverterMesh
from .errors import MedConverterError
from .cells import CellsTypeConverter
from .connectivity import ConnectivityRenumberer

class MedConverterAnsys(MedConverterMesh):

    @staticmethod
    def convert_ansys_to_med(filename_ansys, filename_med, verbose = False):
        if verbose :
            logger.setLevel(logging.DEBUG)
        tic=time.perf_counter()
        c = MedConverterAnsys()
        c.read_ansys_mesh(filename_ansys)
        c.create_med_mesh()
        c.write_med_mesh(filename_med)
        toc=time.perf_counter()
        logger.debug("ANSYS mesh conversion done (in %0.4f seconds)"%(toc-tic))

    @staticmethod
    def convert_med_to_ansys(filename_med, filename_ansys, verbose = False):
        if verbose :
            logger.setLevel(logging.DEBUG)
        c = MedConverterAnsys()
        c.read_med_mesh(filename_med)
        c.create_ansys_mesh()
        c.write_ansys_mesh(filename_ansys)

    def __init__(self):
        super(MedConverterAnsys, self).__init__()
        self.ansysmesh = None

    def read_ansys_mesh(self, filename):
        logger.debug("Reading ANSYS mesh file : %s"%filename)
        NODES, ELEMENTS, GROUPS, IndexElem, ElemAnsys, title  = [], [], [], [], [], [] 

        flag = {'NODES' : 0,
                'ELEMENTS' : 0,
                'GROUPS' : 0,
                'indexElem' : 0,
                'FirstBLOCK' : 0
            }

        # Lecture du fichier .cdb où les blocs sont separés par des BEGIN_* et END_*
        with open(filename, 'r', encoding = self._get_file_encoding(filename)) as f :
            
            for line in f :

                # Gestion d'ajout des lignes
                if flag['NODES'] is 1 : 
                    if "(" in line : None 
                    else : NODES.append(line)
                elif flag['ELEMENTS'] is 1 : 
                    if "(" in line : None 
                    else : ELEMENTS.append(line)

                elif flag['GROUPS'] is 1 : 
                    if "(" in line : None 
                    else : 
                        GROUPS.append(line)

                # création de l'index permettant de faire la correspondance entre 
                # les éléments et leur numéro attribué
                if not "ET, " in line :
                    flag['indexElem'] = 0
                elif 'SET, ' in line :
                    flag['indexElem'] = 0 
                elif "ET, " in line :
                    flag['indexElem'] = 1
                if flag['indexElem'] is 1 :
                    IndexElem.append(line.split(",")[2])
                    ElemAnsys.append(int(line.split(",")[1]))

                # Gestion des drapeaux
                if "NBLOCK" in line :
                    flag['NODES'] = 1
                    dim = int(line.split(",")[1])
                    self.space_dim = dim-3
                elif "N,"  in line :
                    flag['NODES'] =  0

                elif "EBLOCK" in line :
                    flag['ELEMENTS'] = 1
                elif "CMBLOCK"   in line :
                    flag['ELEMENTS'] = 0
                    flag['GROUPS'] = 1
                    if flag['FirstBLOCK'] is 0:
                        GROUPS.append(line)
                        flag['FirstBLOCK'] = 1  

                elif "MPTEMP," in line :
                    flag['GROUPS'] = 0
                    flag['ELEMENTS'] = 0

                # Gestion du titre
                elif "/TITLE" in line :
                    title.append(line)

        #Réupération du nom du maillage
        title1 = title[0].split(",")[1]
        title2 = title1.replace(' ', '')
        self.mesh_name = title2.replace("\n", '' ) or osp.splitext(osp.split(filename)[-1])[0]

        logger.debug("Mesh name : %s"%self.mesh_name)
        logger.debug("Space Dimension : %d"%self.space_dim)
        logger.debug("Number of nodes : %d"%(len(NODES)-1))
        logger.debug("Number of elements : %d"%(len(ELEMENTS)-1))
        logger.debug("Number of groups : %d"%(len(GROUPS)-1))

        # Initialise performances
        logger.debug("Creating internal mesh: ")
        tic = time.perf_counter()
        # Les noeuds du maillage
        ticc = time.perf_counter()
       
        for line in NODES[:-1]:
            spline = line.split()
            idx_ansys = int(spline[0])
            coords = tuple(self.splitline(line))
            self.add_node(idx_ansys, coords)
            
        tocc = time.perf_counter()
        logger.debug("-> Adding internal nodes in %0.4f seconds"%(tocc-ticc))

        # Les elements
        ticc = time.perf_counter()
        e_conv = CellsTypeConverter('ANSYS')
        c_renum = ConnectivityRenumberer('ANSYS')
        storeline=[]
        nbligneafaire=1
        for line in ELEMENTS[:-2]:
            spline=line.split()
            storeline.append(spline)
            if len(spline)>=9 and int(spline[9])==0:
                if int(spline[8])<=8:
                    nbligneafaire=1
                else :
                    nbligneafaire=2
            else:
                nbligneafaire=1
            if nbligneafaire==1:
                idx_element_ansys=int(storeline[0][10])
                i=0
                indicecorrespondance=None
                elemvirtuel=int(storeline[0][1])
                for elem in ElemAnsys:
                    if elemvirtuel==elem:
                        indicecorrespondance=i
                    i +=1
                if indicecorrespondance==None:
                    print("Element not found")
                element1=IndexElem[indicecorrespondance].replace("\n","")
                element=element1.replace(" ","")
                element_ansys_type=element
                valeur=[]
                if '184' in element_ansys_type : 
                    storeline=[]
                else :
                    if int(element_ansys_type)==188 and len(storeline[0][11:])==3 :
                        valeur=storeline[0][11:-1]
                    elif int(element_ansys_type)==288 and len(storeline[0][11:])==3 :
                        valeur=storeline[0][11:-1]
                    elif int(element_ansys_type)==189 and len(storeline[0][11:])==4 :
                        valeur=storeline[0][11:-1]
                    elif int(element_ansys_type)==289 and len(storeline[0][11:])==4 :
                        valeur=storeline[0][11:-1]
                    else:
                        if len(storeline)==1:
                            for node in storeline[0][11:]:
                                valeur.append(int(node))
                        else:
                            for node in storeline[0][11:]:
                                valeur.append(int(node))
                            for node2 in storeline[1][:]:
                                valeur.append(int(node2))
                    valeursplit=[]
                    valeursansdoublon=[]
                    for elem in valeur :
                        valeursplit.append(int(elem))
                    for i in valeursplit:
                        if i not in valeursansdoublon:
                            valeursansdoublon.append(i)
                    elements_nodes_ansys = list(map(int, valeursansdoublon))
                    element_ansys_type = element_ansys_type + '_' + str(len(elements_nodes_ansys))
                    element_medcoupling_type = e_conv.external_to_medcoupling(element_ansys_type)
                    element_nodes_med = c_renum.external_to_medcoupling(element_medcoupling_type, elements_nodes_ansys)

                    self.add_cell(idx_element_ansys, element_medcoupling_type, element_nodes_med)
                    storeline=[]
        tocc = time.perf_counter()
        logger.debug("-> Adding internal cells in %0.4f seconds"%(tocc-ticc))

        # Les groups
        ticc = time.perf_counter()
        compteur=0
        for line in GROUPS[:-1] :
            if 'CMBLOCK' in line :
                valeurgroupe=[]
                spline = line.split(",")
                group_name = spline[1]
                group_tag_ansys = spline[2]
                nombre_elemgroup = int(spline[3].split("!")[0])
                quotien=nombre_elemgroup//8
                reste=nombre_elemgroup % 8
                if reste>0 :   
                    nombre_diteration = quotien+1
                else :
                    nombre_diteration = quotien
               
                for i in range((compteur+1),(compteur+nombre_diteration+1)):
                    splinevalues=GROUPS[i].split()
                    for j in range(0,len(splinevalues)):
                        val=int(splinevalues[j])
                        if val<0:
                            if j==0:
                                val1=int(savevalue)+1
                                val2=abs(int(splinevalues[j]))+1
                                for elem in range(val1,val2):
                                    valeurgroupe.append(elem)
                            else:
                                val1=int(splinevalues[j-1])+1
                                val2=abs(int(splinevalues[j]))+1
                                for elem in range(val1,val2):
                                    valeurgroupe.append(elem)
                        else:
                            valeurgroupe.append(val)
                    savevalue=int(splinevalues[-1])
                values =  map(int, valeurgroupe)

                if group_tag_ansys == 'NODE' :
                    self.add_group_nodes(group_name, values)
                else :
                    self.add_group_cells(group_name, values)
            compteur +=1 
        tocc = time.perf_counter()
        logger.debug("-> Adding internal groups in %0.4f seconds"%(tocc-ticc))

        toc = time.perf_counter()
        logger.debug("End creating internal mesh in %0.4f seconds"%(toc-tic))
        logger.debug("End reading ANSYS mesh file") 
		
    def splitline(self, ligne):
        
        coord = []
        floatPremier=0
        floatSecond=0
        floatTroisieme=0
        # le premier decimal commence a la colonne 27 et termine a 48
        strPremier = ligne[27:48]
        try:
            floatPremier = float(strPremier)
        except (ValueError, TypeError):
            floatPremier = float(0)

        strSecond = ligne[48:69]
        try:
            floatSecond = float(strSecond)
        except (ValueError, TypeError):
            floatSecond = float(0)

        strTroisieme = ligne[69:91]           
        try:
            floatTroisieme = float(strTroisieme)
        except (ValueError, TypeError):
            floatTroisieme = float(0)
        
        coord.append(floatPremier)    
        coord.append(floatSecond)
        coord.append(floatTroisieme)
        if len(coord)==2 :
            coord.append(0)
        elif len(coord)==1 :
            coord.append(0)
            coord.append(0)
        return coord
        
    def write_ansys_mesh(self, filename):
        raise NotImplementedError()
    
    def create_ansys_mesh(self):
        raise NotImplementedError()
   
