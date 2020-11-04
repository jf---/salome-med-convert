#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict

from .errors import MedConverterError

import medcoupling


class ElementTypeConverter:

    _systus_to_med = {
        '001' : 'POINT1',

        '102' : 'SEG2',
        '203' : 'TRI3',
        '204' : 'QUAD4',
        '304' : 'TETRA4',
        '308' : 'HEXA8',
        '305' : 'PYRA5',
        '306' : 'PENTA6',

        '103' : 'SEG3',
        '206' : 'TRI6',
        '208' : 'QUAD8',
        '310' : 'TETRA10',
        '320' : 'HEXA20',
        '313' : 'PYRA13',
        '315' : 'PENTA15',
    }

    _abaqus_to_med = OrderedDict((
        ('Node', 'POINT1'),

# Mass element - 0D
        ('MASS', 'POINT1'),

# Frame Element
        ('FRAME2D', 'SEG2'),
        ('FRAME3D', 'SEG2'),

# Joint Element
        ('JOINTC', 'SEG2'),

# Spring element
       ('SPRING1', 'POINT1'),
       ('SPRING2', 'SEG2'),
       ('SPRINGA', 'SEG2'),

# Truss Element
        ('T3D2', 'SEG2'),
        ('T3D3', 'SEG3'),
        ('T3D3H', 'SEG3'),

# Elbow Element
        ('ELBOW31', 'SEG2'),
        ('ELBOW32', 'SEG3'),
        ('ELBOW31B', 'SEG2'),
        ('ELBOW31C', 'SEG2'),

# Diffusive heat transfer elements
        ('DC1D2', 'SEG2'),
        ('DC1D3', 'SEG3'),

# Forced convection heat transfer element
        ('DCC1D2' , 'SEG2'),
        ('DCC1D2D', 'SEG2'),

# Coupled thermal-electrical elements
        ('DC1D2E', 'SEG2'),
        ('DC1D3E', 'SEG3'),

# Axis symmetric thermal element
        ('DCCAX4', 'QUAD4'),

# Acoustic element
        ('AC1D2', 'SEG2'),
        ('AC1D3', 'SEG3'),

# Beam element
        ('B21', 'SEG2'),
        ('B22', 'SEG3'),
        ('B23', 'SEG2'),

        ('B21H', 'SEG2'),
        ('B22H', 'SEG3'),
        ('B23H', 'SEG2'),

        ('B31', 'SEG2'),
        ('B32', 'SEG3'),
        ('B33', 'SEG2'),

        ('B31H', 'SEG2'),
        ('B32H', 'SEG3'),
        ('B33H', 'SEG2'),

# PIPE element
        ('PIPE21', 'SEG2'),
        ('PIPE22', 'SEG3'),

        ('PIPE21H', 'SEG2'),
        ('PIPE22H', 'SEG3'),

        ('PIPE31', 'SEG2'),
        ('PIPE32', 'SEG3'),

        ('PIPE31H', 'SEG2'),
        ('PIPE32H', 'SEG3'),

# Membrane Element
        ('M3D3', 'TRI3'),
        ('M3D4', 'QUAD4'),
        ('M3D6', 'TRI6'),
        ('M3D8', 'QUAD8'),
        ('M3D9', 'QUAD9'),

        ('MAX1', 'SEG2'),
        ('MAX2', 'SEG3'),

        ('MGAX1', 'SEG2'),
        ('MGAX2', 'SEG3'),

# Eulerian Element
        ('EC3D8R', 'HEXA8'),

# Reduced Structural Element
        ('S3R', 'TRI3'),
        ('S3RS', 'TRI3'),

        ('S4R', 'QUAD4'),
        ('S4RS', 'QUAD4'),
        ('S4R5', 'QUAD4'),
        ('S4RSW', 'QUAD4'),

        ('S8R', 'QUAD8'),
        ('S8RS', 'QUAD8'),

        ('S9R5', 'QUAD9'),

# Structural Element
        ('S3', 'TRI3'),
        ('S4', 'QUAD4'),

# Reduced Continuum Element
        ('CPE4R', 'QUAD4'),
        ('CPE4RH', 'QUAD4'),
        ('CPE8R', 'QUAD8'),
        ('CPE8RH', 'QUAD8'),

        ('CPS4R', 'QUAD4'),
        ('CPS8R', 'QUAD8'),

        ('C3D8R', 'HEXA8'),
        ('C3D8RH', 'HEXA8'),
        ('C3D20R', 'HEXA20'),
        ('C3D20RH', 'HEXA20'),
        ('C3D27R', 'HEXA27'),
        ('C3D27RH', 'HEXA27'),

# Plane strain element
        ('CPE3', 'TRI3'),
        ('CPE6', 'TRI6'),

        ('CPE4', 'QUAD4'),
        ('CPE8', 'QUAD8'),
        ('CPE9', 'QUAD9'),

        ('CPE3H', 'TRI3'),
        ('CPE6H', 'TRI6'),

        ('CPE4H', 'QUAD4'),
        ('CPE8H', 'QUAD8'),
        ('CPE9H', 'QUAD9'),

        ('CPE6M', 'TRI6'),
        ('CPE6MH', 'TRI6'),

        ('CPE4I', 'QUAD4'),
        ('CPE4IH', 'QUAD4'),

# Plane stress element
        ('CPS3', 'TRI3'),
        ('CPS6', 'TRI6'),
        ('CPS6M', 'TRI6'),

        ('CPS4', 'QUAD4'),
        ('CPS4I', 'QUAD4'),
        ('CPS8', 'QUAD8'),

# Axi element
        ('CAX3', 'TRI3'),
        ('CAX6', 'TRI6'),

        ('CAX4', 'QUAD4'),
        ('CAX8', 'QUAD8'),
        ('CAX9', 'QUAD9'),

        ('CAX3H', 'TRI3'),
        ('CAX6H', 'TRI6'),

        ('CAX4H', 'QUAD4'),
        ('CAX8H', 'QUAD8'),
        ('CAX9H', 'QUAD9'),

        ('CAX6M', 'TRI6'),
        ('CAX6MH', 'TRI6'),

        ('CAX4I', 'QUAD4'),
        ('CAX4IH', 'QUAD4'),
        ('CAX4R', 'QUAD4'),
        ('CAX4RH', 'QUAD4'),
        ('CAX8R', 'QUAD8'),
        ('CAX8RH', 'QUAD8'),

# Continuum Element - Hybrid element
        ('C3D4H', 'TETRA4'),
        ('C3D10H', 'TETRA10'),
        ('C3D10M', 'TETRA10'),
        ('C3D10MH', 'TETRA10'),

        ('C3D5H', 'PYRA5'),
        ('C3D13H', 'PYRA13'),

        ('C3D6H', 'PENTA6'),
        ('C3D15H', 'PENTA15'),
        ('C3D15VH', 'PENTA18'),

        ('C3D8I', 'HEXA8'),
        ('C3D8IH', 'HEXA8'),
        ('C3D8H', 'HEXA8'),
        ('C3D20H', 'HEXA20'),
        ('C3D27H', 'HEXA27'),

# Continuum Element, must be declared last
        ('C3D4', 'TETRA4'),
        ('C3D10', 'TETRA10'),

        ('C3D5', 'PYRA5'),
        ('C3D13', 'PYRA13'),

        ('C3D6', 'PENTA6'),
        ('C3D15', 'PENTA15'),
        ('C3D15V', 'PENTA18'),

        ('C3D8', 'HEXA8'),
        ('C3D20', 'HEXA20'),
        ('C3D27', 'HEXA27'),
    ))

    _aster_to_med = {
        'POI1'   : 'POINT1',

        'SEG2'   : 'SEG2',
        'TRIA3'  : 'TRI3',
        'QUAD4'  : 'QUAD4',
        'TETRA4' : 'TETRA4',
        'HEXA8'  : 'HEXA8',
        'PYRAM5' : 'PYRA5',
        'PENTA6' : 'PENTA6',

        'SEG3'   : 'SEG3',
        'TRIA6'  : 'TRI6',
        'QUAD8'  : 'QUAD8',
        'TETRA10': 'TETRA10',
        'HEXA20' : 'HEXA20',
        'PYRAM13': 'PYRA13',
        'PENTA15': 'PENTA15',

        'SEG4'   : 'SEG4',
        'TRIA7'  : 'TRI7',
        'QUAD9'  : 'QUAD9',
        'PENTA18': 'PENTA18',
        'HEXA27' : 'HEXA27',
    }

    _ansys_to_med = {

    }

    _med_types = 'POINT1 SEG2 TRI3 QUAD4 TETRA4 HEXA8 PYRA5 PENTA6 SEG3 TRI6 QUAD8 TETRA10 HEXA20 PYRA13 PENTA15 SEG4 TRI7 QUAD9 PENTA18 HEXA27'.split()

    def __init__(self, code):
        self.code = code.lower()

        try :
            data = getattr(self, '_{}_to_med'.format(self.code))
        except AttributeError :
            raise MedConverterError("Unknown format '{}'".format(code))

        assert set(data.values()) <= set(self._med_types)
        mdata = {i : getattr(medcoupling, 'NORM_%s'%k) for i, k in data.items()}

        self._external_to_medcoupling = {i : k for i, k in mdata.items()}
        self._medcoupling_to_external = {k : i for i, k in mdata.items()}

        if 'systus' in self.code:
            self._f_e2m = self._systus_to_mc
            self._f_m2e = self._mc_to_systus
        else :
            self._f_e2m = self._to_mc
            self._f_m2e = self._to_ext


    def external_to_medcoupling(self, external_type):
        return self._f_e2m(external_type)

    def medcoupling_to_external(self, medcoupling_type):
        return self._f_m2e(medcoupling_type)

    # Specific functions
    def _systus_to_mc(self, systus_type):
        dim, nb_nodes = systus_type[0], systus_type[-2:]
        return self._to_mc(''.join((dim, nb_nodes)))

    def _mc_to_systus(self, medcoupling_type):
        item = self._to_ext(medcoupling_type)
        return '0'.join((item[0], item[1:]))

    # Generic functions
    def _to_mc(self, external_type):
        try :
            return self._external_to_medcoupling[external_type]
        except KeyError:
            raise MedConverterError("{} type '{}' unknown.".format(*(self.code.title(), external_type)))

    def _to_ext(self, medcoupling_type):
        try :
            return self._medcoupling_to_external[medcoupling_type]
        except KeyError:
            raise MedConverterError("MedCoupling type '{}' unknown.".format(medcoupling_type))
