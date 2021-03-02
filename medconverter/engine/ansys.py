#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os.path as osp
from collections import OrderedDict
import medcoupling
import numpy as np

from .logger import logger
from .medconverter import MedConverterMesh
from .errors import MedConverterError
from .cells import CellsTypeConverter
from .connectivity import ConnectivityRenumberer

class AnsysCell:

    def __init__(self, elem_type=None, elem_id=None, elem_nodes=None, sec_id=None, elem_rep=None, elem_const=None, elem_tension=None):
        self.id = elem_id
        if elem_nodes is not None:
            self.nodes = elem_nodes
        else:
            self.nodes = []
        self.type = elem_type
        self.sec = sec_id
        self.rep = elem_rep
        self.const=elem_const
        self.tension=elem_tension

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

class Section:

    def __init__(self, sec_type, sec_subtype, sec_data=None, option=0, courbure=0.0) :
        self.type=sec_type
        self.subtype=sec_subtype

    def setData(self, sec_data):
        self.data=sec_data

    def getAire(self):

        aire=0

        if self.subtype=='RECT':
            aire=self.data[0]*self.data[1]

        elif self.subtype=='HREC':
            rec1=self.data[0]*self.data[1]
            rec2=(self.data[0]-self.data[2]-self.data[3])*(self.data[1]-self.data[4]-self.data[5])
            aire=rec1-rec2

        elif self.subtype=='CSOLID':
            aire=math.pi*(self.data[0])**2

        elif 'CTUB' in self.subtype:
            aire=math.pi*((self.data[1])**2-(self.data[0])**2)

        elif self.subtype=='L' or self.subtype=='T':
            aire=(self.data[0]*self.data[2])+(self.data[1]*self.data[3])\
                 -(self.data[2]*self.data[3])

        elif self.subtype=='QUAD':
            x1=self.data[2]-self.data[0]
            x1prime=self.data[4]-self.data[2]
            y1=self.data[3]-self.data[1]
            y1prime=self.data[5]-self.data[3]
            x2=self.data[6]-self.data[0]
            x2prime=self.data[4]-self.data[6]
            y2=self.data[7]-self.data[1]
            y2prime=self.data[5]-self.data[7]
            tri1=(1/2)*((x1*x1prime)+(y1*y1prime))
            tri2=(1/2)*((x2*x2prime)+(y2*y2prime))
            aire=tri1+tri2

        elif self.subtype=='CHAN' or self.subtype=='I' or self.subtype=='Z':
            rec1=self.data[0]*self.data[3]
            rec2=self.data[1]*self.data[4]
            rec3=self.data[2]*self.data[5]
            supp1=self.data[5]*self.data[4]
            supp2=self.data[5]*self.data[3]
            aire=rec1+rec2+rec3-supp1-supp2

        elif self.subtype=='ASEC':
            aire=data[0]

        elif self.subtype=='HATS':
            rec1=self.data[0]*self.data[4]
            rec2=self.data[1]*self.data[5]
            rec3=self.data[2]*self.data[6]
            rec4=self.data[3]*self.data[7]
            rec5=self.data[3]*self.data[8]
            supp1=self.data[4]*self.data[7]
            supp2=self.data[7]*self.data[6]
            supp3=self.data[6]*self.data[8]
            supp4=self.data[8]*self.data[5]
            aire=rec1+rec2+rec3+rec4+rec5-supp1-supp2-supp3-supp4

        elif self.type=='LINK':
            aire=self.data[0]

        elif self.type=='PIPE':
            aire=math.pi*(self.data[0]**2-(self.data[0]-self.data[1])**2)

        return aire

class Repere:

    def __init__(self, rep_type, orig_data, angle_data) :
        self.type = rep_type
        self.orig = orig_data
        self.angle = angle_data

    def getRep(self, coord_nodes):
        if self.type=='CS':
            x1=coord_nodes[self.angle[0]][0]-coord_nodes[self.orig[0]][0]
            x2=coord_nodes[self.angle[0]][1]-coord_nodes[self.orig[0]][1]
            x3=coord_nodes[self.angle[0]][2]-coord_nodes[self.orig[0]][2]
            y1=coord_nodes[self.angle[1]][0]-coord_nodes[self.orig[0]][0]
            y2=coord_nodes[self.angle[1]][1]-coord_nodes[self.orig[0]][1]
            y3=coord_nodes[self.angle[1]][2]-coord_nodes[self.orig[0]][2]
            return (x1, x2, x3, y1, y2, y3)

        elif self.type=='LOCAL' or 'CLOCAL':
            return (self.angle[0], self.angle[2], self.angle[1])

dicoMod = {
    '5_2'       : 'MMA-3D',
    '5_8'       : 'TMA-3D',
    '11'        : 'MBA-BARRE',
    '13_3_3'    : 'MMA-AXIS',
    '13_3'      : 'MMA-C_PLAN',
    '13_2_3'    : 'TMA-PLAN',
    '13_2'      : 'TMA-PLAN',
    '14'        : 'MDI-DIS_T',
    '14_0'      : 'MDI-DIS_T',
    '14_2'      : 'MDD-2D_DIS_T',
    '16'        : 'MPO-POU_D_T',
    '21'        : 'MDI-DIS_TR',
    '21_0'      : 'MDI-DIS_TR',
    '21_2'      : 'MDI-DIS_T',
    '21_3'      : 'MDD-2D_DIS_TR',
    '21_4'      : 'MDD-2D_DIS_T',
    '25_3'      : 'MMA-AXIS',
    '25_4'      : 'MMA-D_PLAN',
    '29_3'      : 'MMA-AXIS',
    '29'        : 'MMA-D_PLAN_HHM',
    '30'        : 'AMA-3D',
    '31'        : 'TMA-AXIS',
    '33'        : 'TMA-AXIS',
    '34'        : 'TMA-AXIS',
    '35'        : 'TMA-PLAN',
    '39'        : '',
    '40'        : '',
    '40_0'      : '',
    '40_1'      : '',
    '40_2'      : '',
    '40_3'      : '',
    '40_4'      : '',
    '40_5'      : '',
    '40_6'      : '',
    '40_7'      : '',
    '40_8'      : '',
    '42'        : 'MMA-C_PLAN',
    '42_0_3'    : 'MMA-AXIS',
    '42_2_3'    : 'MMA-AXIS',
    '42_0'      : 'MMA-C_PLAN',
    '42_2'      : 'MMA-D_PLAN',
    '45'        : 'MMA-3D',
    '45_0'      : 'MMA-3D',
    '45_1'      : 'MMA-3D',
    '47'        : 'TMA-PLAN',
    '47_1'      : 'TMA-PLAN',
    '55'        : 'TMA-PLAN',
    '59'        : 'MPO-POU_D_T',
    '59_1'      : 'MCA-CABLE',
    '59_0'      : 'MDD-2D_POU_D_TR',
    '59_2'      : 'MDD-2D_POU_D_TR',
    '61'        : 'MCO-COQUE_AXIS',
    '63'        : 'MCO-DKT',
    '65'        : 'MMA-3D',
    '68'        : 'TMA-AXIS',
    '70'        : 'TMA-3D',
    '71'        : '',
    '75'        : 'TMA-PLAN',
    '77'        : 'TMA-PLAN',
    '78'        : 'TMA-PLAN',
    '82'        : 'MMA-C_PLAN',
    '83'        : 'MMA-C_PLAN',
    '87'        : 'TMA-3D',
    '90'        : 'TMA-3D',
    '92'        : 'MMA-3D',
    '95'        : 'MMA-3D',
    '95_0'      : 'MMA-3D',
    '95_1'      : 'MMA-3D',
    '96'        : '',
    '98'        : 'MMA-3D',
    '98_2'      : 'MMA-3D',
    '98_8'      : 'TMA-3D',
    '111'       : '',
    '111_3'     : 'TMA-3D',
    '116'       : 'TMA-AXIS',
    '116_0'     : 'TMA-AXIS',
    '116_1'     : 'TMA-AXIS',
    '116_2'     : '',
    '116_3'     : '',
    '120'       : '',
    '121'       : '',
    '122'       : '',
    '123'       : '',
    '129'       : '',
    '131'       : 'TCO-COQUE',
    '132'       : 'TCO-COQUE',
    '136'       : 'MMA-D_PLAN_HM',
    '138'       : 'Elem2D',
    '143'       : '',
    '143_0'     : '',
    '143_1'     : '',
    '151'       : 'TMA-AXIS',
    '152'       : 'TMA-PLAN',
    '153'       : 'MMA-AXIS',
    '154'       : 'MMA-3D_ABSO',
    '156'       : 'MMA-AXIS',
    '157'       : 'TCO-COQUE',
    '160'       : 'MBA-BARRE',
    '161'       : 'MPO-POU_D_T',
    '162'       : '',
    '163'       : 'MCO-DKT',
    '164'       : 'MMA-3D',
    '164_0'     : '',
    '164_1'     : '',
    '164_2'     : '',
    '165'       : 'MDI-DIS_T',
    '165_0'     : 'MDI-DIS_T',
    '165_1'     : 'MDI-DIS_TR',
    '166'       : 'MDI-DIS_T',
    '167'       : 'MCA-CABLE',
    '168'       : 'MMA-3D',
    '169'       : '',
    '170'       : '',
    '171'       : '',
    '171_0'     : '',
    '171_1'     : '',
    '171_2'     : '',
    '171_7'     : '',
    '171_8'     : '',
    '171_9'     : '',
    '171_10'    : '',
    '172'       : '',
    '172_0'     : '',
    '172_1'     : '',
    '172_2'     : '',
    '172_7'     : '',
    '172_8'     : '',
    '172_9'     : '',
    '172_10'    : '',
    '173'       : '',
    '173_0'     : '',
    '173_1'     : '',
    '173_2'     : '',
    '173_8'     : '',
    '173_9'     : '',
    '173_10'    : '',
    '174'       : '',
    '174_0'     : '',
    '174_1'     : '',
    '174_2'     : '',
    '174_8'     : '',
    '174_9'     : '',
    '174_10'    : '',
    '175'       : '',
    '175_0'     : '',
    '175_1'     : '',
    '175_2'     : '',
    '175_8'     : '',
    '175_9'     : '',
    '175_10'    : '',
    '176'       : '',
    '177'       : '',
    '180_0'     : 'MBA-BARRE',
    '180_1'     : 'MCA-CABLE',
    '181'       : 'MCO-DKT',
    '181_0'     : 'MCO-DKT',
    '181_1'     : 'MCO-DKT',
    '182'       : 'MMA-D_PLAN',
    '182_0'     : 'MMA-C_PLAN',
    '182_2'     : 'MMA-D_PLAN',
    '182_3'     : 'MMA-C_PLAN',
    '182_5'     : 'MMA-D_PLAN',
    '183'       : 'MMA-D_PLAN',
    '183_0'     : 'MMA-C_PLAN',
    '183_2'     : 'MMA-D_PLAN',
    '183_3'     : 'MMA-C_PLAN',
    '183_5'     : 'MMA-D_PLAN',
    '184'       : 'MPO-POU_D_T',
    '185'       : 'MMA-3D',
    '186'       : 'MMA-3D',
    '187'       : 'MMA-3D',
    '188'       : 'MPO-POU_D_T',
    '189_3'     : 'MPO-TUYAU_3M',
    '190'       : 'Coque',
    '192'       : 'M-PLAN_JOINT',
    '195'       : 'M-3D_JOINT',
    '202'       : 'MMA-C_PLAN',
    '202_0'     : 'MMA-C_PLAN',
    '202_2'     : 'MMA-D_PLAN',
    '202_3'     : 'MMA-C_PLAN',
    '204'       : 'MMA-3D',
    '212_3'     : '',
    '212'       : '',
    '213_3'     : 'M-D_PLAN_HM',
    '213'       : 'M-D_PLAN_HHM',
    '215'       : '',
    '216'       : 'M-3D_HM',
    '217'       : '',
    '218'       : 'M-D_PLAN_THH',
    '218_0'     : '',
    '218_1'     : 'M-D_PLAN_THH',
    '220'       : 'AMA-3D',
    '221'       : 'AMA-3D',
    '223'       : '',
    '223_11'    : '',
    '223_100001': '',
    '223_100010': '',
    '223_100011': '',
    '226'       : '',
    '226_11'    : '',
    '226_100001': '',
    '226_100010': '',
    '226_100011': '',
    '227'       : '',
    '227_11'    : '',
    '227_100001': '',
    '227_100010': '',
    '227_100011': '',
    '230'       : '',
    '231'       : '',
    '232'       : '',
    '233'       : '',
    '236'       : '',
    '237'       : '',
    '238'       : '',
    '239'       : '',
    '240'       : '',
    '251'       : '',
    '252'       : '',
    '278'       : '',
    '279'       : '',
    '281'       : 'MCO-COQUE_3D',
    '281_0'     : 'MCO-COQUE_3D',
    '281_1'     : 'MCO-COQUE_3D',
    '285'       : '',
    '288'       : 'MPO-POU_D_T',
    '289_3'     : 'MPO-TUYAU_3M',
    '290'       : 'MPO-TUYAU_3M',
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

#Conversion de la modélisation vers le mot clé adapté dans AFFE_CARA_ELEM
dicoKeyword = {
    #MECA
    'BARRE'        : 'BARRE',
    'CABLE_GAINE'  : 'BARRE',
    'CABLE'        : 'CABLE',
    'CALBE_POULIE' : 'CABLE',
    'COUE_AXIS'    : 'COQUE',
    'COQUE_C_PLAN' : 'COQUE',
    'COQUE_D_PLAN' : 'COQUE',
    'DKT'          : 'COQUE',
    'DST'          : 'COQUE',
    'DKQ'          : 'COQUE',
    'DSQ'          : 'COQUE',
    'Q4G'          : 'COQUE',
    'COQUE_3D'     : 'COQUE',
    'DKTG'         : 'COQUE',
    'Q4GG'         : 'COQUE',
    'DIS_T'        : 'DISCRET',
    'DIS_TR'       : 'DISCRET',
    '2D_DIS_T'     : 'DISCRET_2D',
    '2D_DIS_TR'    : 'DISCRET_2D',
    'POU_D_E'      : 'POUTRE',
    'POU_D_T'      : 'POUTRE',
    'POU_D_TG'     : 'POUTRE',
    'POU_D_T_GD'   : 'POUTRE',
    'FLUI_STRU'    : 'POUTRE',
    'TUYAU_3M'     : 'POUTRE',
    'TUYAY_6M'     : 'POUTRE',
    'POU_D_EM'     : 'POUTRE',
    'POU_D_TGM'    : 'POUTRE',
    '3D'           : 'MASSIF',
    'AXIS'         : 'MASSIF',
    'AXIS_FOURIER' : 'MASSIF',
    'C_PLAN'       : 'MASSIF',
    'D_PLAN'       : 'MASSIF',
    'TUYAU_3M'     : 'POUTRE',
    'TUYAU_6M'     : 'POUTRE',
    'POU_D_EM'     : 'POUTRE',
    #THER
    'COQUE'        : 'COQUE',
    'COQUE_PLAN'   : 'COQUE',
    'PLAN'         : 'MASSIF',
    #NONE
    '3D_INCO_UP'   : None,
    '3D_JOINT'     : None,
    'POU_D_SQUE'   : None,
}


class MedConverterAnsys(MedConverterMesh):

    @staticmethod
    def convert_ansys_to_med(filename_ansys, filename_med, output_comm, verbose = False):

        tic = time.perf_counter()
        c = MedConverterAnsys()
        c.verbose = verbose
        data_read = c.read_ansys_mesh(filename_ansys)
        c.create_med_mesh()
        c.write_med_mesh(filename_med)
        toc = time.perf_counter()
        logger.debug("Mesh converted (in %0.4f seconds)"%(toc-tic))

        if output_comm is not None:
           c.convert_ansys_data(filename_ansys, output_comm, data_read) 

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
        Cells, Groups, groupsName, title  = [], [], [], None
        nb_total_nodes, nb_total_cells, last_idx_sec, last_idx_rep, const_len = 0, 0, 0, 0, 0
        time_nodes, time_cell, time_groups = 0.0, 0.0, 0.0
        ElemAnsys = {}
        ElemOpt = {}
        Sect= {}
        Rep = {}
        RealConst = {}
        tension_init = {}
        tension = {}
        rep_global=0
        nodes = {}
        Orien_coque = np.zeros((1,3), dtype=float)
        Orien_poutre = np.zeros((1,3), dtype=float)
        epais = np.zeros((1,1), dtype=float)
        GROUPSMODELE = {}

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
                    nodes=self.__read_nodes(file, nodes)
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
                elif strip_line.startswith("SECTYPE") :
                    sspline = strip_line.split(",")
                    Sect[int(sspline[1])]=Section(sspline[2], sspline[3].strip())
                    last_idx_sec=int(sspline[1])
                elif strip_line.startswith("SECDATA") :
                    sspline = strip_line.split(",")
                    if sspline[-1]=="":
                        sspline.pop(-1)
                    data=[float(i) for i in sspline[1:]]
                    Sect[last_idx_sec].setData(data)
                elif strip_line.startswith("SECBLOCK") :
                    sspline = strip_line.split(",")
                    for i in range(int(sspline[1])):
                        nextLine = next(file)
                        next_strip=nextLine.strip()
                        snext=next_strip.split(",")
                        data=[float(i) for i in snext[0:-1]]
                        Sect[last_idx_sec].setData(data)
                        line=nextLine
                elif strip_line.startswith("SECCONTROL"):
                    sspline = strip_line.split(",")
                    if len(sspline)>2:
                        tmp=float(sspline[2].strip())
                        Sect[last_idx_sec].option=int(tmp)
                elif strip_line.startswith("inis,set,csys"):
                    sspline=strip_line.split(",")
                    snext=next(file).strip()
                    ssnext=snext.split(",")
                    if float(ssnext[6]) not in tension_init:
                        tension_init[float(ssnext[6])]=len(tension_init)+1
                    tension[int(ssnext[2])]=float(ssnext[6])
                elif strip_line.startswith("RLBLOCK") :
                    sspline = strip_line.split(",")
                    for i in range(int(sspline[1])+2):
                        nextLine=next(file)
                        if nextLine.startswith("("):
                            line=nextLine
                        else :
                            snext=nextLine.split()
                            if int(snext[1]) > const_len:
                                    const_len = int(snext[1])
                            tmp=float(snext[0])
                            RealConst[int(tmp)]=[float(i) for i in snext[1:]]
                        line=nextLine
                elif (strip_line.startswith("LOCAL") or strip_line.startswith("CLOCAL") or \
                     strip_line.startswith("CS,")):
                    sspline=strip_line.split(",")
                    nextLine=next(file)
                    next_strip=nextLine.strip()
                    snext=next_strip.split(",")
                    data1=[float(i) for i in sspline[5:]]
                    data2=[float(j) for j in snext[5:]]
                    Rep[int(sspline[3])]=Repere(sspline[0], data1, data2)
                    last_idx_rep=int(sspline[3])
                    for i in range(2):
                        nextLine=next(file)
                    line=nextLine
                elif strip_line.startswith("ESYS"):
                    sspline = strip_line.split(",")
                    rep_global=int(sspline[1])
                elif "/TITLE" in line :
                    # Gestion du titre
                    title = line.split(",")[1].strip().replace("\n", '')


        const=np.zeros((1, const_len), dtype=float)
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
                msg="Présence de noeuds orphelins"
            else:
                nb_nodes = len(cell.nodes)

            if cell.type in ElemOpt and \
               ElemOpt[cell.type][0] == dicoOpt[str(element_ansys_type)] :
                element_group_type=str(element_ansys_type)+ '_' + str(ElemOpt[cell.type][1])
            else :
                element_group_type=str(element_ansys_type)
            if nb_nodes==3 :
                element_group_type=element_group_type + '_' + str(nb_nodes)
            if element_group_type=='180':
                element_group_type=element_group_type+'_'+str(Sect[cell.sec].option)
            try :
                element_group=dicoMod[element_group_type]
            except (ValueError, TypeError):
                msg="Erreur: Option de l'élément non traitée"
                raise MedConverterError(msg)

            namegroupelem=element_group
            #Récupération des caractéristiques des éléments discrets
            if dicoKeyword[element_group[4:]]=="DISCRET" or dicoKeyword[element_group[4:]]=="DISCRET_2D":
                const_index=np.where((const==RealConst[cell.const][1:]).all(axis=1))
                if len(const_index[0])>0 :
                    const_id=const_index[0][0]
                else :
                    const_id=len(const)
                    const=np.append(const, [RealConst[cell.const][1:]], axis=0)
                if str(ElemAnsys[cell.type]) in ('21', '166') and cell.type in ElemOpt:
                    namegroupelem=namegroupelem+'-'+str(cell.rep)+'-'+str(const_id)+'-M'+str(ElemOpt[cell.type][1])
                elif str(ElemAnsys[cell.type]) in  ('21', '166') and cell.type not in ElemOpt:
                    namegroupelem=namegroupelem+'-'+str(cell.rep)+'-'+str(const_id)+'-M0'
                elif str(ElemAnsys[cell.type])=='14':
                    if ElemOpt[cell.type][0]==2 and ElemOpt[cell.type][1]==1:
                        namegroupelem=namegroupelem+'-'+str(cell.rep)+'-'+str(const_id)+'-Kx'
                    elif ElemOpt[cell.type][0]==2 and ElemOpt[cell.type][1]==2:
                        namegroupelem=namegroupelem+'-'+str(cell.rep)+'-'+str(const_id)+'-Ky'
                    elif ElemOpt[cell.type][0]==2 and ElemOpt[cell.type][1]==3:
                        namegroupelem=namegroupelem+'-'+str(cell.rep)+'-'+str(const_id)+'-Kz'

            #Calcul des axes X et Y du plan tangent des éléments coque
            if dicoKeyword[element_group[4:]]=='COQUE':
                namegroupelem=namegroupelem+'-'+str(cell.rep)
                i=cell.sec
                epais_index_real=np.where((epais==RealConst[cell.const][1]))
                if i in Sect and Sect[i].type=='SHELL':
                    epais_index=np.where((epais==Sect[i].data[0]))
                    if len(epais_index[0])>0:
                        id_orien=epais_index[0][0]
                    else :
                        id_epais=len(epais)
                        epais=np.append(epais, Sect[i].data[0])
                elif len(epais_index_real[0])>0:
                    id_epais=epais_index_real[0][0]
                else :
                    id_epais=len(epais)
                    epais=np.append(epais, RealConst[cell.const][1])

                namegroupelem=namegroupelem+'-'+str(id_epais)

                if (cell.rep==0 or cell.rep==rep_global):
                    
                    x1=nodes[cell.nodes[1]]
                    o1=nodes[cell.nodes[0]]
                    y1=nodes[cell.nodes[2]]

                    xx=x1[0]-o1[0]
                    xy=x1[1]-o1[1]
                    xz=x1[2]-o1[2]
                    yx=y1[0]-o1[0]
                    yy=y1[1]-o1[1]
                    yz=y1[2]-o1[2]
                    x=np.array([xx, xy, xz])
                    y=np.array([yx, yy, yz])

                    z=np.cross(x, y)

                    vale_c=np.around(np.add(x,z), decimals=2)

                    index_orien=np.where((Orien_coque==vale_c).all(axis=1))
                    index2_orien=np.where((np.cross(Orien_coque[1:], vale_c)==[[0.0, 0.0, 0.0]]).all(axis=1))
                    if len(index_orien[0])>0 :
                        id_orien=index_orien[0][0]
                    elif len(index2_orien[0])>0:
                        id_orien=index2_orien[0][0]
                    else:
                        id_orien=len(Orien_coque)
                        Orien_coque=np.append(Orien_coque, [vale_c], axis=0)

                    namegroupelem=namegroupelem+'-'+str(id_orien)

            #Orientation des poutres à partir du noeud optionnel
            elif dicoKeyword[element_group[4:]]=='POUTRE':
                namegroupelem=namegroupelem+'-'+str(cell.rep)+'-'+str(cell.sec)
                o2=nodes[cell.nodes[0]]
                if element_ansys_test in ("188_3", "189_4", "288_3", "289_4"):
                    x2=nodes[cell.nodes[len(cell.nodes)-1]]
                    x=x2[0]-o2[0]
                    y=x2[1]-o2[1]
                    z=x2[2]-o2[2]

                    vale_p=np.around(np.array([x,y,z]), decimals=2)

                    index_orien=np.where((Orien_poutre==vale_p).all(axis=1))
                    index2_orien=np.where((np.cross(Orien_poutre[1:], vale_p)==[0.0, 0.0, 0.0]).all(axis=1))
                    if len(index_orien[0])>0:
                        id_orien=index_orien[0][0]
                    elif len(index2_orien[0])>0:
                        id_orien=index2_orien[0][0]
                    else:
                        id_orien=len(Orien_poutre)
                        Orien_poutre=np.append(Orien_poutre, [vale_p], axis=0)

                    namegroupelem=namegroupelem+"-"+str(id_orien)

                #Courbure élements courbes
                if element_ansys_test in ("189", "289"):
                    x=(o2[0]-nodes[cell.nodes[2]][0])**2
                    y=(o2[1]-nodes[cell.nodes[2]][1])**2
                    z=(o2[2]-nodes[cell.nodes[2]][2])**2
                    dist_PB=sqrt(x+y+z)/2
                    x1=(nodes[cell.nodes[1]][0]-o2[0])**2
                    y1=(nodes[cell.nodes[1]][1]-o2[1])**2
                    z1=(nodes[cell.nodes[1]][2]-o2[2])**2
                    dist_CB=sqrt(x1+y1+z1)
                    courbure=cos(2*asin(dist_PB/dist_CB)-(math.pi/2))/dist_PB

                    if abs(courbure)>0.005:
                        Sect[cell.sec].courbure=courbure

            elif dicoKeyword[element_group[4:]]=='BARRE':
                namegroupelem=namegroupelem+'-'+str(cell.sec)

            elif dicoKeyword[element_group[4:]]=='CABLE':
                namegroupelem=namegroupelem+'-'+str(cell.sec)+'-'+str(tension_init[tension[cell.id]])

            elif dicoKeyword[element_group[4:]]=='MASSIF':
                namegroupelem=namegroupelem+'-'+str(cell.rep)

            if namegroupelem in GROUPSMODELE:
                GROUPSMODELE[namegroupelem].append(cell.id)
            else:
                GROUPSMODELE[namegroupelem]=[cell.id]

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
            groupsName.append(group)
            rname=group.replace('-', '_')
            self.add_group_cells(rname, GROUPSMODELE[group])

        toc = time.perf_counter()
        logger.debug(" Load %d groups (in %0.4f seconds)"%(len(Groups), toc-tic))

        data_read=(groupsName, nodes, Orien_coque, Orien_poutre, const, Rep, Sect, RealConst, epais, tension_init, rep_global)

        #Recuperation des informations de la mise en donnees pour la creation du fichier de commandes
        return data_read


    def getCoor(self, line, firstStr, longFloat):
        # le premier decimal commence a la colonne firstStrg
        rline = line.rstrip()[firstStr:]
        elems = [float(rline[i:i+longFloat]) for i in range(0, len(rline), longFloat)]

        nbElem = len(elems)

        if nbElem >= 3:
            return elems[0:3]
        else:
            return elems + [0.0]*(3-nbElem)

    def __read_nodes(self, file, nodes):
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
                nodes[int(spline[0])]=self.getCoor(line, firstStr, LongFloat)
        return nodes

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
                    sec = enum[3]
                    rep = enum[4]
                    const = enum[2]
                    if len(cnodes) < nb_nodes:
                        l_new_cell = False
                else:
                    cnodes += enum
                    if len(cnodes) == nb_nodes:
                        l_new_cell = True

                if l_new_cell:
                    assert len(cnodes) == nb_nodes
                    Cells.append(AnsysCell(ctype, cid, cnodes, sec, rep, const))

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

    def write_cara_elems(self, f, modele_name, group_name, data_read):

        nodes=data_read[1]
        orien_coque=data_read[2]
        orien_poutre=data_read[3]
        const=data_read[4]
        Rep=data_read[5]
        Sect=data_read[6]
        RealConst=data_read[7]
        epais=data_read[8]
        tension_init=data_read[9]
        rep_global=data_read[10]

        if 'MECA' in modele_name:
            f.write("CARA_M=AFFE_CARA_ELEM(MODELE={},\n".format(modele_name))
        elif 'ACOU' in modele_name:
            f.write("CARA_A=AFFE_CARA_ELEM(MODELE={},\n".format(modele_name))
        elif 'THER' in modele_name:
            f.write("CARA_T=AFFE_CARA_ELEM(MODELE={},\n".format(modele_name))
        elif 'COQUE' in modele_name:
            f.write("CARA_C=AFFE_CARA_ELEM(MODELE={},\n".format(modele_name))

        #Drapeaux de debut de mot-cle des elements
        flag=[False, False, False, False, False, False, False, False]
        parenthese=False
        orientation=[]
        groupname=sorted(group_name)

        orientation.append("{:>22}ORIENTATION=(".format(" "))
        for name in groupname:

            sname=name.split("-")
            rname=name.replace("-", "_")

            if dicoKeyword[sname[1]] is 'COQUE' :
                if flag[0]==False:
                    if parenthese==True:
                        f.write("{0:>26}),\n".format(" "))
                        parenthese=False
                    f.write("{0:>22}COQUE=(_F(GROUP_MA='{1}', EPAIS={2}, ".format(" ", rname, epais[int(sname[3])]))
                    parenthese=True
                    flag[0]=True
                else :
                    f.write("{0:>29}_F(GROUP_MA='{1}', EPAIS={2}, ".format(" ", rname, epais[int(sname[3])]))

                k=int(sname[2])
                if k in Rep and k!=rep_global:
                    if Rep[k].type=='LOCAL' or Rep[k].type=='CLOCAL':
                        f.write("ANGL_REP={},),\n".format(Rep[k].getRep(nodes)))
                    elif  Rep[k].type=='CS':
                        f.write("VECTEUR={},),\n".format(Rep[k].getRep(nodes)))
                else :
                    k=int(sname[4])
                    f.write("VECTEUR=({0}, {1}, {2}),),\n".format(orien_coque[k][0], orien_coque[k][1], orien_coque[k][2]))

            elif dicoKeyword[sname[1]] is 'POUTRE' :
                if flag[1]==False:
                    if parenthese==True:
                        f.write("{0:>28}),\n".format(" "))
                        parenthese=False
                    f.write("{0:>22}POUTRE=(_F(GROUP_MA='{1}', ".format(" ", rname))
                    parenthese=True
                    flag[1]=True
                else :
                    f.write("{0:>30}_F(GROUP_MA='{1}', ".format(" ", rname))
                i=int(sname[3])
                if i in Sect and Sect[i].type=='BEAM':
                    if Sect[i].subtype == 'RECT' :
                        f.write("SECTION='RECTANGLE', VARI_SECT='CONSTANT', CARA=('HY', 'HZ'), VALE=({}),),\
                                \n".format(Sect[i].data[0], Sect[i].data[1]))
                    elif Sect[i].subtype == 'QUAD' :
                        hy1=math.sqrt((Sect[i].data[0]-Sect[i].data[2])**2+(Sect[i].data[1]-Sect[i].data[3])**2)
                        hy2=math.sqrt((Sect[i].data[4]-Sect[i].data[6])**2+(Sect[i].data[5]-Sect[i].data[7])**2)
                        hz1=math.sqrt((Sect[i].data[0]-Sect[i].data[6])**2+(Sect[i].data[1]-Sect[i].data[7])**2)
                        hz2=math.sqrt((Sect[i].data[2]-Sect[i].data[4])**2+(Sect[i].data[3]-Sect[i].data[5])**2)
                        vale=(hy1, hy2, hz1, hz2)
                        f.write("SECTION='RECTANGLE', VARI_SECT='HOMOTHETIQUE', CARA=('HY1', 'HY2', 'HZ1', 'HZ2'), VALE=({}),),\
                                \n".format(vale))
                    elif Sect[i].subtype == 'HREC':
                        f.write("SECTION='RECTANGLE', VARI_SECT='HOMOTHETIQUE', CARA=('HY1', 'HZ1', 'HY2', 'HZ2', 'EPY1', 'EPY2', 'EPZ1', EPZ2'), VALE=({}),),\
                                \n".format(Sect[i].data[:]))
                    elif Sect[i].subtype == 'CSOLID':
                        f.write("SECTION='CERCLE', VARI_SECT='CONSTANT', CARA=('R'), VALE=({}),),\n".format(Sect[i].data[0]))
                    elif 'CTUB' in Sect[i].subtype:
                        f.write("SECTION='CERCLE', VARI_SECT='CONSTANT', CARA=('R', 'EP'), VALE={},),\
                                \n".format((Sect[i].data[1], Sect[i].data[1]-Sect[i].data[0])))
                    elif Sect[i].subtype =='ASEC':
                        f.write("SECTION='GENERALE', CARA=('A', 'IY', 'IZ', 'AY', 'AZ', 'EY', 'EZ', 'JX', 'JG', 'IYR2', 'IZR2'), VALE=({}),),\
                                \n".format(Sect[i].data[0], Sect[i].data[1], Sect[i].data[3], \
                                Sect[i].data[8], Sect[i].data[9], Sect[i].data[6], Sect[i].data[7],\
                                Sect[i].data[5], Sect[i].data[4], Sect[i].data[11], Sect[i].data[10]))
                    elif Sect[i].subtype in ('I', 'L', 'T', 'Z', 'CHAN', 'HATS'):
                        raise MedConverterError("Section non traitée")
                    else :
                        raise MedConverterError("Section non reconnue")
                elif i in Sect and Sect[i].type=='PIPE':
                    f.write("SECTION='CERCLE', VARI_SECT='CONSTANT', CARA=('R', 'EP'), VALE=({}),),\
                            \n".format(Sect[i].data[0], ", ", Sect[i].data[1]))

                i=int(sname[2])
                if flag[7]==False:
                    orientation.append("_F(GROUP_MA='{}', ".format(rname))
                    flag[7]=True
                else:
                    orientation.append("{:>35}_F(GROUP_MA='{}', ".format(" ", rname))
                if rep_global==0 and len(sname)>4:
                    k=int(sname[4])
                    orientation.append("CARA='VECT_Y', VALE=({0}, {1} ,{2}),),\n".\
                            format(orien_poutre[k][0], orien_poutre[k][1], orien_poutre[k][2]))
                elif i in Rep and (Rep[i].type=='LOCAL' or Rep[i]=='CLOCAL' or i==rep_global):
                    orientation.append("CARA='ANGL_VRIL', VALE={},),\n".format(Rep[i].getRep(nodes)[1]))
                elif i in Rep and (Rep[i].type=='CS'):
                    orientation.append("CARA='VECT_Y', VALE={},),\n".format(Rep[i].getRep(nodes)[3:5]))
                elif rep_global==0:
                    orientation.append("CARA='ANGL_VRIL', VALE=0.0,),\n")

            elif dicoKeyword[sname[1]] is 'DISCRET' :
                if flag[2]==False:
                    if parenthese==True:
                        f.write("{0:>29}),\n".format(" "))
                        parenthese=False
                    f.write("{0:>22}DISCRET=(_F(GROUP_MA='{1}', ".format(" ", rname))
                    parenthese=True
                    flag[2]=True
                else:
                    f.write("{:>31}_F(GROUP_MA='{}', ".format(" ", rname))
                idx=int(sname[3])
                if sname[4]=='Kx':
                    f.write("CARA='K_T_D_L', VALE={}, ".format((const[idx][0], 0.0, 0.0)))
                elif sname[4]=='Ky':
                    f.write("CARA='K_T_D_L', VALE={}, ".format((0.0, const[idx][0], 0.0)))
                elif sname[4]=='Kz':
                    f.write("CARA='K_T_D_L', VALE={}, ".format((0.0, 0.0, const[idx][0])))
                elif sname[4]=='M2':
                    f.write("CARA='M_T_D_N', VALE={}, ".format(const[idx][0]))
                elif sname[4]=='M0':
                    f.write("CARA='M_TR_N', VALE={}, ".format((const[idx][0], const[idx][1], \
                            const[idx][1], const[idx][2], const[idx][2], const[idx][2],\
                            const[idx][3], const[idx][3], const[idx][3], const[idx][3],\
                            const[idx][4], const[idx][4], const[idx][4], const[idx][4],\
                            const[idx][5], const[idx][5], const[idx][5], const[idx][5],\
                            const[idx][5], const[idx][5], const[idx][5],)))
                if rep_global==0 or int(sname[3])==rep_global:
                    f.write("REPERE='GLOBAL'),\n")
                else :
                    f.write("REPERE='LOCAL'),\n")
                    if flag[7]==False:
                        orientation.append("_F(GROUP_MA='{}' ,".format(rname))
                        flag[7]=True
                    else :
                        orientation.append("{:>34}_F(GROUP_MA='{}' ,".format(" ", rname))
                    i=int(sname[2])
                    if i in Rep and (Rep[i].type=='LOCAL' or Rep[i]=='CLOCAL' or i==rep_global):
                        orientation.append("CARA='ANGL_NAUT', VALE={},),\n".format(Rep[i].getRep(nodes)))
                    elif i in Rep and (Rep[i].type=='CS'):
                        orientation.append("CARA='VECT_X_Y', VALE={},),\n".format(Rep[i].getRep(nodes)))

            elif dicoKeyword[sname[1]] is 'DISCRET_2D' :
                if flag[3]==False:
                    if parenthese==True:
                        f.write("{0:>31}),\n".format(" "))
                        parenthese=False
                    f.write("{0:>22}DISCRET_2D=(_F(GROUP_MA='{1}', ".format(" ", rname))
                    parenthese=True
                    flag[3]=True
                else:
                    f.write("{0:>35}_F(GROUP_MA='{1}', ".format(" ", rname))
                idx=int(sname[3])
                if sname[4]=='Kx':
                    f.write("CARA='K_T_D_L', VALE=({0}, {1}), ".format((const[idx][0], 0.0)))
                elif sname[4]=='Ky':
                    f.write("CARA='K_T_D_L', VALE=({0}, {1}), ".format((0.0, const[idx][0])))
                elif sname[4]=='M4':
                    f.write("CARA='M_T_D_N', VALE={0}, ".format(const[idx][0]))
                elif sname[4]=='M3':
                    f.write("CARA='M_TR_N', VALE=({0}, {1}, {2}, {3}, {4}, {5} ".format(const[idx][0],\
                            const[idx][0], const[idx][0], const[idx][1], \
                            const[idx][1], const[idx][1]))
                if rep_global==0 or int(sname[2])==rep_global:
                    f.write("REPERE='GLOBAL'),\n")
                else:
                    f.write("REPERE='LOCAL'),\n")
                    if flag[7]==False:
                        orientation.append("_F(GROUP_MA='{}', ".format(rname))
                        flag[7]=True
                    else :
                        orientation.append("{0:>35}_F(GROUP_MA='{1}', ".format(" ", rname))
                    i=int(sname[2])
                    if i in Rep and (Rep[i].type=='LOCAL' or Rep[i]=='CLOCAL' or i==rep_global):
                        orientation.append("CARA='ANGL_NAUT', VALE={},),\n".format(Rep[i].getRep(nodes)))
                    elif i in Rep and (Rep[i].type=='CS'):
                        orientation.append("CARA='VECT_X_Y', VALE={},),\n".format(Rep[i].getRep(nodes)))

            elif dicoKeyword[sname[1]] is 'BARRE' :
                if flag[4]==False:
                    f.write("{0:>22}BARRE=(_F(GROUP_MA='{1}', ".format(" ", rname))
                    parenthese=True
                    flag[4]=True
                else :
                    f.write("{0:>29}_F(GROUP_MA='{1}', ".format(" ", rname))
                i=int(sname[2])
                if i in Sect:
                    f.write("SECTION='GENERALE', CARA='A', VALE={}),\n".format(Sect[i].getAire()))

            elif dicoKeyword[sname[1]] is 'CABLE':
                if flag[5]==False:
                    if parenthese==True:
                        f.write("{0:>26}),\n".format(" "))
                        parenthese=False
                    f.write("{0:>22}CABLE=(_F(GROUP_MA='{1}', ".format(" ", rname))
                    parenthese=True
                    flag[5]=True
                else:
                    f.write("{0:>29}_F(GROUP_MA='{1}', ".format(" ", rname))

                i=int(sname[2])
                if i in Sect:
                    present=False
                    for c, v in tension_init.items():
                        if int(sname[3])==v:
                            f.write("SECTION={0}, N_INIT={1}),\n".format(Sect[i].getAire(), c))
                            present=True
                            break
                    if present==False:
                        f.write("SECTION={0}, N_INIT={1}),\n".format(Sect[i].getAire(), 0.0))

            elif dicoKeyword[sname[1]] is 'MASSIF':
                i=int(sname[2])
                if flag[6]==False:
                    if parenthese==True:
                        f.write("{0:>28},)\n".format(" "))
                        parenthese=False
                    f.write("{0:>22}MASSIF=(_F(GROUP_MA='{1}', ".format(" ", rname))
                    parenthese=False
                    flag[6]=True
                else :
                    f.write("{0:>30}_F(GROUP_MA='{1}', ".format(" ", rname))
                if rep_global==0 and i==0:
                    f.write("{}ANGL_EULER=(0, 0, 0),)\n".format(" "))
                else:
                    if i in Rep and (Rep[i].type=='LOCAL' or Rep[i].type=='CLOCAL' or i==rep_global):
                        f.write("ANGL_EULER={},),\n".format(Rep[i].getRep(nodes)))
                    elif i in Rep and (Rep[i].type=='CS'):
                        f.write("ANGL_EULER={},),\n".format(Rep[i].getRep(nodes)))

        if parenthese==True:
            f.write("{0:>28},)\n".format(" "))
            parenthese=False


        if len(orientation)>1:
            for s in orientation:
                f.write(s)
            f.write("{0:>34}),\n".format(" "))
        f.write("{0:>32}),\n{0:>21})\n\n".format(" "))

    def convert_ansys_data(self, ansys_file, comm_file, data_read):

        group_name=data_read[0]
        nodes=data_read[1]
        orien_coque=data_read[2]
        orien_poutre=data_read[3]
        const=data_read[4]
        Rep=data_read[5]
        Sect=data_read[6]
        RealConst=data_read[7]
        epais=data_read[8]
        tension_init=data_read[9]
        rep_global=data_read[10]

        with open(comm_file, 'w') as f :

            coque=False
            coque_name=[]
            flag=[False, False, False]
            meca_name=[]
            ther_name=[]
            acou_name=[]

            groupname=sorted(group_name)

            for name in groupname :

                sname=name.split("-")
                rname=name.replace("-", "_")

                if sname[1]=='COQUE_3D':
                    coque_name.append(name)
                    coque=True
                else :
                    if sname[0][0]=='M' and flag[0]==False:
                        f.write("MO_MECA=AFFE_MODELE(MAILLAGE=MA,\n{0:>20}AFFE=(\n".format(" "))
                        flag[0]=True
                        f.write("{0:>26}_F(GROUP_MA='{1}',\n{0:>28}PHENOMENE='MECANIQUE',\
                                \n{0:>29}MODELISATION='{2}'),\n ".format(" ", rname, sname[1]))
                        meca_name.append(name)
                    elif sname[0][0]=='M':
                        f.write("{0:>26}_F(GROUP_MA='{1}',\n {0:>28}PHENOMENE='MECANIQUE',\
                                \n{0:>29}MODELISATION='{2}'),\n".format(" ", rname, sname[1]))
                        meca_name.append(name)

                    elif sname[0][0]=='T' and flag[1]==False:
                        f.write("MO_THER = AFFE_MODELE(MAILLAGE=MA,\n{0:>15}AFFE=(\n".format(" "))
                        flag[1]=True
                        f.write("{0:>26}_F(GROUP_MA='{1}',\n{0:>28}PHENOMENE='THERMIQUE',\
                                \n{0:>29}MODELISATION='{1}'),\n".format(" ", rname))
                        ther_name.append(name)
                    elif sname[0][0]=='T':
                        f.write("{0:>26}_F(GROUP_MA='{1}',\n{0:>28}PHENOMENE='THERMIQUE',\
                                \n{:>29}MODELISATION='{2}'),\n".format(" ", rname, sname[1]))
                        ther_name.append(name)

                    elif sname[0][0]=='A' and flag[2]==False:
                        f.write("MO_ACOU = AFFE_MODELE(MAILLAGE=MA,\n{0:>15}AFFE=(\n".format(" "))
                        flag[1]=True
                        f.write("{0:>26}_F(GROUP_MA='{1}',\n {0:>28}PHENOMENE='ACOUSTIQUE',\
                                \n{0:>29}MODELISATION='{2}'),\n".format(" ", rname, sname[1]))
                        acou_name.append(name)

                    elif sname[0][0]=='A':
                        f.write("{0:>26}_F(GROUP_MA='{1}', \n{0:>28}PHENOMENE='ACOUSTIQUE',\
                                \n{0:>29}MODELISATION='{2}'),\n".format(" ", rname, sname[1]))
                        acou_name.append(name)

            if flag[0]==True:
                f.write("{0:>21}),\n{0:>15})\n\n".format(" "))
                self.write_cara_elems(f, 'MO_MECA', meca_name, data_read)
            elif flag[1]==True:
                f.write("{0:>21}),\n{0:>15})\n\n".format(" "))
                self.write_cara_elems(f, 'MO_THER', ther_name, data_read)
            elif flag[2]==True:
                f.write("{0:>21}),\n{0:>15})\n\n".format(" "))
                self.write_cara_elems(f, 'MO_ACOU', acou_name, data_read)

            #Gestion des coques 3D avec un passage de TRIA6/QUAD8 vers TRIA7/QUAD9
            elif coque==True:
                s="'"
                f.write("MA_COQUE=CREA_MAILLAGE(MAILLAGE=MA, \n")

                for name in coque_name:
                    sname=name.split("-")
                    s=s+sname+"', '"
                s=s[:-2]
                f.write("MODI_MAILLE=(_F(GROUP_MA='{0}'\n{1:>17}OPTION='TRIA6_7'),\
                        \n{1:>14}_F(GROUP_MA='{0}\n{1:>17}OPTION='QUAD8_9'),),),\n ".format(s, " "))

                f.write("MO_COQUE=AFFE_MODELE(MAILLAGE=MA_COQUE,\n{0:>20}AFFE=(_F(TOUT='OUI',\
                        \n{0:>28}PHENOMENE='MECANIQUE',\n{0:>29}MODELISATION='COQUE_3D'),),),\n".format(" "))

                self.write_cara_elems(f, 'MO_COQUE', coque_name, data_read)

            f.write("\n")
