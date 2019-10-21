#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import logging
import os.path as osp
from operator import itemgetter
from collections import OrderedDict
from time import strftime

import medcoupling
from MEDLoader import *
from .logger import logger

class ConnectivityRenumberer:

    # Les chiffres des listes indiquent à quelle position SYSTUS se trouve le noeud MED à l'index.
    # e.g. pour le QUAD8 :
    # Le noeud 0 MED correspond au noeud 0 SYSTUS
    # Le noeud 1 MED correspond au noeud 4 SYSTUS
    # Le noeud 2 MED correspond au noeud 1 SYSTUS
    # Le noeud 3 MED correspond au noeud 5 SYSTUS
    # Le noeud 4 MED correspond au noeud 2 SYSTUS
    # Le noeud 5 MED correspond au noeud 6 SYSTUS
    # Le noeud 6 MED correspond au noeud 3 SYSTUS
    # Le noeud 7 MED correspond au noeud 7 SYSTUS

    _systus = {
        'POINT1'     : [0],
        
        'SEG2'    : [0, 1],
        'TRI3'    : [0, 1, 2],
        'QUAD4'   : [0, 1, 2, 3],
        'TETRA4'  : [0, 2, 1, 3],
        'HEXA8'   : [0, 3, 2, 1,   4, 7, 6, 5],
        #'PYRA5'   : [],
        'PENTA6'  : [0, 2, 1,   3, 5, 4],

        'SEG3'    : [0, 2, 1],
        'TRI6'    : [0, 3, 1, 4, 2, 5],
        'QUAD8'   : [0, 4, 1, 5, 2, 6, 3, 7],
        'TETRA10' : [0,  6,  2,  5,  1,  4,    7,  9,  8,   3 ],
        'HEXA20'  : [0, 11, 3, 10, 2, 9, 1, 8,   16, 19, 18, 17,   4, 15, 7, 14, 6, 13, 5, 12 ],
        #'PYRA13'  : [],
        'PENTA15' : [0, 8, 2, 7, 1, 6,   12, 14, 13,   3, 11, 5, 10, 4, 9]
    }

    def __init__(self, code):

        self._connectivity_med_to_external = {}
        self._connectivity_external_to_med = {}

        try : 
            connectivity = getattr(self, '_{}'.format(code.lower()))
            for elem, nodes in connectivity.items() :

                self._connectivity_med_to_external[elem] = OrderedDict()

                self._connectivity_external_to_med[elem] = OrderedDict()
                tmp = {}

                for i, val in enumerate(nodes) :
                    tmp[val] = i 
                    self._connectivity_med_to_external[elem][i] = val
                for i in sorted(tmp) :
                    self._connectivity_external_to_med[elem][i] = tmp[i]
                
        except AttributeError:
            raise
            raise KeyError('Unknown connectivity {}'.format(code))


    def external_to_med(self, elem_type, nodes):
        try :
            return tuple(nodes[self._connectivity_external_to_med[elem_type][i]] for i in self._connectivity_external_to_med[elem_type])
        except KeyError :
            raise KeyError('Unsupported element type %s'%elem_type)
    def med_to_external(self, elem_type, nodes):
        try :
            return tuple(nodes[self._connectivity_med_to_external[elem_type][i]] for i in self._connectivity_med_to_external[elem_type])
        except KeyError :
            raise KeyError('Unsupported element type %s'%elem_type)

class ElementTypeConverter:
    _systus_to_med = {
        '001' : (1,  'POINT1',  0),
        
        '102' : (2,  'SEG2',    1),
        '203' : (3,  'TRI3',    2),
        '204' : (4,  'QUAD4',   2),
        '304' : (4,  'TETRA4',  3),
        '308' : (8,  'HEXA8',   3),
        '305' : (5,  'PYRA5',   3),
        '306' : (6,  'PENTA6',  3),

        '103' : (3,  'SEG3',    1),
        '206' : (6,  'TRI6',    2), 
        '208' : (8,  'QUAD8',   2), 
        '310' : (10, 'TETRA10', 3),
        '320' : (20, 'HEXA20',  3),
        '313' : (13, 'PYRA13',  3),
        '315' : (15, 'PENTA15', 3),
    } 
    _med_to_systus = {item[1] : (item[0], '0'.join((i[0], i[1:])), item[2]) for i, item in _systus_to_med.items()}
    _med_to_medcoupling = { item[1] : (item[0], getattr(medcoupling, 'NORM_%s'%item[1]), item[2]) for item in _systus_to_med.values()}
    
    def systus_to_med_type(self, systus_type):
        try :
            dim, nb_nodes = systus_type[0], systus_type[-2:]
            key = ''.join((dim, nb_nodes))
            return self._systus_to_med[key]

        except KeyError:
            raise KeyError("Systus type '{}' unknown.".format(systus_type))

    def med_to_systus_type(self, med_type):
        try :
            return self._med_to_systus[med_type]
        except KeyError:
            raise KeyError("Med type '{}' unknown.".format(med_type))

    def med_to_medcoupling_type(self, med_type):
        try :
            return self._med_to_medcoupling[med_type]
        except KeyError:
            raise KeyError("Med type '{}' unknown.".format(med_type))
        

class MedConvert:

    def __init__(self):
        self.mesh_name = None
        self.space_dim = None
        self.nodes = None
        self.elements = {}
        self.groups_e = {}
        self.groups_n = {}

        self.verbose = False
        
        self.medmesh = None

    def _get_file_encoding(self, filename):

        encodings = 'utf8 latin_1 cp437'.split()
        
        for enc in encodings :
            try :
                with open(filename, mode = 'r', encoding = enc) as f : f.read()
                return enc
            except UnicodeDecodeError as err:
                continue
        
        msg = "File encoding is not among : %s"%(', '.join(encodings))
        raise UnicodeError(msg)
    
    def read_med_mesh(self, filename):
        logger.debug("Reading Med mesh file : %s"%filename)
        self.medmesh = MEDFileUMesh(filename)

    def write_med_mesh(self, filename):
        logger.debug("Writing Med mesh file : %s"%filename)
        self.medmesh.write(filename, 2)
                
    def create_med_mesh(self):

        coords = medcoupling.DataArrayDouble(self.nodes, len(self.nodes)//self.space_dim, self.space_dim)

        self.medmesh = MEDFileUMesh()

        c_renum = ConnectivityRenumberer('SYSTUS')
        e_conv = ElementTypeConverter()

        # Les clés de elements correspondent aux dimensions dans le maillage
        for i, dim in enumerate(sorted(self.elements.keys())[::-1]) :
            level = -1*i

            mesh_at_current_level = MEDCouplingUMesh(self.mesh_name, int(dim[0]))
            mesh_at_current_level.setCoords(coords)
            number_of_elements_at_level = len(self.elements[dim])
            mesh_at_current_level.allocateCells(number_of_elements_at_level)

            # Elements par niveau, avec renumerotation au passage
            for (med_type, element_nodes_asc) in self.elements[dim]:

                number_of_nodes_current_element, medcoupling_type, element_dim = e_conv.med_to_medcoupling_type(med_type)
                element_nodes_med = c_renum.external_to_med(med_type, element_nodes_asc)
                mesh_at_current_level.insertNextCell(medcoupling_type, number_of_nodes_current_element , element_nodes_med)

            mesh_at_current_level.finishInsertingCells()
            sort_order = mesh_at_current_level.sortCellsInMEDFileFrmt()
            sort_dict = {idx : item for idx, item in enumerate(sort_order.getValues())}
            mesh_at_current_level.checkConsistencyLight()
            self.medmesh.setMeshAtLevel(level, mesh_at_current_level)

            # Groupes d'elements par niveau
            try :
                groups_e_at_level = []
                for group_name, group_elements in self.groups_e[dim].items():
                    sorted_group = tuple(sort_dict[item] for item in group_elements)
                    group_medcoupling = medcoupling.DataArrayInt(sorted_group)
                    group_medcoupling.setName(group_name)
                    groups_e_at_level.append(group_medcoupling)
                self.medmesh.setGroupsAtLevel(level, groups_e_at_level)
            except KeyError :
                # On peut ne pas avoir de groupes de mailles d'une certaine dimension
                pass

        # Groupes de noeuds
        groups_n_at_level = []
        for group_name, group_nodes in self.groups_n.items():
            group_medcoupling = medcoupling.DataArrayInt(group_nodes)
            group_medcoupling.setName(group_name)
            groups_n_at_level.append(group_medcoupling)
        self.medmesh.setGroupsAtLevel(1, groups_n_at_level) # Groupes de noeuds au niveau 1

        self.medmesh.setName(self.mesh_name)
        self.medmesh.rearrangeFamilies()
        
    

class MedConvertSystus(MedConvert):

    @staticmethod
    def convert_systus_to_med(filename_systus, filename_med, verbose = False):
        if verbose : logger.setLevel(logging.DEBUG)
        c = MedConvertSystus()
        c.read_systus_mesh(filename_systus)
        c.create_med_mesh()
        c.write_med_mesh(filename_med)
    
    @staticmethod
    def convert_med_to_systus(filename_med, filename_systus, verbose = False):
        if verbose : logger.setLevel(logging.DEBUG)
        c = MedConvertSystus()
        c.read_med_mesh(filename_med)
        c.create_systus_mesh()
        c.write_systus_mesh(filename_systus)
        
    def __init__(self):
        super(MedConvertSystus, self).__init__()
        self.systusmesh = None
        
    def read_systus_mesh(self, filename):
        logger.debug("Reading SYSTUS mesh file : %s"%filename)
        
        NODES, ELEMENTS, GROUPS = [], [], []

        flag = {'NODES' : 0,
                'ELEMENTS' : 0,
                'GROUPS' : 0
            }

        # Lecture du fichier .ASC où les blocs sont separés par des BEGIN_* et END_*
        with open(filename, 'r', encoding = self._get_file_encoding(filename)) as f :
            next(f) 

            # Lecture du nom du maillage si disponible
            line_1 = next(f).strip()
            # self.mesh_name = line_1 if line_1 else 'Mesh'
            self.mesh_name = line_1 if line_1 else osp.splitext(osp.split(filename)[-1])[0]
            
            for line in f :

                if flag['NODES'] is 1 : NODES.append(line)
                elif flag['ELEMENTS'] is 1 : ELEMENTS.append(line)
                elif flag['GROUPS'] is 1 : GROUPS.append(line)

                if "BEGIN_NODES" in line :
                    flag['NODES'] = 1
                    self.space_dim = int(line.split()[2])
                elif "END_NODES"  in line :
                    flag['NODES'] =  0

                elif "BEGIN_ELEMENTS" in line :
                    flag['ELEMENTS'] = 1
                elif "END_ELEMENTS"   in line :
                    flag['ELEMENTS'] = 0

                elif "BEGIN_GROUPS" in line :
                    flag['GROUPS'] = 1
                elif "END_GROUPS"   in line :
                    flag['GROUPS'] = 0

        logger.debug("Mesh name : %s"%self.mesh_name)
        logger.debug("Space Dimension : %d"%self.space_dim)
        logger.debug("Number of nodes : %d"%(len(NODES)-1))
        logger.debug("Number of elements : %d"%(len(ELEMENTS)-1))
        logger.debug("Number of groups : %d"%(len(GROUPS)-1))

        # Les noeuds du maillage
        iter_idx = (int(line.split()[0]) for line in NODES[:-1])
        corresponding_nodes = { item : i for i, item in enumerate(iter_idx)}

        idx_coords = tuple(range(-self.space_dim, 0, 1))
        iter_nodes = ((map(float, itemgetter(*idx_coords)(line.split()))) for line in NODES[:-1])
        self.nodes = tuple(coord for node in iter_nodes for coord in node)

        # Les elements, triés par dimension
        corresponding_elements = {}
        max_dim_elements = '0D'
        e_conv = ElementTypeConverter()

        for line in ELEMENTS[:-1] :
            spline = line.split()
            idx_element_systus = int(spline[0])
            element_systus_type = spline[1]
            elements_nodes_systus = map(int, spline[5:])

            _, element_med_type, element_dim = e_conv.systus_to_med_type(element_systus_type)
            elements_nodes_med = tuple(corresponding_nodes[k] for k in elements_nodes_systus)

            key = '%dD'%element_dim
            if not key in self.elements : self.elements[key] = []
            if not key in corresponding_elements : corresponding_elements[key] = {}
            self.elements[key].append((element_med_type, elements_nodes_med))
            corresponding_elements[key][idx_element_systus] = len(corresponding_elements[key])
            max_dim_elements = max(max_dim_elements, key)

        # Les groups, triés par dimension
        for line in GROUPS[:-1] :
            spline = line.split()
            values =  map(int, line.split('"')[-1].split())
            group_name = spline[1]
            group_tag_systus = spline[2]

            if group_tag_systus == '1' :
                self.groups_n[group_name] = tuple(corresponding_nodes[k] for k in values)

            else :
                for element_systus in values :
                    for key in self.elements.keys():
                        if element_systus in corresponding_elements[key]:
                            if not key in self.groups_e : self.groups_e[key] = {}
                            if not group_name in self.groups_e[key]:  self.groups_e[key][group_name] = []
                            self.groups_e[key][group_name].append(corresponding_elements[key][element_systus])

            
    def write_systus_mesh(self, filename):
        logger.debug("Writing SYSTUS mesh file : %s"%filename)
        with open(filename, 'w') as f : f.write(self.systusmesh)
        
    def create_systus_mesh(self):

        mesh_name = self.medmesh.getName()
        groups_names = self.medmesh.getGroupsNames()
        mesh_dim = self.medmesh.getMeshDimension()

        # Noeuds
        coords = self.medmesh.getCoords()
        space_dim = self.medmesh.getSpaceDimension()
        nb_nodes = len(coords)
        nodes_shift = 1 # La numérotation SYSTUS des noeuds démarre à 1
        nodes_lines = ('%d 0 0 0 0 0 '%(i+nodes_shift) + ' '.join(map(str,node)) for i, node in enumerate(coords))

        # Elements et groupes
        elements_lines = []
        groups_lines = []
        groups_e_ids = {}
        groups_n_ids = {}
        cells_shift = 1 # La numérotation SYSTUS des éléments démarre à 1. De plus la numérotation MED est compacte par niveau. On se servira de cette variable pour créer une numérotation globale

        c_renum = ConnectivityRenumberer('SYSTUS')
        e_conv = ElementTypeConverter()
        non_empty_levs = self.medmesh.getNonEmptyLevels()
        for lev in non_empty_levs:
            mesh_lev = self.medmesh[lev]
            j = 0 # Un index pour compter les cells par niveau
            types_at_level = mesh_lev.getAllGeoTypesSorted()
            for a_type in types_at_level :
                nb_nodes_per_cell = MEDCouplingUMesh.GetNumberOfNodesOfGeometricType(a_type)
                med_type = MEDCouplingUMesh.GetReprOfGeometricType(a_type).split('NORM_')[-1]
                _, systus_type, _ = e_conv.med_to_systus_type(med_type)
                cells_by_type = mesh_lev.giveCellsWithType(a_type).getValues()
                for cell in cells_by_type :
                    element_nodes_med = DataArrayInt(mesh_lev.getNodeIdsOfCell(cell)) + nodes_shift
                    element_nodes_asc = c_renum.med_to_external(med_type, element_nodes_med)
                    elements_lines.append('%d %s 1 0 0 '%(j+cells_shift, systus_type) + ' '.join(map(str,element_nodes_asc)))
                    j+=1
                 
            groups_e_at_level = self.medmesh.getGroupsOnSpecifiedLev(lev)
            for group in groups_e_at_level :
                ids = cells_shift + self.medmesh.getGroupArr(lev, group)
                # Gestion des groupes sur plusierus niveaux
                if group in groups_e_ids :
                    groups_e_ids[group].append(ids.getValues())
                else:
                    groups_e_ids[group] = ids.getValues()

            cells_shift+=mesh_lev.getNumberOfCells() # Pour créer une numérotation globale

        groups_n = self.medmesh.getGroupsOnSpecifiedLev(1)
        for group in groups_n :
            ids = nodes_shift + self.medmesh.getGroupArr(1, group)
            groups_n_ids[group] = ids.getValues()

        nb_elements = cells_shift-1

        id_groups = 1 # La numérotation des groupes systus est incrementale et commune à tout type de groupe
        for name in sorted(groups_e_ids.keys()) :
            group_e = groups_e_ids[name]
            group_line = '%d %s 2 0 "PART_ID %d" "" "" %s'%(id_groups, name, id_groups, ' '.join(map(str, group_e)))
            id_groups+=1
            groups_lines.append(group_line)

        for name in sorted(groups_n_ids.keys()) :
            group_n = groups_n_ids[name]
            group_line = '%d %s 1 0 "COLLECTOR_ID %d" "" "" %s'%(id_groups, name, id_groups, ' '.join(map(str, group_n)))
            id_groups+=1
            groups_lines.append(group_line)
        nb_groups = id_groups-1


        # Entete du fichier
        txt_header = """1VSD 0 {0} {0}
{1}
 100000 4 {2} {3} 0 3 6 0 0
BEGIN_INFORMATIONS
{1}
 4 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 3 3 9 0 0 0 0 9 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0
END_INFORMATIONS
""".format(*[strftime("%y%m%d %H%M%S"), mesh_name, nb_nodes, nb_elements])

        txt_nodes = "BEGIN_NODES %d %d\n%s\nEND_NODES\n"%(nb_nodes, space_dim, '\n'.join(nodes_lines))
        txt_elements = "BEGIN_ELEMENTS %d\n%s\nEND_ELEMENTS\n"%(nb_elements, '\n'.join(elements_lines))
        txt_groups = "BEGIN_GROUPS %d\n%s\nEND_GROUPS\n"%(nb_groups, '\n'.join(groups_lines)) if groups_lines else ''
        self.systusmesh = ''.join((txt_header, txt_nodes, txt_elements, txt_groups))
