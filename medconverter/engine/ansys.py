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
#from .ansys_comm import *

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


dicoMod = {
        '5_2'       : 'MECA_3D',
        '5_8'       : 'THER_3D',
        '11'        : 'MECA_BARRE',
        '13'        : 'NONE',
        '13_3_3'    : 'MECA_AXIS',
        '13_3'      : 'MECA_C_PLAN',
        '13_2_3'    : 'THER_PLAN',
        '13_2'      : 'THER_PLAN',
        '14'        : 'MECA_2D_DIS_T',
        '14_0'      : 'MECA_DIS_T',
        '14_1'      : 'MECA_DIS_TR',
        '14_2'      : 'MECA_2D_DIS_T',
        '16'        : 'MECA_POUT_D_T',
        '21'        : 'MECA_2D_DIS_T',
        '21_0'      : 'MECA_DIS_TR',
        '21_2'      : 'MECA_DIS_T',
        '21_3'      : 'MECA_2D_DIST_TR',
        '21_4'      : 'MECA_2D_DIST_T',
        '25_3'      : 'MECA_AXIS',
        '25_4'      : 'MECA_D_PLAN',
        '29_3'      : 'MECA_AXIS',             #???
        '29'        : 'MECA_D_PLAN_HHM',       #???
        '30'        : 'ACOU_3D',
        '31'        : 'THER_AXIS',
        '33'        : 'THER_AXIS',
        '34'        : 'THER_AXIS',
        '35'        : 'THER_PLAN',
        '39'        : 'Elem2D',                #???
        '40'        : 'Discret',               #???
        '40_0'      : 'Discret',               #???
        '40_1'      : 'Discret',               #???
        '40_2'      : 'Discret',               #???
        '40_3'      : 'Discret',               #???
        '40_4'      : 'Discret',               #???
        '40_5'      : 'Discret',               #???
        '40_6'      : 'Discret',               #???
        '40_7'      : 'Discret',               #???
        '40_8'      : 'Discret',               #???
        '42'        : 'MECA_C_PLAN',
        '42_0_3'    : 'MECA_AXIS',
        '42_2_3'    : 'MECA_AXIS',
        '42_0'      : 'MECA_C_PLAN',
        '42_2'      : 'MECA_D_PLAN',
        '45'        : 'MECA_3D',
        '45_0'      : 'MECA_3D',
        '45_1'      : 'MECA_3D',
        '47'        : 'THER_PLAN',
        '47_1'      : 'THER_PLAN',
        '55'        : 'THER_PLAN',
        '59'        : 'MECA_POUT_D_T',
        '59_1'      : 'MECA_CABLE',
        '59_0'      : 'MECA_2D_POUT_D_TR',
        '59_2'      : 'MECA_2D_POUT_D_TR',
        '61'        : 'MECA_COQUE_AXIS',      #???
        '63'        : 'MECA_DKT',
        '65'        : 'MECA_3D',
        '68'        : 'THER_AXIS',
        '70'        : 'THER_3D',
        '71'        : 'Discret',
        '75'        : 'THER_PLAN',
        '77'        : 'THER_PLAN',
        '78'        : 'THER_PLAN',
        '82'        : 'MECA_C_PLAN',
        '83'        : 'MECA_C_PLAN',
        '87'        : 'THER_3D',
        '90'        : 'THER_3D',
        '92'        : 'MECA_3D',
        '95'        : 'MECA_3D',
        '95_0'      : 'MECA_3D',
        '95_1'      : 'MECA_3D',
        '96'        : 'Elem3D',                #???
        '98'        : 'MECA_3D',
        '98_2'      : 'MECA_3D',
        '98_8'      : 'THER_3D',
        '111'       : 'Elem3D',
        '111_3'     : 'THER_3D',
        '116'       : 'THER_AXIS',
        '116_0'     : 'THER_AXIS',
        '116_1'     : 'THER_AXIS',
        '116_2'     : 'Elem3D',
        '116_3'     : 'Elem3D',
        '120'       : 'Elem3D',
        '121'       : 'Elem2D',
        '122'       : 'Elem3D',
        '123'       : 'Elem3D',
        '129'       : 'Discret',
        '131'       : 'THER_COQUE',
        '132'       : 'THER_COQUE',
        '136'       : 'MECA_D_PLAN_HM',
        '138'       : 'Elem2D',
        '143'       : 'Coque',
        '143_0'     : 'Coque',
        '143_1'     : 'Coque',
        '151'       : 'THER_AXIS',
        '152'       : 'THER_PLAN',
        '153'       : 'MECA_AXIS',
        '154'       : 'MECA_3D_ABSO',
        '156'       : 'MECA_AXIS',              #???
        '157'       : 'THER_COQUE',
        '160'       : 'MECA_BARRE',
        '161'       : 'MECA_POU_D_T',
        '162'       : 'Coque',
        '163'       : 'Coque',
        '164'       : 'MECA_3D',
        '164_0'     : 'Elem3D',
        '164_1'     : 'Elem3D',
        '164_2'     : 'Elem3D',
        '165'       : 'MECA_DIST_T',
        '165_0'     : 'MECA_DIST_T',
        '165_1'     : 'MECA_DIST_TR',
        '166'       : 'MECA_DIST_T',
        '167'       : 'MECA_DIST_T',
        '168'       : 'MECA_3D',
        '169'       : 'Discret',
        '170'       : 'Discret',
        '171'       : 'Discret',
        '171_0'     : 'Discret',
        '171_1'     : 'Discret',
        '171_2'     : 'Discret',
        '171_7'     : 'Discret',
        '171_8'     : 'Discret',
        '171_9'     : 'Discret',
        '171_10'    : 'Discret',
        '172'       : 'Discret',
        '172_0'     : 'Discret',
        '172_1'     : 'Discret',
        '172_2'     : 'Discret',
        '172_7'     : 'Discret',
        '172_8'     : 'Discret',
        '172_9'     : 'Discret',
        '172_10'    : 'Discret',
        '173'       : 'Discret',
        '173_0'     : 'Discret',
        '173_1'     : 'Discret',
        '173_2'     : 'Discret',
        '173_8'     : 'Discret',
        '173_9'     : 'Discret',
        '173_10'    : 'Discret',
        '174'       : 'Discret',
        '174_0'     : 'Discret',
        '174_1'     : 'Discret',
        '174_2'     : 'Discret',
        '174_8'     : 'Discret',
        '174_9'     : 'Discret',
        '174_10'    : 'Discret',
        '175'       : 'Discret',
        '175_0'     : 'Discret',
        '175_1'     : 'Discret',
        '175_2'     : 'Discret',
        '175_8'     : 'Discret',
        '175_9'     : 'Discret',
        '175_10'    : 'Discret',
        '176'       : 'Discret',
        '177'       : 'Discret',
        '180'       : 'MECA_BARRE',
        '181'       : 'MECA_DKT',
        '181_0'     : 'MECA_DKT',
        '181_1'     : 'MECA_DKT',
        '182'       : 'MECA_D_PLAN',
        '182_0'     : 'MECA_C_PLAN',
        '182_2'     : 'MECA_D_PLAN',
        '182_3'     : 'MECA_C_PLAN',
        '182_5'     : 'MECA_D_PLAN',
        '183'       : 'MECA_D_PLAN',
        '183_0'     : 'MECA_C_PLAN',
        '183_2'     : 'MECA_D_PLAN',
        '183_3'     : 'MECA_C_PLAN',
        '183_5'     : 'MECA_D_PLAN',
        '184'       : 'MECA_3D_JOINT',
        '185'       : 'MECA_3D_INCO_UP',
        '186'       : 'MECA_3D_INCO_UP',
        '187'       : 'MECA_3D_INCO_UP',
        '188'       : 'MECA_POU_D_EM',
        '189_3'     : 'MECA_POU_D_SQUE',
        '190'       : 'Coque',
        '192'       : 'MECA_PLAN_JOINT',
        '195'       : 'MECA_3D_JOINT',
        '202'       : 'MECA_C_PLAN',
        '202_0'     : 'MECA_C_PLAN',
        '202_2'     : 'MECA_D_PLAN',
        '202_3'     : 'MECA_C_PLAN',
        '204'       : 'MECA_3D',
        '212_3'     : 'MECA_',                         #???
        '212'       : 'MECA_',                         #???
        '213_3'     : 'MECA_D_PLAN_HM',
        '213'       : 'MECA_D_PLAN_HHM',
        '215'       : 'MECA_',                         #???
        '216'       : 'MECA_3D_HM',                    #Forme dégénéré ??
        '217'       : 'Elem3D',
        '218'       : 'MECA_D_PLAN_THH',
        '218_0'     : 'Elem2D',
        '218_1'     : 'MECA_D_PLAN_THH',
        '220'       : 'ACOU_3D',
        '221'       : 'ACOU_3D',
        '223'       : 'Elem2D',
        '223_11'    : 'Elem2D',
        '223_100001': 'Elem2D',
        '223_100010': 'Elem2D',
        '223_100011': 'Elem2D',
        '226'       : 'Elem3D',
        '226_11'    : 'Elem3D',
        '226_100001': 'Elem3D',
        '226_100010': 'Elem3D',
        '226_100011': 'Elem3D',
        '227'       : 'Elem3D',
        '227_11'    : 'Elem3D',
        '227_100001': 'Elem3D',
        '227_100010': 'Elem3D',
        '227_100011': 'Elem3D',
        '230'       : 'Elem2D',
        '231'       : 'Elem3D',
        '232'       : 'Elem3D',
        '233'       : 'Elem2D',
        '236'       : 'Elem3D',
        '237'       : 'Elem3D',
        '238'       : 'Elem2D',
        '239'       : 'Elem3D',
        '240'       : 'Elem3D',
        '251'       : 'Elem2D',
        '252'       : 'Elem2D',
        '278'       : 'Elem3D',
        '279'       : 'Elem3D',
        '281'       : 'MECA_COQUE_3D',      #a verifier
        '281_0'     : 'MECA_COQUE_3D',      #a verifier
        '281_1'     : 'MECA_COQUE_3D',      #a verifier
        '285'       : 'Elem3D',
        '288'       : 'MECA_POU_D_T',
        '289_3'     : 'MECA_TUYAU_3M',
        '290'       : 'MECA_',
}

dicoOpt = {
        '5'  : 1,
        '11' : None,
        '13' : 1,
        '14' : 3,
        '16' : None,
        '21' : 3,
        '25' : None,
        '29' : None,
        '30' : None,
        '31' : None,
        '33' : None,
        '34' : None,
        '35' : None,
        '39' : 4,
        '40' : 3,
        '42' : 3,
        '45' : 2,
        '47' : 1,
        '55' : None,
        '59' : 1,
        '61' : None,
        '63' : None,
        '65' : None,
        '68' : None,
        '70' : None,
        '71' : None,
        '75' : None,
        '77' : None,
        '78' : None,
        '82' : None,
        '83' : None,
        '87' : None,
        '90' : None,
        '92' : None,
        '95' : 11,
        '96' : None,
        '98' : 1,
        '111': 1,
        '116': 1,
        '120': None,
        '121': None,
        '122': None,
        '123': None,
        '129': None,
        '131': None,
        '132': None,
        '136': None,
        '138': None,
        '143': 1,
        '151': None,
        '152': None,
        '153': None,
        '154': None,
        '156': None,
        '157': None,
        '160': None,
        '161': None,
        '162': None,
        '163': None,
        '164': 1,
        '165': 1,
        '166': None,
        '167': None,
        '168': None,
        '169': None,
        '170': None,
        '171': 1,
        '172': 1,
        '173': 1,
        '174': 1,
        '175': 1,
        '176': None,
        '177': None,
        '180': None,
        '181': 1,
        '182': 3,
        '183': 3,
        '184': None,
        '185': None,
        '186': None,
        '187': None,
        '188': None,
        '189': None,
        '190': None,
        '192': None,
        '195': None,
        '202': 3,
        '204': None,
        '212': None,
        '213': None,
        '215': None,
        '216': None,
        '217': None,
        '218': 1,
        '220': None,
        '221': None,
        '223': 1,
        '226': 1,
        '227': 1,
        '230': None,
        '231': None,
        '232': None,
        '233': None,
        '236': None,
        '237': None,
        '238': None,
        '239': None,
        '240': None,
        '251': None,
        '252': None,
        '278': None,
        '279': None,
        '281': 1,
        '285': None,
        '288': None,
        '289': None,
        '290': None,
}


class MedConverterAnsys(MedConverterMesh):

    @staticmethod
    def convert_ansys_to_med(filename_ansys, filename_med, output_comm, verbose = False):

        tic = time.perf_counter()
        c = MedConverterAnsys()
        c.verbose = verbose
        groupsName = c.read_ansys_mesh(filename_ansys)
        c.create_med_mesh()
        c.write_med_mesh(filename_med)
        toc = time.perf_counter()
        logger.debug("Mesh converted (in %0.4f seconds)"%(toc-tic))

        if output_comm is not None:
           c.convert_ansys_data(filename_ansys, output_comm, groupsName)
        


    @staticmethod
    def convert_med_to_ansys(filename_med, filename_ansys, output_comm, verbose = False):

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
        Cells, Groups, GROUPSMODELE, groupsName, title  = [], [], [], [], None
        nb_total_nodes, nb_total_cells = 0, 0
        time_nodes, time_cell, time_groups = 0.0, 0.0, 0.0
        ElemAnsys = {}
        ElemOpt = {}

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
                elif strip_line.startswith("KEYOP"):
                    sspline = strip_line.split(",")
                    ElemOpt[int(sspline[1])] = [int(sspline[2]), int(sspline[3])]
                elif "/TITLE" in line :
                    # Gestion du titre
                    title = line.split(",")[1].strip().replace("\n", '')


        #assert nb_total_nodes == len(self.nodes)
        assert nb_total_cells == len(Cells)


        #Réupération du nom du maillage
        self.mesh_name = title or osp.splitext(osp.split(filename)[-1])[0]

        toc = time.perf_counter()
        logger.debug(" File name : %s (parsed in %0.4f seconds)"%(filename, toc-tic))
        logger.debug(" -> nodes: %d (parsed in %0.4f seconds)"%(len(self.nodes), time_nodes))
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


            if cell.type in ElemOpt and \
               ElemOpt[cell.type][0] == dicoOpt[str(element_ansys_type)] :
                #if element_group_type=='39' and elemOpt[cell.type][1]==0:
                element_group_type=str(element_ansys_type)+ '_' + str(valopt)
            else :
                element_group_type=str(element_ansys_type)
            if nb_nodes == 3 :
                element_group_type=element_group_type + '_' + str(nb_nodes)
            try :
                element_group=dicoMod[element_group_type]
            except (ValueError, TypeError):
                msg="Erreur: Option de l'élément non traitée"
                raise MedConverterError(msg)

            namegroupelem='G_'+element_group
            ajout=0
            compteurgroup=0
            for group in GROUPSMODELE :
                if namegroupelem in group[0]:
                    GROUPSMODELE[compteurgroup].append(cell.id)
                    ajout=1
                compteurgroup +=1
            if ajout==0 :
                GROUPSMODELE.append([namegroupelem])
                GROUPSMODELE[-1].append(cell.id)

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

        for group in GROUPSMODELE :
            self.add_group_cells(group[0], group[1:])
            groupsName.append(group[0])

        toc = time.perf_counter()
        logger.debug(" Load %d groups (in %0.4f seconds)"%(len(Groups), toc-tic))

        return groupsName


    def getCoor(self, line, firstStr, longFloat):
        # le premier decimal commence a la colonne firstStrg
        rline = line.rstrip()[firstStr:]
        elems = [float(rline[i:i+longFloat]) for i in range(0, len(rline), longFloat)]

        nbElem = len(elems)

        if nbElem >= 3:
            return elems[0:3]
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

    def convert_ansys_data(self, ansys_file, comm_file, group_name):

        IndexElem, NODES, ELEMENTS, GROUPS, OPT, SecDat, SecType, DataMatrice, RealConst = [], [], [], [], [], [], [], [], []
        flag={  'indexElem' : 0,
                'Nodes': 0,
                'Elements': 0,
                'Groups': 0,
                'Options': 0,
                'SectionData': 0,
                'SectionType': 0,
                'DataMat': 0,
                'FirstBLOCK': 0,
                'RealConst' : 0
             }

        with open(ansys_file, 'r', encoding = self._get_file_encoding(ansys_file)) as f :

            for line in f:

                if flag['Nodes'] is 1 : 
                    if "(" in line : None 
                    else : NODES.append(line)
                elif flag['Elements'] is 1 : 
                    if "(" in line : None 
                    else : ELEMENTS.append(line)
                elif flag['Groups'] is 1 : 
                    if "(" in line : None 
                    else : GROUPS.append(line)
                                                
                if "SECDATA" in line :
                    flag['SectionData']=1
                elif not "SECDATA" in line :
                    flag['SectionData']=0
                elif "SECTYPE" in line :
                    flag['SectionType']=1
                elif not "SECTYPE" in line :
                    flag['SectionType']=0

                if "NBLOCK" in line :
                    flag['Nodes']=1
                elif "N," in line :
                    flag['Nodes']=0

                if "EBLOCK" in line :
                    flag['Elements']= 1
                elif "CMBLOCK"   in line :
                    flag['Elements']=0
                    flag['Groups']=1
                if flag['FirstBLOCK'] is 0:
                    GROUPS.append(line)
                    flag['FirstBLOCK']=1

                if "KEYOP," in line :
                    flag['Options']=1
                elif not "KEYOP," in line :
                    flag['Options']=0

                if "MPTEMP," in line :
                    flag['Groups']=0
                    flag['Elements']=0
                elif "EXTOPT," in line :
                    flag['Groups']=0
                    flag['Elements']=0
                elif "TREF," in line :
                    flag['Groups']=0
                    flag['Elements']=0

                if flag['Options'] is 1 :
                    OPT.append(line)
                elif flag['SectionData'] is 1:
                    SecDat.append(line)
                elif flag['SectionType'] is 1:
                    SecType.append(line)

                if "RLBLOCK," in line :
                    flag['RealConst']=1
                    nbRl = int(line.split(",")[1])
                    cptRl = 1
                elif flag['RealConst'] is 1 :
                    if "(" in line : None
                    else :
                        if cptRl <= nbRl:
                            RealConst.append(line)
                            cptRl +=1
                        else :
                            flag['RealConst']=0

        with open(comm_file, 'w') as f :

            print(group_name)

            f.write("# coding=utf-8\n\n")
            f.write("DEBUT()\n\n")
            f.write("MA = LIRE_MAILLAGE(FORMAT='MED')\n\n")

            f.write("MO = AFFE_MODELE(MAILLAGE=MA,\n")
            f.write("                 AFFE=(\n")

            for name in group_name :

                if 'MECA' in name:
                    phen='MECANIQUE'
                elif 'THER' in name:
                    phen='THERMIQUE' 
                elif 'ACOU' in name:
                    phen='ACOUSTIQUE'

                f.write("                       _F(GROUP_MA='%s', \n" % name)
                f.write("                          PHENOMENE='%s', \n" % phen)
                f.write("                          MODELISATION='%s'),\n" % name[7:])

            f.write("                      ),\n")
            f.write("                )\n\n")


            f.write("#cara = AFFE_CARA_ELEM(MODELE = MO,\n")
            f.write("\n")






            f.write("FIN()")

    def _get_file_encoding(self, filename):

            encodings = 'utf8 latin_1 cp437'.split()

            for enc in encodings :
                try :
                    with open(filename, mode = 'r', encoding = enc) as f : f.read()
                    return enc
                except UnicodeDecodeError as err:
                    continue

            msg = "File encoding is not among : %s"%(', '.join(encodings))
            print(msg)
