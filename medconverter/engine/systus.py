#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import logging
import os.path as osp
from operator import itemgetter
import medcoupling
from medcoupling import *

from .logger import logger
from .medconverter import MedConverterMesh
from .errors import MedConverterError
from .cells import CellsTypeConverter
from .connectivity import ConnectivityRenumberer

class MedConverterSystus(MedConverterMesh):

    @staticmethod
    def convert_systus_to_med(filename_systus, filename_med, verbose = False):
        if verbose :
            logger.setLevel(logging.DEBUG)
        c = MedConverterSystus()
        c.read_systus_mesh(filename_systus)
        c.create_med_mesh()
        c.write_med_mesh(filename_med)

    @staticmethod
    def convert_med_to_systus(filename_med, filename_systus, verbose = False):
        if verbose :
            logger.setLevel(logging.DEBUG)
        c = MedConverterSystus()
        c.read_med_mesh(filename_med)
        c.create_systus_mesh()
        c.write_systus_mesh(filename_systus)

    def __init__(self):
        super(MedConverterSystus, self).__init__()
        self.systusmesh = None

    def read_systus_mesh(self, filename):
        self._reset_structures()

        NODES, ELEMENTS, GROUPS = [], [], []

        flag = {'NODES' : 0,
                'ELEMENTS' : 0,
                'GROUPS' : 0
            }

        tic = time.perf_counter()
        # Lecture du fichier .ASC où les blocs sont separés par des BEGIN_* et END_*
        with open(filename, 'r', encoding = self._get_file_encoding(filename)) as f :
            line_0 = next(f)

            # Lecture du nom du maillage si disponible
            line_1 = next(f).strip()
            self.mesh_name = line_1 or osp.splitext(osp.split(filename)[-1])[0]

            for line in f :

                if flag['NODES'] is 1 :
                    NODES.append(line)
                elif flag['ELEMENTS'] is 1 :
                    ELEMENTS.append(line)
                elif flag['GROUPS'] is 1 :
                    GROUPS.append(line)

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

        toc = time.perf_counter()

        logger.debug("Reading SYSTUS mesh file : %s (in %0.4f seconds)"%(filename, toc-tic))
        logger.debug("Mesh name : %s"%self.mesh_name)
        logger.debug("Space Dimension : %d"%self.space_dim)
        logger.debug("Number of nodes : %d"%(len(NODES)-1))
        logger.debug("Number of elements : %d"%(len(ELEMENTS)-1))
        logger.debug("Number of groups : %d"%(len(GROUPS)-1))

        # Les noeuds
        tic = time.perf_counter()
        for line in NODES[:-1]:
            spline = line.split()
            idx_systus = int(spline[0])
            coords = tuple(map(float, spline[-self.space_dim:]))
            self.add_node(idx_systus, coords)
        toc = time.perf_counter()
        logger.debug("-> Adding nodes (in %0.4f seconds)"%(toc-tic))
        
        # Les elements
        e_conv = CellsTypeConverter('SYSTUS')
        c_renum = ConnectivityRenumberer('SYSTUS')

        tic = time.perf_counter()
        for line in ELEMENTS[:-1] :
            spline = line.split()
            idx_element_systus = int(spline[0])
            element_systus_type = spline[1]
            elements_nodes_systus = tuple(map(int, spline[5:]))

            element_medcoupling_type = e_conv.external_to_medcoupling(element_systus_type)
            element_nodes_med = c_renum.external_to_medcoupling(element_medcoupling_type, elements_nodes_systus)

            self.add_cell(idx_element_systus, element_medcoupling_type, element_nodes_med)

        toc = time.perf_counter()
        logger.debug("-> Adding cells (in %0.4f seconds)"%(toc-tic))

        tic = time.perf_counter()
        # Les groups
        for line in GROUPS[:-1] :
            spline = line.split()
            values =  map(int, line.split('"')[-1].split())
            group_name = spline[1]
            group_tag_systus = spline[2]

            if group_tag_systus == '1' :
                self.add_group_nodes(group_name, values)
            else :
                self.add_group_cells(group_name, values)
        toc = time.perf_counter()
        logger.debug("-> Adding groups (in %0.4f seconds)"%(toc-tic))
        
    def write_systus_mesh(self, filename):
        logger.debug("Writing SYSTUS mesh file : %s"%filename)
        with open(filename, 'w') as f : f.write(self.systusmesh)

    def create_systus_mesh(self):
        self.systusmesh = None

        # Noeuds
        nb_nodes = len(self.nodes)
        nodes_shift = 1 # La numérotation SYSTUS des noeuds démarre à 1
        nodes_lines = ('%d 0 0 0 0 0 '%(i+nodes_shift) + ' '.join(map(str,node)) for i, node in enumerate(self.nodes))

        # Elements et groupes
        elements_lines = []
        groups_lines = []
        groups_e_ids = {}
        groups_n_ids = {}
        cells_shift = 1 # La numérotation SYSTUS des éléments démarre à 1. De plus la numérotation MED est compacte par niveau. On se servira de cette variable pour créer une numérotation globale

        c_renum = ConnectivityRenumberer('SYSTUS')
        e_conv = CellsTypeConverter('SYSTUS')

        for j, (medcoupling_type, element_nodes_med) in self.cells_continuous.items():
            systus_type = e_conv.medcoupling_to_external(medcoupling_type)
            element_nodes_med = cells_shift + DataArrayInt(element_nodes_med)
            element_nodes_asc = c_renum.medcoupling_to_external(medcoupling_type, element_nodes_med)
            elements_lines.append('%d %s 1 0 0 '%(j+cells_shift, systus_type) + ' '.join(map(str,element_nodes_asc)))

        nb_elements = len(self.cells_continuous)

        for group, values in self.groups_e_continuous.items():
            ids = cells_shift + DataArrayInt(values)
            groups_e_ids[group] = ids.getValues()
            
        for group, values in self.groups_n.items():
            ids = nodes_shift + DataArrayInt(values)
            groups_n_ids[group] = ids.getValues()
            
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
""".format(*[time.strftime("%y%m%d %H%M%S"), self.mesh_name, nb_nodes, nb_elements])

        txt_nodes = "BEGIN_NODES %d %d\n%s\nEND_NODES\n"%(nb_nodes, self.space_dim, '\n'.join(nodes_lines))
        txt_elements = "BEGIN_ELEMENTS %d\n%s\nEND_ELEMENTS\n"%(nb_elements, '\n'.join(elements_lines))
        txt_groups = "BEGIN_GROUPS %d\n%s\nEND_GROUPS\n"%(nb_groups, '\n'.join(groups_lines)) if groups_lines else ''
        self.systusmesh = ''.join((txt_header, txt_nodes, txt_elements, txt_groups))
