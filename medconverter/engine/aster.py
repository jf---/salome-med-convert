#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import re
import os.path as osp
import medcoupling

from ..utilities import chunks
from .logger import logger
from .medconverter import MedConverterMesh
from .errors import MedConverterError
from .cells import CellsTypeConverter
from .connectivity import ConnectivityRenumberer

ASTER_MAX_LINE_SIZE = 8
ASTER_NODES_SHIFT = 1  # La numérotation ASTER des noeuds démarre à 1
ASTER_CELLS_SHIFT = 1  # La numérotation ASTER des élements démarre à 1


class MedConverterAster(MedConverterMesh):
    @staticmethod
    def convert_aster_to_med(filename_aster, filename_med, output_comm, verbose=False):

        tic = time.perf_counter()
        c = MedConverterAster()
        c.verbose = verbose
        c.read_aster_mesh(filename_aster)
        c.create_med_mesh()
        c.write_med_mesh(filename_med)
        toc = time.perf_counter()
        logger.debug("Mesh converted (in %0.4f seconds)" % (toc - tic))

    @staticmethod
    def convert_med_to_aster(filename_med, filename_aster, output_comm, verbose=False):

        tic = time.perf_counter()
        c = MedConverterAster()
        c.verbose = verbose
        c.read_med_mesh(filename_med)
        c.create_aster_mesh()
        c.write_aster_mesh(filename_aster)
        toc = time.perf_counter()
        logger.debug("Mesh converted (in %0.4f seconds)" % (toc - tic))

    def __init__(self):
        super(MedConverterAster, self).__init__()
        self.astermesh = None

    def _slow_parser(self, filename):
        # Pour lire des fichiers .mail assez vieux...
        skip = "NBOBJ NBLIGE NBLIGT NUMIN NUMAX AUTEUR DATE".split()
        re_dbl_fort = re.compile(r"(\d*\.\d+)[dD]([-+]?\d+)")

        with open(filename, "r", encoding=self._get_file_encoding(filename)) as f:
            for line in f:
                line = line.partition("%")[0].strip()
                if any(j in line for j in skip):
                    for k in skip:
                        line = line.partition(k)[0].strip()
                line = line.upper()
                line = re_dbl_fort.sub(r"\1E\2", line)
                spline = line.split()
                if len(spline) > 0:
                    yield line, spline

    def _fast_parser(self, filename):
        # Pour lire des fichiers .mail exportés par un IMPR_RESU
        with open(filename, "r", encoding=self._get_file_encoding(filename)) as f:
            for line in f:
                line = line.partition("%")[0].strip()
                spline = line.split()
                if len(spline) > 0:
                    yield line, spline

    def read_aster_mesh(self, filename, parse_fast=True):
        logger.debug("Read ASTER mesh.")

        self._reset_structures()

        NODES, ELEMENTS, GROUPS_N, GROUPS_M = [], {}, {}, {}

        flag = {"NODES": 0, "ELEMENTS": 0, "GROUPS_N": 0, "GROUPS_M": 0}

        tic = time.perf_counter()

        self.mesh_name = osp.splitext(osp.split(filename)[-1])[0]

        mail_parser = self._fast_parser(filename) if parse_fast else self._slow_parser(filename)
        for line, spline in mail_parser:

            if not "FINSF" in spline[0]:
                if flag["NODES"] == 1:
                    NODES.append(spline)
                elif flag["ELEMENTS"] == 1:
                    for i in spline:
                        ELEMENTS[etype].append(i)
                elif flag["GROUPS_N"] == 1:
                    for i in spline:
                        GROUPS_N[grp_name].append(i)
                elif flag["GROUPS_M"] == 1:
                    for i in spline:
                        GROUPS_M[grp_name].append(i)

            if any(i in (spline[0],) for i in ("COOR_2D", "COOR_3D")):
                flag["NODES"] = 1
                self.space_dim = int(spline[0].strip("COOR_").strip("D"))

            elif any(i in (spline[0],) for i in CellsTypeConverter._aster_to_med.keys()):
                flag["ELEMENTS"] = 1
                etype = spline[0]
                ELEMENTS.setdefault(etype, [])

            elif "GROUP_NO" in spline[0]:
                flag["GROUPS_N"] = 1
                if any("NOM" in i for i in spline):
                    grp_name = line.partition("NOM")[-1].partition("=")[-1].strip().split()[0]
                else:
                    grp_name = next(mail_parser)[0]
                GROUPS_N[grp_name] = []

            elif "GROUP_MA" in spline[0]:
                flag["GROUPS_M"] = 1
                if any("NOM" in i for i in spline):
                    grp_name = line.partition("NOM")[-1].partition("=")[-1].strip().split()[0]
                else:
                    grp_name = next(mail_parser)[0]
                GROUPS_M[grp_name] = []

            elif "FINSF" in spline[0]:
                flag["NODES"] = 0
                flag["ELEMENTS"] = 0
                flag["GROUPS_N"] = 0
                flag["GROUPS_M"] = 0

        for etype, values in ELEMENTS.items():
            nb_nodes = int(re.findall(r"\d+", etype)[0])
            ELEMENTS[etype] = list(chunks(values, 1 + nb_nodes))

        toc = time.perf_counter()
        logger.debug(" File name : %s (parsed in %0.4f seconds)" % (filename, toc - tic))
        logger.debug(" Mesh name : %s" % self.mesh_name)
        logger.debug(" Space Dimension : %d" % self.space_dim)

        # Les noeuds
        tic = time.perf_counter()
        for spline in NODES:
            idx_aster = spline[0]
            coords = tuple(map(float, spline[-self.space_dim :]))
            self.add_node(idx_aster, coords)
        toc = time.perf_counter()
        logger.debug(" Load %d nodes (in %0.4f seconds)" % (len(NODES), toc - tic))

        # Les elements
        e_conv = CellsTypeConverter("ASTER")
        c_renum = ConnectivityRenumberer("ASTER")

        tic = time.perf_counter()
        nb_elements = 0
        for element_aster_type, cells in ELEMENTS.items():
            for spline in cells:
                idx_element_aster = spline[0]
                elements_nodes_aster = spline[1:]

                element_medcoupling_type = e_conv.external_to_medcoupling(element_aster_type)
                element_nodes_med = c_renum.external_to_medcoupling(element_medcoupling_type, elements_nodes_aster)

                self.add_cell(idx_element_aster, element_medcoupling_type, element_nodes_med)
                nb_elements += 1

        toc = time.perf_counter()
        logger.debug(" Load %d cells (in %0.4f seconds)" % (nb_elements, toc - tic))

        # Les groups
        tic = time.perf_counter()
        nb_groups = 0
        for group_name, values in GROUPS_N.items():
            self.add_group_nodes(group_name, values)
            nb_groups += 1
        toc = time.perf_counter()
        logger.debug(" Load %d groups of nodes (in %0.4f seconds)" % (nb_groups, toc - tic))

        tic = time.perf_counter()
        nb_groups = 0
        for group_name, values in GROUPS_M.items():
            self.add_group_cells(group_name, values)
            nb_groups += 1
        toc = time.perf_counter()
        logger.debug(" Load %d groups of cells (in %0.4f seconds)" % (nb_groups, toc - tic))

    def write_aster_mesh(self, filename):
        tic = time.perf_counter()
        with open(filename, "w") as f:
            f.write(self.astermesh)
        toc = time.perf_counter()
        logger.debug("Write ASTER mesh file : %s (in %0.4f seconds)" % (filename, toc - tic))

    def create_aster_mesh(self):
        ENDBLOCK = "FINSF\n%"
        self.astermesh = ""
        logger.debug("Create ASTER mesh.")

        if not (bool(self.cells_continuous) or bool(self.groups_e_continuous)):
            tic = time.perf_counter()
            self._make_continuous()
            toc = time.perf_counter()
            logger.debug("Make continuous (in %0.4f seconds)" % (toc - tic))

        logger.debug(" Mesh name : %s" % self.mesh_name)
        logger.debug(" Space Dimension : %d" % self.space_dim)

        # Noeuds
        tic = time.perf_counter()
        nb_nodes = len(self.nodes)
        nodes_lines = (
            "N%d " % (i + ASTER_NODES_SHIFT) + " ".join(map(repr, node))
            for i, node in enumerate(self.nodes)
        )
        toc = time.perf_counter()
        logger.debug(" Add %d nodes (in %0.4f seconds)" % (nb_nodes, toc - tic))

        # Elements et groupes
        elements_lines = []
        groups_lines = []
        groups_e_ids = {}
        groups_n_ids = {}

        c_renum = ConnectivityRenumberer("ASTER")
        e_conv = CellsTypeConverter("ASTER")

        tic = time.perf_counter()
        elements_by_type = {}
        for j, (medcoupling_type, element_nodes_med) in self.cells_continuous.items():
            elements_by_type.setdefault(medcoupling_type, {})
            elements_by_type[medcoupling_type][j] = element_nodes_med
            toc = time.perf_counter()
        logger.debug(" Rearrange cells by type (in %0.4f seconds)" % (toc - tic))

        tic = time.perf_counter()
        for medcoupling_type in sorted(elements_by_type.keys()):
            aster_type = e_conv.medcoupling_to_external(medcoupling_type)
            elements_lines.append(aster_type)
            for j, element_nodes_med in elements_by_type[medcoupling_type].items():
                element_nodes_med = ["N%d" % (i + ASTER_NODES_SHIFT) for i in element_nodes_med]
                element_nodes_asc = c_renum.medcoupling_to_external(
                    medcoupling_type, element_nodes_med
                )
                elements_lines.append("M%d" % (j + ASTER_CELLS_SHIFT))
                for chunck in chunks(element_nodes_asc, ASTER_MAX_LINE_SIZE):
                    elements_lines.append(" ".join(chunck))
            elements_lines.append(ENDBLOCK)

        nb_elements = len(self.cells_continuous)
        toc = time.perf_counter()
        logger.debug(" Add %d cells (in %0.4f seconds)" % (nb_elements, toc - tic))

        tic = time.perf_counter()
        groups_lines = []
        nb_groups = 1

        for group, values in self.groups_n.items():
            groups_lines.append("GROUP_NO\n%s" % group)
            ids = ["N%d" % (i + ASTER_NODES_SHIFT) for i in values]
            for chunck in chunks(ids, ASTER_MAX_LINE_SIZE):
                groups_lines.append(" ".join(chunck))
            groups_lines.append(ENDBLOCK)
            nb_groups += 1

        for group, values in self.groups_e_continuous.items():
            groups_lines.append("GROUP_MA\n%s" % group)
            ids = ["M%d" % (i + ASTER_CELLS_SHIFT) for i in values]
            for chunck in chunks(ids, ASTER_MAX_LINE_SIZE):
                groups_lines.append(" ".join(chunck))
            groups_lines.append(ENDBLOCK)
            nb_groups += 1

        toc = time.perf_counter()
        logger.debug(" Add %d groups (in %0.4f seconds)" % (nb_groups, toc - tic))

        tic = time.perf_counter()
        # Entete du fichier
        txt_header = "TITRE\n%s\n%s" % (self.mesh_name, ENDBLOCK)

        txt_nodes = "\nCOOR_%dD\n%s\n%s" % (self.space_dim, "\n".join(nodes_lines), ENDBLOCK)
        txt_elements = "\n%s\n" % ("\n".join(elements_lines),)
        txt_groups = "\n".join(groups_lines) if groups_lines else ""

        self.astermesh = "".join((txt_header, txt_nodes, txt_elements, txt_groups, "\nFIN"))
        toc = time.perf_counter()
        logger.debug(" Assembly file (in %0.4f seconds)" % (toc - tic))
