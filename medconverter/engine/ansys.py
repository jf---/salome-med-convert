#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path as osp

from operator import itemgetter

from .medconverter import *
from .mesh import *

class MedConverterAnsys(MedConverter):

    @staticmethod
    def convert_ansys_to_med(filename_ansys, filename_med, verbose = False):
        if verbose :
            logger.setLevel(logging.DEBUG)
        c = MedConverterAnsys()
        c.read_ansys_mesh(filename_ansys)
        c.create_med_mesh()
        c.write_med_mesh(filename_med)

    @staticmethod
    def convert_med_to_ansys(filename_med, filename_ansys, verbose = False):
        if verbose :
            logger.setLevel(logging.DEBUG)
        c = MedConverterAnsys()
        c.read_med_mesh(filename_med)
        c.create_ansys_mesh()
        c.write_ansys_mesh(filename_ansys)

    def __init__(self):
        super(MedConverterAnsys, self).__init__()
        self.ansysmesh = None

    def read_ansys_mesh(self, filename):
        logger.debug("Reading ANSYS mesh file : %s"%filename)
        self.mesh = Mesh()
        self.mesh.setInputFormat("ANSYS")
        pass

    def write_ansys_mesh(self, filename):
        raise NotImplementedError()
    
    def create_ansys_mesh(self):
        raise NotImplementedError()
   
