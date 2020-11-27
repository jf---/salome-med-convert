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
        logger.debug("Reading MED mesh file : %s"%filename)
        self.medmesh = MEDFileUMesh(filename)

    def write_med_mesh(self, filename):
        logger.debug("Writing MED mesh file : %s"%filename)
        tic = time.perf_counter()
        self.medmesh.write(filename, 2)
        toc = time.perf_counter()
        logger.debug("End writing in %0.4f seconds" %(toc-tic))


    def create_med_mesh(self):

        assert self._med_ok()

        coords = medcoupling.DataArrayDouble(self.nodes, len(self.nodes)//self.space_dim, self.space_dim)

        logger.debug("Creating MED mesh:")
        self.medmesh = MEDFileUMesh()
        max_dim_elements = int(max(self.elements.keys())[0])
        level_by_dimension = {'%dD'%i : i-max_dim_elements for i in range(max_dim_elements,-1,-1)}

        # Les clés de elements correspondent aux dimensions dans le maillage
        for dim in sorted(self.elements.keys())[::-1]:
            tic = time.perf_counter()

            level = level_by_dimension[dim]
            mesh_at_current_level = MEDCouplingUMesh(self.mesh_name, int(dim[0]))
            mesh_at_current_level.setCoords(coords)
            number_of_elements_at_level = len(self.elements[dim])
            mesh_at_current_level.allocateCells(number_of_elements_at_level)
            toc = time.perf_counter()
            logger.debug("-> Add nodes : %d (in %0.4f seconds)"%(len(coords), toc-tic))
            tic = time.perf_counter()

            # Elements par niveau, avec renumerotation au passage
            for (medcoupling_type, element_nodes_med) in self.elements[dim]:

                number_of_nodes_current_element = MEDCouplingUMesh.GetNumberOfNodesOfGeometricType(medcoupling_type)
                mesh_at_current_level.insertNextCell(medcoupling_type, number_of_nodes_current_element , element_nodes_med)

            mesh_at_current_level.finishInsertingCells()
            sort_order = mesh_at_current_level.sortCellsInMEDFileFrmt()
            sort_dict = {idx : item for idx, item in enumerate(sort_order.getValues())}
            mesh_at_current_level.checkConsistencyLight()
            self.medmesh.setMeshAtLevel(level, mesh_at_current_level)
            toc = time.perf_counter()
            logger.debug("-> Add elements : %d (in %0.4f seconds)"%(len(self.elements[dim]), toc-tic))
            tic = time.perf_counter()

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
        
    def _check_med_group_names(self, lnames):

        MED_LNAME_SIZE = 80
        for group_name in lnames:
            len_name = len(group_name)
            if len_name > MED_LNAME_SIZE :
                msg = "Group name '%s' is too long %d>%d"%(group_name, len_name, MED_LNAME_SIZE)
                raise MedConverterError(msg)

    def _med_ok(self):

        MED_NAME_SIZE = 64
        if len(self.mesh_name) > MED_NAME_SIZE :
            msg = "Mesh name '%s' is too long %d>%d"%(self.mesh_name, len(self.mesh_name), MED_NAME_SIZE)
            raise MedConverterError(msg)

        self._check_med_group_names(self.groups_n.keys())
        for groups_e_at_level in self.groups_e.values():
            self._check_med_group_names(groups_e_at_level.keys())

        return True
