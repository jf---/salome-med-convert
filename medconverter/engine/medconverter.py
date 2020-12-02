#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import logging
import os.path as osp
import numpy as np
from collections import OrderedDict
import medcoupling
from medcoupling import *

from .logger import logger
from .errors import MedConverterError

class MedConverterMesh:

    @property
    def mesh_name(self):
        return self._mesh_name
    
    @mesh_name.setter
    def mesh_name(self, name):
        not_allowed_symbols_in_name = ('/',)
        if any(symbol in name for symbol in not_allowed_symbols_in_name) :
            msg = "The following symbols are not allowed in MED mesh name: {}".format(not_allowed_symbols_in_name)
            raise MedConverterError(msg)

        MED_NAME_SIZE = 64
        if len(name) > MED_NAME_SIZE :
            msg = "Mesh name '%s' is too long %d>%d"%(name, len(name), MED_NAME_SIZE)
            raise MedConverterError(msg)
        
        self._mesh_name = name

    @property
    def dimensions(self):
        return sorted(self.cells.keys())[::-1]

    @property
    def levels(self):
        max_dim_cells = int(max(self.cells.keys())[0])
        return {'%dD'%i : i-max_dim_cells for i in range(max_dim_cells,-1,-1)}
                    
    def __init__(self):
        self._mesh_name = None
        self.space_dim = None
        self.nodes = []
        self.cells = OrderedDict() # Par niveau
        self.groups_e = OrderedDict() # Par niveau
        self.groups_n = OrderedDict()
        
        self.groups_e_continuous = OrderedDict() # Numérotation globale
        self.cells_continuous = OrderedDict() # Numérotation globale
        
        self.verbose = False
        self.medmesh = None
        
        self._corresponding_nodes = {}
        self._corresponding_cells = {}
        
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

    def _check_group_name(self, name):
        MED_LNAME_SIZE = 80
        if len(name) > MED_LNAME_SIZE :
            msg = "Group name '%s' is too long %d>%d"%(name, len(name), MED_LNAME_SIZE)
            raise MedConverterError(msg)

    def add_node(self, idx, coords):
        self._corresponding_nodes[idx] = len(self.nodes)
        self.nodes.append(coords)
        
    def add_cell(self, idx, medcoupling_cell_type, cell_nodes):
        
        cell_dim = MEDCouplingUMesh.GetDimensionOfGeometricType(medcoupling_cell_type)
        cell_nodes_med = tuple(self._corresponding_nodes[k] for k in cell_nodes)
        
        key = '%dD'%cell_dim
        if not key in self.cells :
            self.cells[key] = []
        if not key in self._corresponding_cells :
            self._corresponding_cells[key] = {}

        self.cells[key].append((medcoupling_cell_type, cell_nodes_med))
        self._corresponding_cells[key][idx] = len(self._corresponding_cells[key])

    def add_group_nodes(self, group_name, group_nodes):
        self._check_group_name(group_name)
        self.groups_n[group_name] = tuple(self._corresponding_nodes[k] for k in group_nodes)
    
    def add_group_cells(self, group_name, group_cells):
        self._check_group_name(group_name)
        for cell in group_cells :
            for dim in self.cells.keys():
                if cell in self._corresponding_cells[dim]:
                    if not dim in self.groups_e :
                        self.groups_e[dim] = {}
                    if not group_name in self.groups_e[dim]:
                        self.groups_e[dim][group_name] = []
                    self.groups_e[dim][group_name].append(self._corresponding_cells[dim][cell])
                   
    def read_med_mesh(self, filename):
        logger.debug("Reading MED mesh file : %s"%filename)
        
        self.medmesh = MEDFileUMesh(filename)
        self.mesh_name = self.medmesh.getName()
        self.space_dim = self.medmesh.getSpaceDimension()
        
        self.nodes = self.medmesh.getCoords().getValuesAsTuple()
        self._corresponding_nodes = {i : i  for i in range(len(self.nodes))}

        non_empty_levs = self.medmesh.getNonEmptyLevels()
        cells_shift = 0 # Variable pour la creation d'une numérotation globale
        for lev in non_empty_levs:
            mesh_lev = self.medmesh[lev]
            j = 0 # Variable pour conter le nombre d'elements par niveau
            types_at_level = mesh_lev.getAllGeoTypesSorted()
            for medcoupling_cell_type in types_at_level :
                cells_by_type = mesh_lev.giveCellsWithType(medcoupling_cell_type).getValues()
                for cell in cells_by_type :
                    element_nodes_med = mesh_lev.getNodeIdsOfCell(cell)
                    self.add_cell(cells_shift+j, medcoupling_cell_type, element_nodes_med)
                    self.cells_continuous[cells_shift+j] = (medcoupling_cell_type, element_nodes_med)
                    j+=1

            for group in self.medmesh.getGroupsOnSpecifiedLev(lev):
                ids = cells_shift + self.medmesh.getGroupArr(lev, group)
                self.add_group_cells(group, ids.getValues())
                if group in self.groups_e_continuous :
                    for v in ids.getValues():
                        self.groups_e_continuous[group].append(v)
                else:
                    self.groups_e_continuous[group] = ids.getValues()

            cells_shift+=mesh_lev.getNumberOfCells()

        for group in self.medmesh.getGroupsOnSpecifiedLev(1):
            ids = self.medmesh.getGroupArr(1, group).getValues()
            self.add_group_nodes(group, ids)
                   
    def write_med_mesh(self, filename):
        logger.debug("Writing MED mesh file : %s"%filename)
        tic = time.perf_counter()
        self.medmesh.write(filename, 2)
        toc = time.perf_counter()
        logger.debug("End writing in %0.4f seconds" %(toc-tic))

    def create_med_mesh(self):
        
        coords = DataArrayDouble(self.nodes)
        
        logger.debug("Creating MED mesh:")
        self.medmesh = MEDFileUMesh()

        # Les clés de elements correspondent aux dimensions dans le maillage
        for dim in self.dimensions:
            tic = time.perf_counter()

            level = self.levels[dim]
            mesh_at_current_level = MEDCouplingUMesh(self.mesh_name, int(dim[0]))
            mesh_at_current_level.setCoords(coords)
            number_of_elements_at_level = len(self.cells[dim])
            mesh_at_current_level.allocateCells(number_of_elements_at_level)
            toc = time.perf_counter()
            logger.debug("-> Add nodes : %d (in %0.4f seconds)"%(len(coords), toc-tic))
            tic = time.perf_counter()
            
            # Elements par niveau, avec renumerotation au passage
            for (medcoupling_type, element_nodes_med) in self.cells[dim]:
                number_of_nodes_current_element = MEDCouplingUMesh.GetNumberOfNodesOfGeometricType(medcoupling_type)
                mesh_at_current_level.insertNextCell(medcoupling_type, number_of_nodes_current_element , element_nodes_med)

            mesh_at_current_level.finishInsertingCells()
            o2n = mesh_at_current_level.sortCellsInMEDFileFrmt()
            mesh_at_current_level.checkConsistencyLight()
            self.medmesh.setMeshAtLevel(level, mesh_at_current_level)
            toc = time.perf_counter()
            logger.debug("-> Add elements : %d (in %0.4f seconds)"%(len(self.cells[dim]), toc-tic))
            tic = time.perf_counter()

            # Groupes d'elements par niveau
            try :
                groups_e_at_level = []
                for group_name, group_elements in self.groups_e[dim].items():
                    group_medcoupling = medcoupling.DataArrayInt(group_elements)
                    group_medcoupling.transformWithIndArr(o2n)
                    group_medcoupling.setName(group_name)
                    groups_e_at_level.append(group_medcoupling)
                self.medmesh.setGroupsAtLevel(level, groups_e_at_level)
            except KeyError :
                # On peut ne pas avoir de groupes de mailles d'une certaine dimension
                pass
            toc = time.perf_counter()
            logger.debug("-> Add groups of elements : %d (in %0.4f seconds)"%(len(groups_e_at_level), toc-tic))

        tic = time.perf_counter()

        # Groupes de noeuds
        groups_n_at_level = []
        for group_name, group_nodes in self.groups_n.items():
            group_medcoupling = medcoupling.DataArrayInt(group_nodes)
            group_medcoupling.setName(group_name)
            groups_n_at_level.append(group_medcoupling)
        self.medmesh.setGroupsAtLevel(1, groups_n_at_level) # Groupes de noeuds au niveau 1
        self.medmesh.setName(self.mesh_name)
        toc = time.perf_counter()
        logger.debug("-> Add groups of nodes : %d (in %0.4f seconds)"%(len(groups_n_at_level), toc-tic))

        tic = time.perf_counter()
        self.medmesh.rearrangeFamilies()
        toc = time.perf_counter()
        logger.debug("-> Sort families : (in %0.4f seconds)"%(toc-tic))
