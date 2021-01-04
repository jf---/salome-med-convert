#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os.path as osp
import medcoupling

from ..utilities import chunks
from .logger import logger
from .medconverter import MedConverterMesh
from .errors import MedConverterError
from .cells import CellsTypeConverter, GroupCellsTypeConverter
from .connectivity import ConnectivityRenumberer

ZSET_MAX_LINE_SIZE = 21
ZSET_NODES_SHIFT = 1 # La numérotation ZSET des noeuds démarre à 1
ZSET_CELLS_SHIFT = 1 # La numérotation ZSET des élements démarre à 1

class MedConverterZset(MedConverterMesh):

    @staticmethod
    def convert_zset_to_med(filename_zset, filename_med, verbose = False):

        tic = time.perf_counter()
        c = MedConverterZset()
        c.verbose = verbose
        c.read_zset_mesh(filename_zset)
        c.create_med_mesh()
        c.write_med_mesh(filename_med)
        toc = time.perf_counter()
        logger.debug("Mesh converted (in %0.4f seconds)"%(toc-tic))

    @staticmethod
    def convert_med_to_zset(filename_med, filename_zset, verbose = False):

        tic = time.perf_counter()
        c = MedConverterZset()
        c.verbose = verbose
        c.read_med_mesh(filename_med)
        c.create_zset_mesh()
        c.write_zset_mesh(filename_zset)
        toc = time.perf_counter()
        logger.debug("Mesh converted (in %0.4f seconds)"%(toc-tic))

    def __init__(self):
        super(MedConverterZset, self).__init__()
        self.zsetmesh = None

    def read_zset_mesh(self, filename):
        logger.debug("Read ZSET mesh.")

        self._reset_structures()

        NODES, ELEMENTS, GROUPS = [], [], []

        flag = {'NODES' : 0,
                'ELEMENTS' : 0,
                'GROUPS' : 0
            }

        tic = time.perf_counter()
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

        logger.debug(" File name : %s (parsed in %0.4f seconds)"%(filename, toc-tic))
        logger.debug(" Mesh name : %s"%self.mesh_name)
        logger.debug(" Space Dimension : %d"%self.space_dim)

        # Les noeuds
        tic = time.perf_counter()
        for line in NODES[1:-1]:
            spline = line.split()
            idx_zset = int(spline[0])
            coords = tuple(map(float, spline[-self.space_dim:]))
            self.add_node(idx_zset, coords)
        toc = time.perf_counter()
        logger.debug(" Load %d nodes (in %0.4f seconds)"%(len(NODES)-2, toc-tic))

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
        logger.debug(" Load %d cells (in %0.4f seconds)"%(len(ELEMENTS)-2, toc-tic))

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
        logger.debug(" Parse groups (in %0.4f seconds)"%(toc-tic))

        tic = time.perf_counter()
        nodes_groups = groups.get('nset', {})
        for group_name, items in sorted(nodes_groups.items()):
            values = (int(i) for line in items for i in line)
            self.add_group_nodes(group_name, values)
        toc = time.perf_counter()
        logger.debug(" Add %d nset (in %0.4f seconds)"%(len(nodes_groups), toc-tic))

        tic = time.perf_counter()
        cells_groups = groups.get('elset', {})
        for group_name, items in sorted(cells_groups.items()):
            values = (int(i) for line in items for i in line)
            self.add_group_cells(group_name, values)
        toc = time.perf_counter()
        logger.debug(" Add %d elset (in %0.4f seconds)"%(len(cells_groups), toc-tic))

        tic = time.perf_counter()
        faset = groups.get('faset', {})
        for faset_name, items in sorted(faset.items()):
            self._add_bset(faset_name, items, g_conv, c_renum)
        toc = time.perf_counter()
        logger.debug(" Add %d faset (in %0.4f seconds)"%(len(faset), toc-tic))

        tic = time.perf_counter()
        liset = groups.get('liset', {})
        for liset_name, items in sorted(liset.items()):
            self._add_bset(liset_name, items, g_conv, c_renum)
        toc = time.perf_counter()
        logger.debug(" Add %d liset (in %0.4f seconds)"%(len(liset), toc-tic))

    def _add_bset(self, bset_name, bset_items, g_conv, c_renum):
        max_idx_elements = max(i for dim in self.corresponding_cells.values() for i in dim)
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
        tic = time.perf_counter()
        with open(filename, 'w') as f :
            f.write(self.zsetmesh)
        toc = time.perf_counter()
        logger.debug("Write ZSET mesh file : %s (in %0.4f seconds)"%(filename, toc-tic))

    def create_zset_mesh(self):
        self.zsetmesh = None
        logger.debug("Create ZSET mesh.")
        logger.debug(" Mesh name : %s"%self.mesh_name)
        logger.debug(" Space Dimension : %d"%self.space_dim)

        tic = time.perf_counter()
        nb_nodes = len(self.nodes)
        frmt = ' '.join(['{:.15e}']*self.space_dim)
        nodes_lines = ('%d '%(i+ZSET_NODES_SHIFT) + frmt.format(*node) for i, node in enumerate(self.nodes))
        toc = time.perf_counter()
        logger.debug(" Add %d nodes (in %0.4f seconds)"%(nb_nodes, toc-tic))

        c_renum = ConnectivityRenumberer('ZSET')
        e_conv = CellsTypeConverter('ZSET')
        g_conv = GroupCellsTypeConverter('ZSET')

        elements_lines = []
        tic = time.perf_counter()
        for j, (medcoupling_type, element_nodes_med) in enumerate(self.cells[self.max_dim_cells]):
            zset_type = e_conv.medcoupling_to_external(medcoupling_type)
            element_nodes_med = ZSET_CELLS_SHIFT + medcoupling.DataArrayInt(element_nodes_med)
            element_nodes_geof = c_renum.medcoupling_to_external(medcoupling_type, element_nodes_med)
            elements_lines.append('%d %s '%(j+ZSET_CELLS_SHIFT, zset_type) + ' '.join(map(str,element_nodes_geof)))

        nb_elements = len(elements_lines)
        toc = time.perf_counter()
        logger.debug(" Add %d cells (in %0.4f seconds)"%(nb_elements, toc-tic))

        tic = time.perf_counter()
        groups_lines = []
        for group, values in self.groups_n.items():
            ids = ZSET_NODES_SHIFT + medcoupling.DataArrayInt(values)
            groups_lines.append('**nset {}'.format(group))
            for chunck in chunks(ids.getValues(), ZSET_MAX_LINE_SIZE):
                groups_lines.append(' %s'%(' '.join(map(str, chunck))))
        toc = time.perf_counter()
        logger.debug(" Add %d nset (in %0.4f seconds)"%(len(self.groups_n), toc-tic))

        tic = time.perf_counter()
        elset = self.groups_e.get(self.max_dim_cells, {})
        for group, values in elset.items():
            ids = ZSET_CELLS_SHIFT + medcoupling.DataArrayInt(values)
            groups_lines.append('**elset {}'.format(group))
            for chunck in chunks(ids.getValues(), ZSET_MAX_LINE_SIZE):
                groups_lines.append(' %s'%(' '.join(map(str, chunck))))
        toc = time.perf_counter()
        logger.debug(" Add %d elset (in %0.4f seconds)"%(len(elset), toc-tic))

        tic = time.perf_counter()
        dim_liset = '1D'
        liset = self.groups_e.get(dim_liset, {})
        for group, values in liset.items():
            groups_lines.append('**liset {}'.format(group))
            for cell in values:
                medcoupling_type, element_nodes_med = self.cells[dim_liset][cell]
                zset_type = g_conv.medcoupling_to_external(medcoupling_type)
                element_nodes_med = ZSET_CELLS_SHIFT + medcoupling.DataArrayInt(element_nodes_med)
                element_nodes_geof = c_renum.medcoupling_to_external(medcoupling_type, element_nodes_med)
                groups_lines.append('%s  '%zset_type + ' '.join(map(str, element_nodes_geof)))
            groups_lines.append('')
        toc = time.perf_counter()
        logger.debug(" Add %d liset (in %0.4f seconds)"%(len(liset), toc-tic))

        tic = time.perf_counter()
        dim_faset = '2D' if self.space_dim == 3 else None
        faset = self.groups_e.get(dim_faset, {})
        for group, values in faset.items():
            groups_lines.append('**faset {}'.format(group))
            for cell in values:
                medcoupling_type, element_nodes_med = self.cells[dim_faset][cell]
                zset_type = g_conv.medcoupling_to_external(medcoupling_type)
                element_nodes_med = ZSET_CELLS_SHIFT + medcoupling.DataArrayInt(element_nodes_med)
                element_nodes_geof = c_renum.medcoupling_to_external(medcoupling_type, element_nodes_med)
                groups_lines.append('%s  '%zset_type + ' '.join(map(str, element_nodes_geof)))
            groups_lines.append('')
        toc = time.perf_counter()
        logger.debug(" Add %d faset (in %0.4f seconds)"%(len(faset), toc-tic))

        tic = time.perf_counter()
        txt_header = "***geometry\n"
        txt_nodes = "**node\n%d %d\n%s\n"%(nb_nodes, self.space_dim, '\n'.join(nodes_lines))
        txt_elements = "**element\n%d\n%s\n***group\n"%(nb_elements, '\n'.join(elements_lines))
        txt_groups = '\n'.join(groups_lines)
        txt_footer = '\n***return'
        self.zsetmesh = ''.join((txt_header, txt_nodes, txt_elements, txt_groups, txt_footer))
        toc = time.perf_counter()
        logger.debug(" Assembly file (in %0.4f seconds)"%(toc-tic))
