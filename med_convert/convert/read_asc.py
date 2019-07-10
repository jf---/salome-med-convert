#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path as osp
import numpy as np
from operator import itemgetter

def import_asc_mesh(filename):

    with open(filename, 'r') as f :
        lines = f.readlines()

    return read_asc_mesh(lines)
        
def read_asc_mesh(lines):

    # Lecture du nom du maillage si disponible, sinon MAILLAGE
    mesh_name = lines[1].strip() if lines[1].strip() else 'MAILLAGE'

    # Lecture du fichier .ASC où les blocs sont separés par des BEGIN_* et END_*
    NODES, ELEMENTS, GROUPS = [], [], []
    
    flag = {'NODES' : 0,
            'ELEMENTS' : 0,
            'GROUPS' : 0
        }

    for line in lines :
        
        if flag['NODES'] is 1 : NODES.append(line)
        elif flag['ELEMENTS'] is 1 : ELEMENTS.append(line)
        elif flag['GROUPS'] is 1 : GROUPS.append(line)

        if "BEGIN_NODES" in line :
            flag['NODES'] = 1
            mesh_dim = int(line.split()[2])
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
    idx = (0,) + tuple(range(-mesh_dim, 0, 1))
    NODES = tuple(tuple(map(float, itemgetter(*idx)(line.split()))) for line in NODES[:-1])
    corresponding_nodes = { int(i[0]) : j for j, i in enumerate(NODES)}
    nodes = np.array(NODES)[:,1:]
        
    elements = {'1D' : [],
                '2D' : [],
                '3D' : [],
            }
    corresponding_elements = {'1D' : {},
                     '2D' : {},
                     '3D' : {},
                 }

    # Les elements, triés par dimension
    
    for line in ELEMENTS[:-1] :
        spline = line.split()
        type_element_systus = spline[1]
        element_dim, type_element_aster = get_type_element_code_aster(type_element_systus)
        values = tuple(map(int, spline[:2] + spline[5:]))
        elements_aster = tuple(corresponding_nodes[k] for k in values[2:])
        
        if element_dim == 1 :
            elements['1D'].append((type_element_aster, elements_aster))
            corresponding_elements['1D'][values[0]] = len(corresponding_elements['1D'])
        elif element_dim == 2 :
            elements['2D'].append((type_element_aster, elements_aster))
            corresponding_elements['2D'][values[0]] = len(corresponding_elements['2D'])
        elif element_dim == 3 :
            elements['3D'].append((type_element_aster, elements_aster))
            corresponding_elements['3D'][values[0]] = len(corresponding_elements['3D'])
        else :
            raise ValueError(element_dim)

        
    # Les groups, triés par dimension
    groups_n = {}
    groups_e = {'1D' : {},
                '2D' : {},
                '3D' : {},
            }
    
    for line in GROUPS[:-1] :
        spline = line.split()
        values =  map(int, line.split('"')[-1].split())
        group_name = spline[1]
        group_dim = spline[2]

        if group_dim == '1' :
            groups_n[group_name] = tuple(corresponding_nodes[k] for k in values)

        else :
            for element_systus in values :
                if element_systus in corresponding_elements['1D']:
                    if not group_name in groups_e['1D']:  groups_e['1D'][group_name] = []
                    groups_e['1D'][group_name].append(corresponding_elements['1D'][element_systus])
                elif element_systus in corresponding_elements['2D']:
                    if not group_name in groups_e['2D']:  groups_e['2D'][group_name] = []
                    groups_e['2D'][group_name].append(corresponding_elements['2D'][element_systus])
                elif element_systus in corresponding_elements['3D']:
                    if not group_name in groups_e['3D']:  groups_e['3D'][group_name] = []
                    groups_e['3D'][group_name].append(corresponding_elements['3D'][element_systus])
                else :
                    raise ValueError(element_systus)

    
    return mesh_name, mesh_dim, nodes, elements, groups_e, groups_n

def get_type_element_code_aster(type_code_systus):
    dim, nb_nodes = int(str(type_code_systus)[0]), int(str(type_code_systus)[-2:])
   
    if dim == 0 and nb_nodes == 1 :
        type_code_aster = 'POI'
        
    elif dim == 1 and nb_nodes == 2:
        type_code_aster = 'SEG2'
    elif dim == 2 and nb_nodes == 3:
        type_code_aster = 'TRI3'
    elif dim == 2 and nb_nodes == 4:
        type_code_aster = 'QUAD4'   
    elif dim == 3 and nb_nodes == 4:
        type_code_aster = 'TETRA4'
    elif dim == 3 and nb_nodes == 8:
        type_code_aster = 'HEXA8'
    elif dim == 3 and nb_nodes == 5:
        type_code_aster = 'PYRA5'
    elif dim == 3 and nb_nodes == 6:
        type_code_aster = 'PENTA6'


    elif dim == 1 and nb_nodes == 3:
        type_code_aster = 'SEG3'
    elif dim == 2 and nb_nodes == 6:
        type_code_aster = 'TRI6'
    elif dim == 2 and nb_nodes == 8:
        type_code_aster = 'QUAD8'   
    elif dim == 3 and nb_nodes == 10:
        type_code_aster = 'TETRA10'
    elif dim == 3 and nb_nodes == 20:
        type_code_aster = 'HEXA20'
    elif dim == 3 and nb_nodes == 13:
        type_code_aster = 'PYRA13'
    elif dim == 3 and nb_nodes == 15:
        type_code_aster = 'PENTA15'

    else :
        raise KeyError(type_code_systus)
    
    return dim, type_code_aster
