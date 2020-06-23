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

class MedConverterError(Exception):
    "Base class for exceptions raised by the medconverter module."
    pass

class ConnectivityRenumberer:

    # Les items d'une liste indiquent à quelle position MED se trouve le noeud SYSTUS correspondant à l'index dans la liste.
    # e.g. pour le QUAD8 :
    # Le noeud 0 SYSTUS correspond au noeud 0 MED
    # Le noeud 1 SYSTUS correspond au noeud 4 MED
    # Le noeud 2 SYSTUS correspond au noeud 1 MED
    # Le noeud 3 SYSTUS correspond au noeud 5 MED
    # Le noeud 4 SYSTUS correspond au noeud 2 MED
    # Le noeud 5 SYSTUS correspond au noeud 6 MED
    # Le noeud 6 SYSTUS correspond au noeud 3 MED
    # Le noeud 7 SYSTUS correspond au noeud 7 MED

    _systus = {
        'POINT1'  : [0],

        'SEG2'    : [0, 1],
        'TRI3'    : [0, 1, 2],
        'QUAD4'   : [0, 1, 2, 3],
        'TETRA4'  : [0, 2, 1, 3],
        'HEXA8'   : [0, 3, 2, 1,   4, 7, 6, 5],
        'PYRA5'   : [0, 3, 2, 1, 4],
        'PENTA6'  : [0, 2, 1,   3, 5, 4],

        'SEG3'    : [0, 2, 1],
        'TRI6'    : [0, 3, 1, 4, 2, 5],
        'QUAD8'   : [0, 4, 1, 5, 2, 6, 3, 7],
        'TETRA10' : [0,  6,  2,  5,  1,  4,   7,  9,  8,   3],
        'HEXA20'  : [0, 11, 3, 10, 2, 9, 1, 8,   16, 19, 18, 17,   4, 15, 7, 14, 6, 13, 5, 12 ],
        'PYRA13'  : [0, 8, 3, 7, 2, 6, 1, 5,   9, 12, 11, 10,   4],
        'PENTA15' : [0, 8, 2, 7, 1, 6,   12, 14, 13,   3, 11, 5, 10, 4, 9]
    }

    _abaqus = {
        'POINT1'  : [0],

        'SEG2'    : range(2),
        'SEG3'    : [0, 2, 1],

        'TRI3'    : range(3),
        'TRI6'    : range(6),

        'QUAD4'   : range(4),
        'QUAD8'   : range(8),
        'QUAD9'   : range(9),

        'TETRA4'  : [0, 2, 1, 3],
        'TETRA10' : [0, 2, 1, 3, 6, 5, 4, 7, 9, 8],

        'HEXA8'   : [0, 3, 2, 1, 4, 7, 6, 5],
        'HEXA20'  : [0, 3, 2, 1, 4, 7, 6, 5, 11, 10, 9, 8, 15, 14, 13, 12, 16, 19, 18, 17],
        'HEXA27'  : [0, 3, 2, 1, 4, 7, 6, 5, 11, 10, 9, 8, 15, 14, 13, 12, 16, 19, 18, 17, 26, 20, 25, 24, 23, 22, 21],

        'PENTA6'  : [0, 2, 1, 3, 5, 4],
        'PENTA15' : [0, 2, 1, 3, 5, 4, 8, 7, 6, 11, 10, 9, 12, 14, 13],
        'PENTA18' : [0, 2, 1, 3, 5, 4, 8, 7, 6, 11, 10, 9, 12, 14, 13, 17, 16, 15],

        'PYRA5' : [0, 3, 2, 1, 4],
        'PYRA13' : [0, 3, 2, 1, 4, 8, 7, 6, 5, 9, 12, 11, 10],

    }

    _aster = {
        'POINT1'  : [0],

        'SEG2'    : range(2),
        'TRI3'    : range(3),
        'QUAD4'   : range(4),
        'TETRA4'  : [0, 2, 1, 3],
        'HEXA8'   : [0, 3, 2, 1, 4, 7, 6, 5],
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

    _med_types = 'POINT1 SEG2 TRI3 QUAD4 TETRA4 HEXA8 PYRA5 PENTA6 SEG3 TRI6 QUAD8 TETRA10 HEXA20 PYRA13 PENTA15 SEG4 TRI7 QUAD9 PENTA18 HEXA27'.split()

    def __init__(self, code):

        self._connectivity_med_to_external = {}
        self._connectivity_external_to_med = {}

        try :
            connectivity = getattr(self, '_{}'.format(code.lower()))
            assert set(connectivity.keys()) <= set(self._med_types)

            for elem, nodes in connectivity.items() :
                elem_mc = getattr(medcoupling, 'NORM_%s'%elem)
                self._connectivity_med_to_external[elem_mc] = OrderedDict()
                self._connectivity_external_to_med[elem_mc] = OrderedDict()
                tmp = {}

                for i, val in enumerate(nodes) :
                    tmp[val] = i
                    self._connectivity_med_to_external[elem_mc][i] = val
                for i in sorted(tmp) :
                    self._connectivity_external_to_med[elem_mc][i] = tmp[i]

        except AttributeError:
            raise MedConverterError('Unknown connectivity {}'.format(code))

    def external_to_medcoupling(self, medcoupling_type, nodes):
        try :
            return tuple(nodes[self._connectivity_external_to_med[medcoupling_type][i]] for i in self._connectivity_external_to_med[medcoupling_type])
        except KeyError :
            raise MedConverterError('Unsupported element type %s'%medcoupling_type)

    def medcoupling_to_external(self, medcoupling_type, nodes):
        try :
            return tuple(nodes[self._connectivity_med_to_external[medcoupling_type][i]] for i in self._connectivity_med_to_external[medcoupling_type])
        except KeyError :
            raise MedConverterError('Unsupported element type %s'%medcoupling_type)


class ElementTypeConverter:

    _systus_to_med = {
        '001' : 'POINT1',

        '102' : 'SEG2',
        '203' : 'TRI3',
        '204' : 'QUAD4',
        '304' : 'TETRA4',
        '308' : 'HEXA8',
        '305' : 'PYRA5',
        '306' : 'PENTA6',

        '103' : 'SEG3',
        '206' : 'TRI6',
        '208' : 'QUAD8',
        '310' : 'TETRA10',
        '320' : 'HEXA20',
        '313' : 'PYRA13',
        '315' : 'PENTA15',
    }

    _abaqus_to_med = OrderedDict((
       ('Node', 'POINT1'),

# Frame Element
       ('FRAME2D', 'SEG2'),
       ('FRAME3D', 'SEG2'),

# Elbow Element
       ('ELBOW31', 'SEG2'),
       ('ELBOW32', 'SEG3'),
       ('ELBOW31B', 'SEG2'),
       ('ELBOW31C', 'SEG2'),

# Diffusive heat transfer elements
       ('DC1D2', 'SEG2'),
       ('DC1D3', 'SEG3'),

# Forced convection heat transfer element
       ('DCC1D2' , 'SEG2'),
       ('DCC1D2D', 'SEG2'),

# Coupled thermal-electrical elements
       ('DC1D2E', 'SEG2'),
       ('DC1D3E', 'SEG3'),

# Axis symmetric thermal element
       ('DCCAX4', 'QUAD4'),

# Acoustic element
       ('AC1D2', 'SEG2'),
       ('AC1D3', 'SEG3'),

# Beam element
       ('B21', 'SEG2'),
       ('B22', 'SEG3'),
       ('B23', 'SEG2'),

       ('B21H', 'SEG2'),
       ('B22H', 'SEG3'),
       ('B23H', 'SEG2'),

       ('B31', 'SEG2'),
       ('B32', 'SEG3'),
       ('B33', 'SEG2'),

       ('B31H', 'SEG2'),
       ('B32H', 'SEG3'),
       ('B33H', 'SEG2'),

# PIPE element
       ('PIPE21', 'SEG2'),
       ('PIPE22', 'SEG3'),

       ('PIPE21H', 'SEG2'),
       ('PIPE22H', 'SEG3'),

       ('PIPE31', 'SEG2'),
       ('PIPE32', 'SEG3'),

       ('PIPE31H', 'SEG2'),
       ('PIPE32H', 'SEG3'),

# Membrane Element
       ('M3D3', 'TRI3'),
       ('M3D4', 'QUAD4'),
       ('M3D6', 'TRI6'),
       ('M3D8', 'QUAD8'),
       ('M3D9', 'QUAD9'),

       ('MAX1', 'SEG2'),
       ('MAX2', 'SEG3'),

       ('MGAX1', 'SEG2'),
       ('MGAX2', 'SEG3'),

# Reduced Structural Element
       ('S3R', 'TRI3'),
       ('S3RS', 'TRI3'),

       ('S4R', 'QUAD4'),
       ('S4RS', 'QUAD4'),
       ('S4R5', 'QUAD4'),
       ('S4RSW', 'QUAD4'),

       ('S8R', 'QUAD8'),
       ('S8RS', 'QUAD8'),

       ('S9R5', 'QUAD9'),

# Structural Element
       ('S3', 'TRI3'),
       ('S4', 'QUAD4'),

# Reduced Continuum Element
       ('CPE4R', 'QUAD4'),
       ('CPE4RH', 'QUAD4'),
       ('CPE8R', 'QUAD8'),
       ('CPE8RH', 'QUAD8'),

       ('CPS4R', 'QUAD4'),
       ('CPS8R', 'QUAD8'),

       ('C3D8R', 'HEXA8'),
       ('C3D8RH', 'HEXA8'),
       ('C3D20R', 'HEXA20'),
       ('C3D20RH', 'HEXA20'),
       ('C3D27R', 'HEXA27'),
       ('C3D27RH', 'HEXA27'),

# Plane strain element
       ('CPE3', 'TRI3'),
       ('CPE6', 'TRI6'),

       ('CPE4', 'QUAD4'),
       ('CPE8', 'QUAD8'),
       ('CPE9', 'QUAD9'),

       ('CPE3H', 'TRI3'),
       ('CPE6H', 'TRI6'),

       ('CPE4H', 'QUAD4'),
       ('CPE8H', 'QUAD8'),
       ('CPE9H', 'QUAD9'),

       ('CPE6M', 'TRI6'),
       ('CPE6MH', 'TRI6'),

       ('CPE4I', 'QUAD4'),
       ('CPE4IH', 'QUAD4'),

# Plane stress element
       ('CPS3', 'TRI3'),
       ('CPS6', 'TRI6'),
       ('CPS6M', 'TRI6'),

       ('CPS4', 'QUAD4'),
       ('CPS4I', 'QUAD4'),
       ('CPS8', 'QUAD8'),

# Axi element
       ('CAX3', 'TRI3'),
       ('CAX6', 'TRI6'),

       ('CAX4', 'QUAD4'),
       ('CAX8', 'QUAD8'),
       ('CAX9', 'QUAD9'),

       ('CAX3H', 'TRI3'),
       ('CAX6H', 'TRI6'),

       ('CAX4H', 'QUAD4'),
       ('CAX8H', 'QUAD8'),
       ('CAX9H', 'QUAD9'),

       ('CAX6M', 'TRI6'),
       ('CAX6MH', 'TRI6'),

       ('CAX4I', 'QUAD4'),
       ('CAX4IH', 'QUAD4'),
       ('CAX4R', 'QUAD4'),
       ('CAX4RH', 'QUAD4'),
       ('CAX8R', 'QUAD8'),
       ('CAX8RH', 'QUAD8'),

# Continuum Element - Hybrid element
       ('C3D4H', 'TETRA4'),
       ('C3D10H', 'TETRA10'),
       ('C3D10M', 'TETRA10'),
       ('C3D10MH', 'TETRA10'),

       ('C3D5H', 'PYRA5'),
       ('C3D13H', 'PYRA13'),

       ('C3D6H', 'PENTA6'),
       ('C3D15H', 'PENTA15'),
       ('C3D15VH', 'PENTA18'),

       ('C3D8I', 'HEXA8'),
       ('C3D8IH', 'HEXA8'),
       ('C3D8H', 'HEXA8'),
       ('C3D20H', 'HEXA20'),
       ('C3D27H', 'HEXA27'),

# Continuum Element, must be declared last
       ('C3D4', 'TETRA4'),
       ('C3D10', 'TETRA10'),

       ('C3D5', 'PYRA5'),
       ('C3D13', 'PYRA13'),

       ('C3D6', 'PENTA6'),
       ('C3D15', 'PENTA15'),
       ('C3D15V', 'PENTA18'),

       ('C3D8', 'HEXA8'),
       ('C3D20', 'HEXA20'),
       ('C3D27', 'HEXA27'),
    ))

    _aster_to_med = {
        'POI1'   : 'POINT1',

        'SEG2'   : 'SEG2',
        'TRIA3'  : 'TRI3',
        'QUAD4'  : 'QUAD4',
        'TETRA4' : 'TETRA4',
        'HEXA8'  : 'HEXA8',
        'PYRAM5' : 'PYRA5',
        'PENTA6' : 'PENTA6',

        'SEG3'   : 'SEG3',
        'TRIA6'  : 'TRI6',
        'QUAD8'  : 'QUAD8',
        'TETRA10': 'TETRA10',
        'HEXA20' : 'HEXA20',
        'PYRAM13': 'PYRA13',
        'PENTA15': 'PENTA15',

        'SEG4'   : 'SEG4',
        'TRIA7'  : 'TRI7',
        'QUAD9'  : 'QUAD9',
        'PENTA18': 'PENTA18',
        'HEXA27' : 'HEXA27',
    }

    _med_types = 'POINT1 SEG2 TRI3 QUAD4 TETRA4 HEXA8 PYRA5 PENTA6 SEG3 TRI6 QUAD8 TETRA10 HEXA20 PYRA13 PENTA15 SEG4 TRI7 QUAD9 PENTA18 HEXA27'.split()

    def __init__(self, code):
        self.code = code.lower()

        try :
            data = getattr(self, '_{}_to_med'.format(self.code))
        except AttributeError :
            raise MedConverterError("Unknown format '{}'".format(code))

        assert set(data.values()) <= set(self._med_types)
        mdata = {i : getattr(medcoupling, 'NORM_%s'%k) for i, k in data.items()}

        self._external_to_medcoupling = {i : k for i, k in mdata.items()}
        self._medcoupling_to_external = {k : i for i, k in mdata.items()}

        if 'systus' in self.code:
            self._f_e2m = self._systus_to_mc
            self._f_m2e = self._mc_to_systus
        else :
            self._f_e2m = self._to_mc
            self._f_m2e = self._to_ext


    def external_to_medcoupling(self, external_type):
        return self._f_e2m(external_type)

    def medcoupling_to_external(self, medcoupling_type):
        return self._f_m2e(medcoupling_type)

    # Specific functions
    def _systus_to_mc(self, systus_type):
        dim, nb_nodes = systus_type[0], systus_type[-2:]
        return self._to_mc(''.join((dim, nb_nodes)))

    def _mc_to_systus(self, medcoupling_type):
        item = self._to_ext(medcoupling_type)
        return '0'.join((item[0], item[1:]))

    # Generic functions
    def _to_mc(self, external_type):
        try :
            return self._external_to_medcoupling[external_type]
        except KeyError:
            raise MedConverterError("{} type '{}' unknown.".format(*(self.code.title(), external_type)))

    def _to_ext(self, medcoupling_type):
        try :
            return self._medcoupling_to_external[medcoupling_type]
        except KeyError:
            raise MedConverterError("MedCoupling type '{}' unknown.".format(medcoupling_type))



class MedConverter:

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
        raise MedConverterError(msg)

    def read_med_mesh(self, filename):
        logger.debug("Reading Med mesh file : %s"%filename)
        self.medmesh = MEDFileUMesh(filename)

    def write_med_mesh(self, filename):
        logger.debug("Writing Med mesh file : %s"%filename)
        self.medmesh.write(filename, 2)

    def create_med_mesh(self):
        coords = medcoupling.DataArrayDouble(self.nodes, len(self.nodes)//self.space_dim, self.space_dim)

        self.medmesh = MEDFileUMesh()

        # Les clés de elements correspondent aux dimensions dans le maillage
        for i, dim in enumerate(sorted(self.elements.keys())[::-1]) :
            level = -1*i

            mesh_at_current_level = MEDCouplingUMesh(self.mesh_name, int(dim[0]))
            mesh_at_current_level.setCoords(coords)
            number_of_elements_at_level = len(self.elements[dim])
            mesh_at_current_level.allocateCells(number_of_elements_at_level)

            # Elements par niveau, avec renumerotation au passage
            for (medcoupling_type, element_nodes_med) in self.elements[dim]:

                number_of_nodes_current_element = MEDCouplingUMesh.GetNumberOfNodesOfGeometricType(medcoupling_type)
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
        self.medmesh.setName(self.mesh_name[0:63])
        self.medmesh.rearrangeFamilies()
