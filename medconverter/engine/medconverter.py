#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import logging

import medcoupling
from MEDLoader import *
from .logger import logger

from .errors import MedConverterError
from .mesh import Mesh

class MedConverter:

    def __init__(self):
        self.verbose = False

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
        logger.debug("Reading MED mesh file : %s"%filename)
        self.medmesh = MEDFileUMesh(filename)

        tic = time.perf_counter()
        self.mesh = Mesh()
        self.mesh.setInputFormat("MED")
        self.mesh.setMeshName(self.medmesh.getName())
        self.mesh.setDimension(self.medmesh.getSpaceDimension())

        # Nodes
        coords = self.medmesh.getCoords()
        for idx, coord in enumerate(coords):
            self.mesh.addNode(idx, coord)

        # Cells (to do)

        # Group's of Cell (to do)

        # Group's of Node
        groups_n = self.medmesh.getGroupsOnSpecifiedLev(1)
        for group in groups_n :
            self.mesh.addGroupOfNodes(group, self.medmesh.getGroupArr(1, group).getValues())

        self.mesh.renumbering()

        toc = time.perf_counter()
        logger.debug("Creating internal mesh in %0.4f seconds"%(toc-tic))

    def write_med_mesh(self, filename):
        logger.debug("Writing MED mesh file : %s"%filename)
        tic = time.perf_counter()
        self.medmesh.write(filename, 2)
        toc = time.perf_counter()
        logger.debug("End writing in %0.4f seconds" %(toc-tic))


    def create_med_mesh(self):

        assert self._med_ok()

        coords = medcoupling.DataArrayDouble(self.mesh.getNodesCoordinates(), \
                    self.mesh.getNumberOfNodes(), self.mesh.getDimension())

        logger.debug("Creating MED mesh:")
        self.medmesh = MEDFileUMesh()

        cellIdsByDim = self.mesh.getCellIdsByDimension()
        max_dim_elements = int(max(cellIdsByDim.keys()))
        level_by_dimension = {i : i-max_dim_elements for i in range(max_dim_elements,-1,-1)}

        grpCellsByDim = self.mesh.getGroupsOfCellIdsByDimension()

        # Les clés de elements correspondent aux dimensions dans le maillage
        for dim in sorted(cellIdsByDim.keys())[::-1]:
            tic = time.perf_counter()

            level = level_by_dimension[dim]
            mesh_at_current_level = MEDCouplingUMesh(self.mesh.getMeshName(), int(dim))
            mesh_at_current_level.setCoords(coords)
            number_of_elements_at_level = len(cellIdsByDim[dim])
            mesh_at_current_level.allocateCells(number_of_elements_at_level)
            toc = time.perf_counter()
            logger.debug("-> Add nodes : %d (in %0.4f seconds)"%(len(coords), toc-tic))
            tic = time.perf_counter()

            # Elements par niveau, avec renumerotation au passage
            sort_dict = {}
            for idx, cell_id in enumerate(cellIdsByDim[dim]):
                sort_dict[cell_id] = idx
                cell = self.mesh.cells[cell_id]
                medcoupling_type = cell.getType()
                element_nodes_med = cell.getNodes()
                number_of_nodes_current_element = MEDCouplingUMesh.GetNumberOfNodesOfGeometricType(medcoupling_type)
                mesh_at_current_level.insertNextCell(medcoupling_type, number_of_nodes_current_element, \
                    element_nodes_med)

            mesh_at_current_level.finishInsertingCells()
            sort_order = mesh_at_current_level.sortCellsInMEDFileFrmt()
            mesh_at_current_level.checkConsistencyLight()
            self.medmesh.setMeshAtLevel(level, mesh_at_current_level)
            toc = time.perf_counter()
            logger.debug("-> Add elements : %d (in %0.4f seconds)"%(len(cellIdsByDim[dim]), toc-tic))

            # Groupes d'elements par niveau
            try :
                tic = time.perf_counter()
                groups_e_at_level = []
                for group_e in grpCellsByDim[dim]:
                    sorted_group = tuple(sort_dict[item] for item in group_e.getElements())
                    group_medcoupling = medcoupling.DataArrayInt(sorted_group)
                    group_medcoupling.setName(str(group_e.getId()))
                    groups_e_at_level.append(group_medcoupling)
                self.medmesh.setGroupsAtLevel(level, groups_e_at_level)
                toc = time.perf_counter()
                logger.debug("-> Add groups of elements : %d (in %0.4f seconds)"%(len(groups_e_at_level), toc-tic))
            except KeyError :
                # On peut ne pas avoir de groupes de mailles d'une certaine dimension
                pass

        # Groupes de noeuds
        tic = time.perf_counter()
        groups_n_at_level = []
        for group_n in self.mesh.groupsOfNodes:
            group_medcoupling = medcoupling.DataArrayInt(group_n.getElements())
            group_medcoupling.setName(str(group_n.getId()))
            groups_n_at_level.append(group_medcoupling)
        self.medmesh.setGroupsAtLevel(1, groups_n_at_level) # Groupes de noeuds au niveau 1
        self.medmesh.setName(self.mesh.getMeshName())
        toc = time.perf_counter()
        logger.debug("-> Add groups of nodes : %d (in %0.4f seconds)"%(len(groups_n_at_level), toc-tic))

        tic = time.perf_counter()
        self.medmesh.rearrangeFamilies()
        toc = time.perf_counter()
        logger.debug("-> Sort families : (in %0.4f seconds)"%(toc-tic))

    def _check_med_group_names(self, lgrp):

        MED_LNAME_SIZE = 80
        for group in lgrp:
            group_name = str(group.getId())
            len_name = len(group_name)
            if len_name > MED_LNAME_SIZE :
                msg = "Group name '%s' is too long %d>%d"%(group_name, len_name, MED_LNAME_SIZE)
                raise MedConverterError(msg)

    def _med_ok(self):

        MED_NAME_SIZE = 64
        if len(self.mesh.getMeshName()) > MED_NAME_SIZE :
            msg = "Mesh name '%s' is too long %d>%d"%(self.mesh.getMeshName(), \
                   len(self.mesh.getMeshName()), MED_NAME_SIZE)
            raise MedConverterError(msg)

        self._check_med_group_names(self.mesh.groupsOfNodes)
        self._check_med_group_names(self.mesh.groupsOfCells)

        return True
