#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    idx = (0,) + tuple(range(-space_dim, 0, 1))
    NODES = tuple(tuple(map(float, itemgetter(*idx)(line.split()))) for line in NODES[:-1])
    nb_nodes = len(NODES)
    corresponding_nodes = { int(i[0]) : j for j, i in enumerate(NODES)}
    nodes = tuple(coord for node in NODES for coord in node[1:])
        
    # Les elements, triés par dimension
    elements = {}
    corresponding_elements = {}
    max_dim_elements = '0D'
    
    for line in ELEMENTS[:-1] :
        spline = line.split()
        type_element_systus = spline[1]
        element_dim, type_element_aster = get_type_element_code_aster(type_element_systus)
        values = tuple(map(int, spline[:2] + spline[5:]))
        elements_aster = tuple(corresponding_nodes[k] for k in values[2:])

        key = '%dD'%element_dim
        if not key in elements : elements[key] = []
        if not key in corresponding_elements : corresponding_elements[key] = {}
        elements[key].append((type_element_aster, elements_aster))
        corresponding_elements[key][values[0]] = len(corresponding_elements[key])
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

