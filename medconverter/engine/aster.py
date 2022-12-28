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

    def read_aster_mesh(self, filename):
        logger.debug("Read ASTER mesh.")

        self._reset_structures()

        def zip_line(line):
            # Restituer la ligne sans champs et les champs à part
            spline = line.split()
            fields = dict(
                i.split("=") for i in spline if ("=" in i and len(i.split("=")) == 2)
            )
            zipped = " ".join((i for i in spline if "=" not in i)).strip()
            return zipped, fields

        def zip_block(block):
            strip = {" =": "=", "= ": "="}
            # Supprimer l'ensemble des espaces avant et après le =
            # Afin d'identifier les champs
            while any(key in block for key in strip.keys()):
                for k, sk in strip.items():
                    block = block.replace(k, sk)
            lines = (line for line in block.split("\n") if len(line) > 0)

            fields = {}
            zipped_lines = []
            for item in lines:
                zipped, flds = zip_line(item)
                if len(zipped) > 0:
                    zipped_lines.append(zipped)
                fields.update(flds)

            block_name = zipped_lines[0]
            block_body = " ".join(zipped_lines[1:]).split()
            return block_name, block_body, fields

        def remove_comments_and_split(fstream):
            comment = "%"
            txt = "\n".join(line.partition(comment)[0].strip() for line in fstream)
            return txt.split("FINSF")

        tic = time.perf_counter()

        with open(filename, "r", encoding=self._get_file_encoding(filename)) as f:
            mesh_blocks = remove_comments_and_split(f)
        toc = time.perf_counter()
        logger.debug(
            " File name : %s (splitted in %0.4f seconds)" % (filename, toc - tic)
        )

        tic = time.perf_counter()
        NODES, ELEMENTS, GROUPS_N, GROUPS_M = [], {}, {}, {}

        self.mesh_name = osp.splitext(osp.split(filename)[-1])[0]
        for block in mesh_blocks:

            bname, bbody, bfields = zip_block(block)

            if bname in ("COOR_3D", "COOR_2D"):
                self.space_dim = int(bname.strip("COOR_").strip("D"))
                NODES = list(chunks(bbody, self.space_dim + 1))

            elif bname in ("GROUP_MA",):
                if "NOM" in bfields:
                    grp_name = bfields["NOM"]
                    GROUPS_M[grp_name] = bbody
                else:
                    grp_name = bbody[0]
                    GROUPS_M[grp_name] = bbody[1:]

            elif bname in ("GROUP_NO",):
                if "NOM" in bfields:
                    grp_name = bfields["NOM"]
                    GROUPS_N[grp_name] = bbody
                else:
                    grp_name = bbody[0]
                    GROUPS_N[grp_name] = bbody[1:]

            elif bname in CellsTypeConverter._aster_to_med.keys():
                etype = bname
                nb_nodes = int(re.findall(r"\d+", etype)[0])
                ELEMENTS.setdefault(etype, [])
                ELEMENTS[etype].extend(list(chunks(bbody, 1 + nb_nodes)))
            else:
                pass

        toc = time.perf_counter()
        logger.debug(
            " Mesh name : %s (parsed in %0.4f seconds)" % (self.mesh_name, toc - tic)
        )
        logger.debug(" Space Dimension : %d" % self.space_dim)

        # Les noeuds
        strip_fortran_notation = lambda s: s.replace("d", "e").replace("D", "E")
        tic = time.perf_counter()
        for spline in NODES:
            idx_aster = spline[0]
            coords = tuple(
                float(strip_fortran_notation(c)) for c in spline[-self.space_dim :]
            )
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

                element_medcoupling_type = e_conv.external_to_medcoupling(
                    element_aster_type
                )
                element_nodes_med = c_renum.external_to_medcoupling(
                    element_medcoupling_type, elements_nodes_aster
                )

                self.add_cell(
                    idx_element_aster, element_medcoupling_type, element_nodes_med
                )
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
        logger.debug(
            " Load %d groups of nodes (in %0.4f seconds)" % (nb_groups, toc - tic)
        )

        tic = time.perf_counter()
        nb_groups = 0
        for group_name, values in GROUPS_M.items():
            self.add_group_cells(group_name, values)
            nb_groups += 1
        toc = time.perf_counter()
        logger.debug(
            " Load %d groups of cells (in %0.4f seconds)" % (nb_groups, toc - tic)
        )

    def write_aster_mesh(self, filename):
        tic = time.perf_counter()
        with open(filename, "w") as f:
            f.write(self.astermesh)
        toc = time.perf_counter()
        logger.debug(
            "Write ASTER mesh file : %s (in %0.4f seconds)" % (filename, toc - tic)
        )

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
                element_nodes_med = [
                    "N%d" % (i + ASTER_NODES_SHIFT) for i in element_nodes_med
                ]
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

        txt_nodes = "\nCOOR_%dD\n%s\n%s" % (
            self.space_dim,
            "\n".join(nodes_lines),
            ENDBLOCK,
        )
        txt_elements = "\n%s\n" % ("\n".join(elements_lines),)
        txt_groups = "\n".join(groups_lines) if groups_lines else ""

        self.astermesh = "".join(
            (txt_header, txt_nodes, txt_elements, txt_groups, "\nFIN")
        )
        toc = time.perf_counter()
        logger.debug(" Assembly file (in %0.4f seconds)" % (toc - tic))
