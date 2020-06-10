.. MedConverter documentation master file, created by
   sphinx-quickstart on Wed Jun 10 10:57:26 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MedConverter's documentation!
========================================

Introduction
------------

MedConverter is a tool for converting meshes from external formats to the Salome format.
It actually supports Abaqus and Systus formats.

Main function
-------------
.. autofunction:: medconverter.convert

Mesh formats
------------
.. autoclass:: medconverter.Fmt
		  
Tests
-----

.. toctree::
   :maxdepth: 1
	      
   tests

Connectivity tables
-------------------

- `Salome <_static/salome_connectivity.pdf>`_
- `Aster <_static/aster_connectivity.pdf>`_
- `Systus <_static/systus_connectivity.pdf>`_
- `Abaqus <_static/abaqus_connectivity.pdf>`_

 
