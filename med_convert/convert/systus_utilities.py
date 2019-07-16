#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path as osp
from operator import itemgetter
from collections import OrderedDict
import medcoupling as mc
from MEDLoader import *
from time import strftime

def systus_to_med_type(systus_type):

    _conv = {
        '001' : 'POI',
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
        '315' : 'PENTA15'
    }

    try :
        dim, nb_nodes = systus_type[0], systus_type[-2:]
        key = ''.join((dim, nb_nodes))
        return int(nb_nodes), _conv[key], int(dim)

    except KeyError:
        raise KeyError("Systus type '{}' unknown.".format(systus_type))
    

def read_systus_mesh(filename):
    
    NODES, ELEMENTS, GROUPS = [], [], []
    
    flag = {'NODES' : 0,
            'ELEMENTS' : 0,
            'GROUPS' : 0
        }

    # Lecture du fichier .ASC où les blocs sont separés par des BEGIN_* et END_*
    with open(filename, 'r') as f :
        next(f)

        # Lecture du nom du maillage si disponible, sinon MAILLAGE
        line_1 = next(f).strip()
        # mesh_name = line_1 if line_1 else 'Mesh'
        mesh_name = line_1 if line_1 else osp.splitext(osp.split(filename)[-1])[0]

        for line in f :

            if flag['NODES'] is 1 : NODES.append(line)
            elif flag['ELEMENTS'] is 1 : ELEMENTS.append(line)
            elif flag['GROUPS'] is 1 : GROUPS.append(line)

            if "BEGIN_NODES" in line :
                flag['NODES'] = 1
                space_dim = int(line.split()[2])
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

    
    # Les noeuds du maillage
    iter_idx = (int(line.split()[0]) for line in NODES[:-1])
    corresponding_nodes = { item : i for i, item in enumerate(iter_idx)}

    idx_coords = tuple(range(-space_dim, 0, 1))
    iter_nodes = ((map(float, itemgetter(*idx_coords)(line.split()))) for line in NODES[:-1])
    nodes = tuple(coord for node in iter_nodes for coord in node)
    
    # Les elements, triés par dimension
    elements = {}
    corresponding_elements = {}
    max_dim_elements = '0D'
    
    for line in ELEMENTS[:-1] :
        spline = line.split()
        idx_element_systus = int(spline[0])
        element_systus_type = spline[1]
        elements_nodes_systus = map(int, spline[5:])

        _, element_med_type, element_dim = systus_to_med_type(element_systus_type)
        elements_nodes_med = tuple(corresponding_nodes[k] for k in elements_nodes_systus)

        key = '%dD'%element_dim
        if not key in elements : elements[key] = []
        if not key in corresponding_elements : corresponding_elements[key] = {}
        elements[key].append((element_med_type, elements_nodes_med))
        corresponding_elements[key][idx_element_systus] = len(corresponding_elements[key])
        max_dim_elements = max(max_dim_elements, key)

    # Les groups, triés par dimension
    groups_n = {}
    groups_e = {}

    for line in GROUPS[:-1] :
        spline = line.split()
        values =  map(int, line.split('"')[-1].split())
        group_name = spline[1]
        group_tag_systus = spline[2]

        if group_tag_systus == '1' :
            groups_n[group_name] = tuple(corresponding_nodes[k] for k in values)

        else :
            for element_systus in values :
                for key in elements.keys():
                    if element_systus in corresponding_elements[key]:
                        if not key in groups_e : groups_e[key] = {}
                        if not group_name in groups_e[key]:  groups_e[key][group_name] = []
                        groups_e[key][group_name].append(corresponding_elements[key][element_systus])

    
    return mesh_name, space_dim, nodes, elements, groups_e, groups_n
