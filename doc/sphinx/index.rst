
Welcome to MedConverter's documentation!
========================================

Introduction
------------
MedConverter is a tool for converting meshes from external formats to the Salome format.
The current supported formats are Abaqus and Systus.

GUI usage
---------
Follow the wizard.

Main function
-------------
.. autofunction:: medconverter.convert

Mesh formats
------------
.. autoclass:: medconverter.Fmt
		  
Tests
-----
.. toctree::
   :maxdepth: 2
	      
   tests_systus
   tests_abaqus
   tests_ansys

Connectivity tables
-------------------

- `Salome <_static/salome_connectivity.pdf>`_
- `Aster <_static/aster_connectivity.pdf>`_
- `Systus <_static/systus_connectivity.pdf>`_
- `Abaqus <_static/abaqus_connectivity.pdf>`_
- `Ansys <_static/ansys_connectivity.pdf>`_

 
