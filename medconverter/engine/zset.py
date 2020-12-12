#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import logging
import os.path as osp
from operator import itemgetter
import medcoupling
# from medcoupling import *

from .logger import logger
from .medconverter import MedConverterMesh
from .errors import MedConverterError
from .cells import CellsTypeConverter, GroupCellsTypeConverter
from .connectivity import ConnectivityRenumberer

class MedConverterZset(MedConverterMesh):

    @staticmethod
    def convert_zset_to_med(filename_zset, filename_med, verbose = False):
        if verbose :
            logger.setLevel(logging.DEBUG)
        c = MedConverterZset()
        c.read_zset_mesh(filename_zset)
        c.create_med_mesh()
        c.write_med_mesh(filename_med)

    @staticmethod
    def convert_med_to_zset(filename_med, filename_zset, verbose = False):
        if verbose :
            logger.setLevel(logging.DEBUG)
        c = MedConverterZset()
        c.read_med_mesh(filename_med)
        c.create_zset_mesh()
        c.write_zset_mesh(filename_zset)

    @property
    def group_level_labels(self):
        if self.space_dim == 2 :
            return {'2D' : 'elset',
                    '1D' : 'liset'}
        elif self.space_dim == 3 :
            return {'3D' : 'elset',
                    '2D' : 'faset',
                    '1D' : 'liset'}
        else :
            return
        
    def __init__(self):
        super(MedConverterZset, self).__init__()
        self.zsetmesh = None

    def read_zset_mesh(self, filename):
        self._reset_structures()

        NODES, ELEMENTS, GROUPS = [], [], []

        flag = {'NODES' : 0,
                'ELEMENTS' : 0,
                'GROUPS' : 0
            }

        tic = time.perf_counter()
        # Lecture du fichier .ASC où les blocs sont separés par des BEGIN_* et END_*
        with open(filename, 'r', encoding = self._get_file_encoding(filename)) as f :
            self.mesh_name = osp.splitext(osp.split(filename)[-1])[0]

            for line in f :
                if flag['NODES'] is 1 :
                    NODES.append(line)
                elif flag['ELEMENTS'] is 1 :
                    ELEMENTS.append(line)
                elif flag['GROUPS'] is 1 :
                    GROUPS.append(line)
            
                if "**node" in line :
                    flag['NODES'] = 1
            
                elif "**element" in line :
                    flag['ELEMENTS'] = 1
                    flag['NODES'] =  0
                    
                elif "***group" in line :
                    flag['ELEMENTS'] = 0
                    flag['GROUPS'] = 1

                elif "***return" in line :
                    flag['GROUPS'] = 0

        nb_nodes, self.space_dim = map(int, NODES[0].split())
        nb_elements = int(ELEMENTS[0].split()[0])
        toc = time.perf_counter()

        logger.debug("Reading ZSET mesh file : %s (in %0.4f seconds)"%(filename, toc-tic))
        logger.debug("Mesh name : %s"%self.mesh_name)
        logger.debug("Space Dimension : %d"%self.space_dim)
        logger.debug("Number of nodes : %d"%(len(NODES)-1))
        logger.debug("Number of elements : %d"%(len(ELEMENTS)-1))
        logger.debug("Number of groups : %d"%(len(GROUPS)-1))

        # Les noeuds
        tic = time.perf_counter()
        for line in NODES[1:-1]:
            spline = line.split()
            idx_zset = int(spline[0])
            coords = tuple(map(float, spline[-self.space_dim:]))
            self.add_node(idx_zset, coords)
        toc = time.perf_counter()
        logger.debug("-> Adding nodes (in %0.4f seconds)"%(toc-tic))
        
        # Les elements
        e_conv = CellsTypeConverter('ZSET')
        g_conv = GroupCellsTypeConverter('ZSET')
        c_renum = ConnectivityRenumberer('ZSET')

        tic = time.perf_counter()
        for line in ELEMENTS[1:-1] :
            spline = line.split()
            idx_element_zset = int(spline[0])
            element_zset_type = spline[1]
            elements_nodes_zset = tuple(map(int, spline[2:]))

            element_medcoupling_type = e_conv.external_to_medcoupling(element_zset_type)
            element_nodes_med = c_renum.external_to_medcoupling(element_medcoupling_type, elements_nodes_zset)

            self.add_cell(idx_element_zset, element_medcoupling_type, element_nodes_med)

        toc = time.perf_counter()
        logger.debug("-> Adding cells (in %0.4f seconds)"%(toc-tic))
        
        # Les groupes
        tic = time.perf_counter()
        groups = {}
        for line in GROUPS[:-1] :
            if '**' in line:
                type_grp, name_grp = line.strip('**').split()
                if type_grp not in groups:
                    groups[type_grp] = {}
                if name_grp not in groups[type_grp]:
                    groups[type_grp][name_grp] = []
            else:
                groups[type_grp][name_grp].append(line.split())

        toc = time.perf_counter()
        logger.debug("-> Parsing groups (in %0.4f seconds)"%(toc-tic))


        tic = time.perf_counter()
        nodes_groups = groups.get('nset', {})
        for group_name, items in nodes_groups.items():
            values = (int(i) for line in items for i in line)
            self.add_group_nodes(group_name, values)
        toc = time.perf_counter()
        logger.debug("-> Adding nset (in %0.4f seconds)"%(toc-tic))

        tic = time.perf_counter()
        cells_groups = groups.get('elset', {})
        for group_name, items in cells_groups.items():
            values = (int(i) for line in items for i in line)
            self.add_group_cells(group_name, values)
        toc = time.perf_counter()
        logger.debug("-> Adding elset (in %0.4f seconds)"%(toc-tic))

        tic = time.perf_counter()
        faset = groups.get('faset', {})
        for faset_name, items in faset.items():
            self._add_bset(faset_name, items, g_conv, c_renum)
        toc = time.perf_counter()
        logger.debug("-> Adding faset (in %0.4f seconds)"%(toc-tic))

        tic = time.perf_counter()
        liset = groups.get('liset', {})
        for liset_name, items in liset.items():
            self._add_bset(liset_name, items, g_conv, c_renum)
        toc = time.perf_counter()
        logger.debug("-> Adding liset (in %0.4f seconds)"%(toc-tic))

    def _add_bset(self, bset_name, bset_items, g_conv, c_renum):
        max_idx_elements = self.max_idx_cells_external
        values = []
        for i, spline in enumerate((j for j in bset_items if bool(j))):
            idx_element_zset = max_idx_elements + i + 1
            element_zset_type = spline[0]
            elements_nodes_zset = tuple(map(int, spline[1:]))

            element_medcoupling_type = g_conv.external_to_medcoupling(element_zset_type)
            element_nodes_med = c_renum.external_to_medcoupling(element_medcoupling_type, elements_nodes_zset)

            self.add_cell(idx_element_zset, element_medcoupling_type, element_nodes_med)
            values.append(idx_element_zset)
        self.add_group_cells(bset_name, values)
        
    def write_zset_mesh(self, filename):
        raise NotImplementedError()

    def create_zset_mesh(self):
        raise NotImplementedError()
