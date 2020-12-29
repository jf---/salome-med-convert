#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os.path as osp
from collections import OrderedDict
import medcoupling

from .logger import logger
from .medconverter import MedConverterMesh
from .errors import MedConverterError
from .cells import CellsTypeConverter
from .connectivity import ConnectivityRenumberer


class AnsysCell:

    def __init__(self, elem_type=None, elem_id=None, elem_nodes=None):
        self.id = elem_id
        if elem_nodes is not None:
            self.nodes = elem_nodes
        else:
            self.nodes = []
        self.type = elem_type

    def __repr__(self):
        return "<Cell> Id: {0}, Type: {1}, Nodes: {2}".format(self.id, self.type, self.nodes)

    def __str__(self):
        return "<Cell> Id: {0}, Type: {1}, Nodes: {2}".format(self.id, self.type, self.nodes)

class AnsysGroup:

    def __init__(self, name=None, typeg=None, group=None):
        self.name = name
        self.type = typeg
        if group is not None:
            self.elems = group
        else:
            self.elems = []

    def __repr__(self):
        return "<Group> Name: {0}, Instance: {1}, Group: {2}".\
            format(self.name, self.type, self.elems)

    def __str__(self):
        return "<Group> Name: {0}, Instance: {1}, Group: {2}".\
            format(self.name, self.type, self.elems)


class MedConverterAnsys(MedConverterMesh):

    @staticmethod
    def convert_ansys_to_med(filename_ansys, filename_med, verbose = False):

        tic = time.perf_counter()
        c = MedConverterAnsys()
        c.verbose = verbose
        c.read_ansys_mesh(filename_ansys)
        c.create_med_mesh()
        c.write_med_mesh(filename_med)
        toc = time.perf_counter()
        logger.debug("Mesh converted (in %0.4f seconds)"%(toc-tic))

    @staticmethod
    def convert_med_to_ansys(filename_med, filename_ansys, verbose = False):

        tic = time.perf_counter()
        c = MedConverterAnsys()
        c.verbose = verbose
        c.read_med_mesh(filename_med)
        c.create_ansys_mesh()
        c.write_ansys_mesh(filename_ansys)
        toc = time.perf_counter()
        logger.debug("Mesh converted (in %0.4f seconds)"%(toc-tic))

    def __init__(self):
        super(MedConverterAnsys, self).__init__()
        self.ansysmesh = None

    def read_ansys_mesh(self, filename):
        logger.debug("Read ANSYS mesh.")

        self._reset_structures()
        Cells, Groups,  title  = [], [], None
        nb_total_nodes, nb_total_cells = 0, 0
        time_nodes, time_cell, time_groups = 0.0, 0.0, 0.0
        ElemAnsys = {}

        tic = time.perf_counter()
        # Lecture du fichier .cdb où les blocs sont separés par des BEGIN_* et END_*
        with open(filename, 'r', encoding = self._get_file_encoding(filename)) as file :

            for line in file :
                strip_line = line.strip()
                spline = strip_line.split()

                if strip_line.startswith("NBLOCK") :
                    tic0 = time.perf_counter()
                    dim = int(line.split(",")[1])
                    nb_total_nodes += int(line.split(",")[4])
                    self.space_dim = dim-3
                    self.__read_nodes(file)
                    toc0 = time.perf_counter()
                    time_nodes += toc0 - tic0
                elif strip_line.startswith("EBLOCK"):
                    tic0 = time.perf_counter()
                    nb_total_cells += int(line.split(",")[4])
                    self.__read_cells(file, Cells)
                    toc0 = time.perf_counter()
                    time_cell += toc0 - tic0
                elif strip_line.startswith("CMBLOCK") :
                    tic0 = time.perf_counter()
                    self.__read_groups(file, line, Groups)
                    toc0 = time.perf_counter()
                    time_groups += toc0 - tic0
                elif strip_line.startswith("ET,"):
                    sspline = strip_line.split(",")
                    ElemAnsys[int(sspline[1])] = int(sspline[2])
                elif "/TITLE" in line :
                    # Gestion du titre
                    title = line.split(",")[1].strip().replace("\n", '')


        assert nb_total_nodes == len(self.nodes)
        assert nb_total_cells == len(Cells)


        #Réupération du nom du maillage
        self.mesh_name = title or osp.splitext(osp.split(filename)[-1])[0]

        toc = time.perf_counter()
        logger.debug(" File name : %s (parsed in %0.4f seconds)"%(filename, toc-tic))
        logger.debug(" -> nodes: %d (parsed in %0.4f seconds)"%(nb_total_nodes, time_nodes))
        logger.debug(" -> cells: %d (parsed in %0.4f seconds)"%(nb_total_cells, time_cell))
        logger.debug(" -> groups: %d (parsed in %0.4f seconds)"%(len(Groups), time_groups))

        logger.debug(" Mesh name : %s"%self.mesh_name)
        logger.debug(" Space Dimension : %d"%self.space_dim)
        logger.debug(" Number of nodes : %d"%(len(self.nodes)))

        # Les elements
        tic = time.perf_counter()
        e_conv = CellsTypeConverter('ANSYS')
        c_renum = ConnectivityRenumberer('ANSYS')
        for cell in Cells:
            element_ansys_type=ElemAnsys[cell.type]
            # some trick for few cells (remove last node)
            element_ansys_test = str(element_ansys_type) + '_' + str(len(cell.nodes))
            if element_ansys_test in ("188_3", "189_4", "288_3", "289_4"):
                nb_nodes = len(cell.nodes) - 1
            else:
                nb_nodes = len(cell.nodes)

            elements_nodes_ansys = list(OrderedDict.fromkeys(cell.nodes[:nb_nodes]))
            element_ansys_type = str(element_ansys_type) + '_' + str(len(elements_nodes_ansys))
            element_medcoupling_type = e_conv.external_to_medcoupling(element_ansys_type)
            element_nodes_med = c_renum.external_to_medcoupling(element_medcoupling_type, elements_nodes_ansys)

            self.add_cell(cell.id, element_medcoupling_type, element_nodes_med)

        toc = time.perf_counter()
        logger.debug(" Load %d cells (in %0.4f seconds)"%(len(Cells), toc-tic))

        # Les groups
        tic = time.perf_counter()
        for group in Groups :
            values = []
            for elem in group.elems:
                if elem > 0:
                    values.append(elem)
                else:
                    values += range(values[-1]+1, (-elem)+1)

            if group.type == 'NODE' :
                self.add_group_nodes(group.name, values)
            elif group.type == 'ELEM':
                self.add_group_cells(group.name, values)
            else:
                raise MedConverterError("Unknown group's type")

        toc = time.perf_counter()
        logger.debug(" Load %d groups (in %0.4f seconds)"%(len(Groups), toc-tic))


    def getCoor(self, line, firstStr, longFloat):
        # le premier decimal commence a la colonne firstStrg
        rline = line.rstrip()[firstStr:]
        elems = [float(rline[i:i+longFloat]) for i in range(0, len(rline), longFloat)]

        nbElem = len(elems)
        assert nbElem <= 3

        if nbElem == 3:
            return elems
        else:
            return elems + [0.0]*(3-nbElem)

    def __read_nodes(self, file):
        while True:
            line = file.readline()
            strip_line = line.strip()
            if strip_line.startswith("(") :
                [firstStr, LongFloat] = self.node_format(strip_line)
            elif strip_line.startswith("N,") :
                break
            else :
                spline = strip_line.split()
                self.add_node(int(spline[0]), self.getCoor(line, firstStr, LongFloat))

    def __read_cells(self, file, Cells):
        l_new_cell = True
        while True:
            line = file.readline()
            rline = line.rstrip()
            strip_line = rline.lstrip()
            if strip_line.startswith("(") :
                nbElem, LongInt = self.cell_format(strip_line)
            elif strip_line.startswith("-1") :
                break
            else :
                enum = [int(rline[i:i+LongInt]) for i in range(0, len(rline), LongInt)]
                assert len(enum) <= nbElem

                if l_new_cell:
                    cnodes = enum[11:]
                    nb_nodes = enum[8]
                    cid = enum[10]
                    ctype = enum[1]
                    if len(cnodes) < nb_nodes:
                        l_new_cell = False
                else:
                    cnodes += enum
                    if len(cnodes) == nb_nodes:
                        l_new_cell = True

                if l_new_cell:
                    assert len(cnodes) == nb_nodes
                    Cells.append(AnsysCell(ctype, cid, cnodes))

    def __read_groups(self, file, line, Groups):
        spline = line.split(",")
        gname = spline[1]
        gtype = spline[2]
        nb_elem = int(spline[3].split()[0])
        elems = []
        while True:
            line = file.readline()
            rline = line.rstrip()
            strip_line = rline.lstrip()
            if strip_line.startswith("(") :
                nbElem, LongInt = self.cell_format(strip_line)
            else :
                elems += [int(rline[i:i+LongInt]) for i in range(0, len(rline), LongInt)]

                if len(elems) == nb_elem:
                    Groups.append(AnsysGroup(gname, gtype, elems))
                    break
                elif len(elems) > nb_elem:
                    raise MedConverterError("Wrong reading of groups")

    def decode_format(self, line):
        return line.strip().lstrip("(").rstrip(")").split(",")

    def node_format(self, line):
        format = self.decode_format(line)
        s0 = format[0].split("i")
        firstStr = int(s0[0]) * int(s0[1])
        long = int(format[1].split('e')[1].split(".")[0])

        return [firstStr, long]

    def cell_format(self, line):
        format = self.decode_format(line)
        s0 = format[0].split("i")
        nbElem = int(s0[0])
        long = int(s0[1])

        return [nbElem, long]

    def write_ansys_mesh(self, filename):
        raise NotImplementedError()

    def create_ansys_mesh(self):
        raise NotImplementedError()
