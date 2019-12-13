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
        'POINT1'  : [0],
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

    _abaqus = {
        'POINT1'  : [0],
        'SEG2'    : [0, 1],
        'QUAD4'   : [0, 1, 2, 3],
    }

    _aster = {
        'POINT1'  : [0],
        
        'SEG2'    : range(2), 
        'TRI3'    : range(3), 
        'QUAD4'   : range(4), 
        'TETRA4'  : [0, 2, 1, 3],
        'HEXA8'   : [0,  3,  2,  1,  4,  7,  6,  5],
        'PYRA5'   : [0, 3, 2, 1, 4],
        'PENTA6'  : [0, 2, 1, 3, 5, 4],

        'SEG3'    : range(3),  
        'TRI6'    : range(6),  
        'QUAD8'   : range(8),  
        'TETRA10' : [0, 2, 1, 3, 6, 5, 4, 7, 9, 8],
        'HEXA20'  : [0, 3, 2, 1, 4, 7, 6, 5, 11, 10, 9, 8, 16, 19, 18, 17, 15, 14, 13, 12],
        'PYRA13'  : [0, 3, 2, 1, 4, 8, 7, 6, 5, 9, 12, 11, 10],
        'PENTA15' : [0, 2, 1, 3, 5, 4, 8, 7, 6, 12, 14, 13, 11, 10, 9],


        'SEG4'    : range(4), 
        'TRI7'    : range(7),  
        'QUAD9'   : range(9),  
        'PENTA18' : [0, 2, 1, 3, 5, 4, 8, 7, 6, 12, 14, 13, 11, 10, 9, 17, 16, 15],
        'HEXA27'  : [0, 3, 2, 1, 4, 7, 6, 5, 11, 10, 9, 8, 16, 19, 18, 17, 15, 14, 13, 12, 20, 24, 23, 22, 21, 25, 26],

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

    _abaqus_to_med = {
        'Node' : (1,  'POINT1',  0),

        'S4' : (4,  'QUAD4',   2),
    }

    _aster_to_med = {
        'POI1'   : (1,  'POINT1',  0),
        
        'SEG2'   : (2,  'SEG2',    1),
        'TRIA3'  : (3,  'TRI3',    2),
        'QUAD4'  : (4,  'QUAD4',   2),
        'TETRA4' : (4,  'TETRA4',  3),
        'HEXA8'  : (8,  'HEXA8',   3),
        'PYRAM5' : (5,  'PYRA5',   3),
        'PENTA6' : (6,  'PENTA6',  3),
        
        'SEG3'   : (3,  'SEG3',    1),
        'TRIA6'  : (6,  'TRI6',    2), 
        'QUAD8'  : (8,  'QUAD8',   2), 
        'TETRA10': (10, 'TETRA10', 3),
        'HEXA20' : (20, 'HEXA20',  3),
        'PYRAM13': (13, 'PYRA13',  3),
        'PENTA15': (15, 'PENTA15', 3),

        'SEG4'   : (4,  'SEG4',    1),
        'TRIA7'  : (7,  'TRI7',    2), 
        'QUAD9'  : (9,  'QUAD9',   2),
        'PENTA18': (18, 'PENTA15', 3),
        'HEXA27' : (27, 'HEXA27',  3), 

    }

    _med_to_systus = {item[1] : (item[0], '0'.join((i[0], i[1:])), item[2]) for i, item in _systus_to_med.items()}

    _med_to_abaqus = {item[1] : (item[0], i, item[2]) for i, item in _aster_to_med.items()}

    _med_to_aster  = {item[1] : (item[0], i, item[2]) for i, item in _aster_to_med.items()}

    _med_to_medcoupling = { item[1] : (item[0], getattr(medcoupling, 'NORM_%s'%item[1]), item[2]) for item in _aster_to_med.values()}


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

    def abaqus_to_med_type(self, abaqus_type):
        try :
            return self._abaqus_to_med[abaqus_type]

        except KeyError:
            raise KeyError("Abaqus type '{}' unknown.".format(abaqus_type))

    def med_to_abaqus_type(self, med_type):
        try :
            return self._med_to_abaqus[med_type]
        except KeyError:
            raise KeyError("Med type '{}' unknown.".format(med_type))

    def aster_to_med_type(self, aster_type):
        try :
            return self._aster_to_med[aster_type]
        except KeyError:
            raise KeyError("Aster type '{}' unknown.".format(aster_type))

    def med_to_aster_type(self, med_type):
        try :
            return self._med_to_aster[med_type]
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

    def create_med_mesh(self, input_type):
        coords = medcoupling.DataArrayDouble(self.nodes, len(self.nodes)//self.space_dim, self.space_dim)

        self.medmesh = MEDFileUMesh()

        c_renum = ConnectivityRenumberer(input_type)
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
