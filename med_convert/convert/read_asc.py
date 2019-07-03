import os.path as osp
import numpy as np
from operator import itemgetter
from time import time
from glob import glob

def read_asc_mesh(filename):

    with open(mesh) as f :
        lines = f.readlines()

    NODES, ELEMENTS, GROUPS = [], [], []

    flag = {'NODES' : 0,
            'ELEMENTS' : 0,
            'GROUPS' : 0
        }

    for line in lines :
        if flag['NODES'] == 1 : NODES.append(line)
        if flag['ELEMENTS'] == 1 : ELEMENTS.append(line)
        if flag['GROUPS'] == 1 : GROUPS.append(line)

        key = 'NODES'
        if "BEGIN_%s"%key in line :
            flag[key]+=1
            sdim = int(line.split()[2])
        if "END_%s"%key  in line : flag[key]-=1

        for key in ('ELEMENTS', 'GROUPS'):
            if "BEGIN_%s"%key in line : flag[key]+=1
            if "END_%s"%key   in line : flag[key]-=1


    idx = list(range(-sdim, 0, 1))
    NODES = [[i] + [int(item.split()[0])] + list(map(float ,list(itemgetter(*idx)(item.split())))) for i, item in enumerate(NODES[:-1])]

    ALL_ELEMENTS = [list(map(int, item.split()[:2] + item.split()[5:])) for item in ELEMENTS[:-1]]
    ELEMENTS = {'1D' : [],
                '2D' : [],
                '3D' : [],
            }
    
    for item in ALL_ELEMENTS :
        edim = int(str(item[1])[0])
        if edim == 1 :
            ELEMENTS['1D'].append([len(ELEMENTS['1D'])] + item)
        elif edim == 2 :
            ELEMENTS['2D'].append([len(ELEMENTS['2D'])] + item)
        elif edim == 3 :
            ELEMENTS['3D'].append([len(ELEMENTS['3D'])] + item)
        else :
            raise ValueError(edim)
    
    GROUPS_N = [[item.split()[1]] + [int(i) for i in item.split()[4:] if i.isdigit()] for item in GROUPS[:-1] if int(item.split()[2]) == 1]
    ALL_GROUPS_E = [[item.split()[1]] + [int(i) for i in item.split()[4:] if i.isdigit()] for item in GROUPS[:-1] if int(item.split()[2]) == 2]

    corr_nodes = { i[1] : i[0] for i in NODES}
    corr_elements = { dim : { i[1] : i[0] for i in ELEMENTS[dim]} for dim in ELEMENTS.keys()}

    GROUPS_E = {'1D' : [],
                '2D' : [],
                '3D' : [],
            }
    
    for item in ALL_GROUPS_E :
        if item[1] in corr_elements['1D'].keys():
            GROUPS_E['1D'].append(item)
        elif item[1] in corr_elements['2D'].keys():
            GROUPS_E['2D'].append(item)
        elif item[1] in corr_elements['3D'].keys():
            GROUPS_E['3D'].append(item)
        else :
            raise ValueError(item[1])

    nodes = np.array(NODES)[:,2:]

    elements = {}
    for dim, element in ELEMENTS.items() :
        elements[dim] = {}
        for item in element :
            element_type = asso_elem(item[2])[1]
            if not element_type in elements[dim] : elements[dim][element_type] = []
            elements[dim][element_type].append(tuple(corr_nodes[k] for k in item[3:]))
            
            
    groups_n = { item[0] : list(corr_nodes[k] for k in item[2:])  for item in GROUPS_N }
    groups_e = {dim : {item[0] : list(corr_elements[dim][k] for k in item[1:]) for item in group} for dim, group in GROUPS_E.items()}

    return nodes, elements, groups_e, groups_n

def asso_elem(code_systus):
    
    sdim, nb_nodes = int(str(code_systus)[0]), int(str(code_systus)[-2:])

    if sdim == 3 and nb_nodes == 20:
        code_aster = 'HEXA20'
    elif sdim == 3 and nb_nodes == 15:
        code_aster = 'PENTA15'
    elif sdim == 1 and nb_nodes == 2:
        code_aster = 'SEG2'
    elif sdim == 1 and nb_nodes == 3:
        code_aster = 'SEG3'
    elif sdim == 2 and nb_nodes == 6:
        code_aster = 'TRI6'
    elif sdim == 2 and nb_nodes == 8:
        code_aster = 'QUAD8'
    else :
        raise KeyError(code_systus)
    
    return sdim, code_aster
