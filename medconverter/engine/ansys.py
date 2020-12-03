#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os.path as osp
from operator import itemgetter
import medcoupling
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
        c = MedConverterAnsys()
        c.read_ansys_mesh(filename_ansys)
        c.create_med_mesh()
        c.write_med_mesh(filename_med)

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
                    print(line.split(","))
                    IndexElem.append(line.split(",")[2])
                    ElemAnsys.append(int(line.split(",")[1]))

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
        flag = {'Nb_nodes' : 0}
        drapeau = 0
        for line in ELEMENTS[:-2] :
            if flag['Nb_nodes'] is 0:
                spline=line.split() 
                idx_element_ansys = int(spline[10])
                valeur=[]
                i=0
                indicecorrespondance=None
                elemvirtuel=int(spline[1])
                for elem in ElemAnsys:
                    if elemvirtuel==elem:
                        indicecorrespondance=i
                    i +=1
                if indicecorrespondance==None:
                    print("Element not found")
                element1=IndexElem[indicecorrespondance].replace("\n","")
                element=element1.replace(" ","") 
                element_ansys_type=element   
                nombre_noeud_elem=int(ELEMENTS[0].split()[8])
                if nombre_noeud_elem<=8 :
                    if '184' in element_ansys_type :
                        None
                    elif '288' or '289' or '188' or '189' in element_ansys_type :
                        valeur8=spline[11:]
                        if '188' in element_ansys_type and len(valeur8)==3 :
                            valeur8=spline[11:-1]
                        if '288' in element_ansys_type and len(valeur8)==3 :
                            valeur8=spline[11:-1]
                        if '189' in element_ansys_type and len(valeur8)==4 :
                            valeur8=spline[11:-1]
                        if '189' in element_ansys_type and len(valeur8)==4 :
                            valeur8=spline[11:-1]
                        valeursplit=[]
                        valeursansdoublon=[]
                        for elem in valeur8 :
                            valeursplit.append(int(elem))
                        for i in valeursplit:
                            if i not in valeursansdoublon:
                                valeursansdoublon.append(i)    
                        elements_nodes_ansys = list(map(int, valeursansdoublon))
                        element_ansys_type = element_ansys_type + '_' + str(len(elements_nodes_ansys))
                        element_medcoupling_type = e_conv.external_to_medcoupling(element_ansys_type)
                        element_nodes_med = c_renum.external_to_medcoupling(element_medcoupling_type, elements_nodes_ansys)
                        
                        self.add_cell(idx_element_ansys, element_medcoupling_type, element_nodes_med)
                      
                    else :
                        valeur8=spline[11:]
                        valeursplit=[]
                        valeursansdoublon=[]
                        for elem in valeur8 :
                            valeursplit.append(int(elem))
                        for i in valeursplit:
                            if i not in valeursansdoublon:
                                valeursansdoublon.append(i)    
                        elements_nodes_ansys = list(map(int, valeursansdoublon))
                        element_ansys_type = element_ansys_type + '_' + str(len(elements_nodes_ansys))
                        element_medcoupling_type = e_conv.external_to_medcoupling(element_ansys_type)          
                        element_nodes_med = c_renum.external_to_medcoupling(element_medcoupling_type, elements_nodes_ansys)

                        self.add_cell(idx_element_ansys, element_medcoupling_type, element_nodes_med)

                else :
                    for elem in spline[11:]:
                        valeur.append(int(elem))
                    drapeau = 1    
            else :
                spline=line.split()
                for elem in spline :
                    valeur.append(int(elem))
                    
                element_ansys_type = element
                valeursansdoublon=[]
                for i in valeur:
                        if i not in valeursansdoublon:
                            valeursansdoublon.append(i)
                elements_nodes_ansys = list(map(int, valeursansdoublon)) 
                element_ansys_type = element_ansys_type + '_' + str(len(elements_nodes_ansys))    
                element_medcoupling_type = e_conv.external_to_medcoupling(element_ansys_type)
                element_nodes_med = c_renum.external_to_medcoupling(element_medcoupling_type, elements_nodes_ansys)

                self.add_cell(idx_element_ansys, element_medcoupling_type, element_nodes_med)

                drapeau =0
                
            if drapeau == 1 :
                flag['Nb_nodes']=1 
            elif drapeau == 0 :
                flag['Nb_nodes']=0   

            #print("Le type de l'element est : %s" %(element_ansys_type))
            #print("Les valeurs sont : %s" %(spline[11:]))   
        tocc = time.perf_counter()
        logger.debug("-> Adding internal cells in %0.4f seconds"%(tocc-ticc))
        print("fait2")
        
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
                        valeur=abs(int(splinevalues[j]))
                        valeurgroupe.append(valeur)
                values =  map(int, valeurgroupe)

                if group_tag_ansys == 'NODE' :
                    self.add_group_nodes(group_name, values)
                else :
                    self.add_group_cells(group_name, values)

            compteur +=1 
        print("fait3")
        tocc = time.perf_counter()
        logger.debug("-> Adding internal groups in %0.4f seconds"%(tocc-ticc))

        # Finish by renumbering
        #ticc = time.perf_counter()
        #self.mesh.renumbering()
        #tocc = time.perf_counter()
        #logger.debug("-> Renumbering in %0.4f seconds"%(tocc-ticc))

        toc = time.perf_counter()
        logger.debug("End creating internal mesh in %0.4f seconds"%(toc-tic))
        print("Lecture complete") 
		
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
   
