#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from medcoupling import MEDCouplingUMesh
from .connectivity import ConnectivityRenumberer
from .cells import ElementTypeConverter
from .errors import MedConverterError

class Node:

    """Definition of a node """

    def __init__(self, node_id=None, node_coordinates = None):
        """Initialization of the Node

        Arguments:
            node_id (integer or str): identifier of the node
            node_coordinates (list or tuple): coordinates with 3 values [x,y,z]

        """
        self.id = node_id

        if node_coordinates is not None:
            self.setCoordinates(node_coordinates)
        else:
            self.coordinates = []

    def __repr__(self):
        return "<Node> Id: {0}, Coordinates: {1}".format(self.id, self.coordinates)

    def __str__(self):
        return "<Node> Id: {0}, Coordinates: {1}".format(self.id, self.coordinates)

    def setId(self, node_id):
        """Set identifier of the node

        Arguments:
            node_id (integer or str): identifier of the node

        """
        self.id = node_id

    def getId(self):
        """Get identifier of the node

        Returns:
            node_id (integer or str): identifier of the node

        """
        return self.id

    def setCoordinates(self, node_coordinates):
        """Set coordinates of the node

        Arguments:
            node_coordinates (list or tuple): coordinates with 3 values [x,y,z]

        """
        if(len(node_coordinates) != 3):
            raise RuntimeError("Coordinates have to have 3 items")
        self.coordinates = node_coordinates

    def getCoordinates(self):
        """Get coordinates of the node

        Returns:
            node_coordinates (list or tuple): coordinates with 3 values [x,y,z]

        """
        if(len(self.coordinates) != 3):
            raise RuntimeError("Coordinates have to have 3 items")
        return self.coordinates


class Cell:

    def __init__(self, cell_type=None, cell_id=None, cell_nodes=None, finite_element=None):
        """Initialization of the cell

        Arguments:
            cell_type (str): MED geometric type of cell (POINT1, SEG2, SEG3, ...)
            cell_id (integer or str): identifier of the cell
            cell_nodes (list or tuple): list of the identifier of the nodes of the cell
             (use MED connectivity)
            finite_element (str): finite element attached to the cell

        """
        self.id = cell_id
        self.type = cell_type
        if cell_nodes is not None:
            self.setNodes(cell_nodes)
        else:
            self.nodes = []
        self.finite_element = finite_element

    def __repr__(self):
        return "<Cell> Id: {0}, Type: {1}, Nodes: {2}".format(self.id, self.type, self.nodes)

    def __str__(self):
        return "<Cell> Id: {0}, Type: {1}, Nodes: {2}".format(self.id, self.type, self.nodes)

    def setId(self, cell_id):
        """Set identifier of the cell

        Arguments:
            cell_id (integer or str): identifier of the cell

        """
        self.id =  cell_id

    def getId(self):
        """Get identifier of the cell

        Returns:
            cell_id (integer or str): identifier of the cell

        """
        return self.id

    def setNodes(self, cell_nodes):
        """Get list of the identifier of the nodes of the cell

        Arguments:
            cell_nodes (list or tuple): list of the identifier of the nodes of the cell -
            use MED connectivity
        """
        if self.type is not None:
            nb_nodes = MEDCouplingUMesh.GetNumberOfNodesOfGeometricType(self.type)
            assert len(cell_nodes) == nb_nodes

        self.nodes = cell_nodes

    def getNodes(self):
        """Get list of the identifier of the nodes of the cell

        Returns:
            cell_nodes (list or tuple): list of the identifier of the nodes of the cell -
            use MED connectivity
        """
        return self.nodes

    def setType(self, cell_type):
        """Set MED geometric type of the cell

        Arguments:
            cell_type (str): MED geometric type of cell (POINT1, SEG2, SEG3, ...)

        """
        self.type = cell_type

    def getType(self):
        """Get MED geometric type of the node

        Returns:
            cell_type (str): MED geometric type of cell (POINT1, SEG2, SEG3, ...)

        """
        return self.type

    def setFiniteElement(self, finite_element):
        """Set finite element attached to the cell

        Arguments:
            finite_element (str): finite element attached to the cell

        """
        self.finite_element = finite_element

    def getFiniteElement(self):
        """Get finite element attached to the cell

        Returns:
            finite_element (str): finite element attached to the cell

        """
        return self.finite_element

    def getDimension(self):

        """Get the topological dimension of the cell

        Returns:
            (int): topological dimension of the cell

        """

        return MEDCouplingUMesh.GetDimensionOfGeometricType(self.type)


class Group:

    """Definition of a group of nodes or cells """

    def __init__(self, group_id=None, group_elem=None):
        """Initialization of a group

        Arguments:
            group_id (str): identifier of the group
            group_elem (list or tuple): list of elements of the group

        """
        self.id = group_id
        if group_elem is not None:
            self.group = group_elem
        else:
            self.group = []

    def __repr__(self):
        return "<Group> Id: {0}, Elements: {1}".\
            format(self.id, self.group)

    def __str__(self):
        return "<Group> Id: {0}, Elements: {1}".\
            format(self.id,  self.group)

    def setId(self, group_id):
        """Set identifier of the group

        Arguments:
            group_id (str): identifier of the group

        """
        self.id =  group_id

    def getId(self):
        """Get identifier of the group

        Returns:
            group_id (str): identifier of the group

        """
        return self.id

    def addElements(self, group_elem):
        """Add elements in the group

        Arguments:
            group_elem (list or tuple): list of elements to add the group

        """
        self.group += group_elem

    def setElements(self, group_elem):
        """Set elements in the group (replace in place if existing)

        Arguments:
            group_elem (list or tuple): list of elements of the group

        """
        self.group = group_elem

    def getElements(self):
        """Get elements in the group

        Returns:
            group_elem (list or tuple): list of elements of the group

        """
        return self.group

class Mesh:

    """Definition of the mesh """

    def __init__(self, input_format=None, mesh_name=None, dimension=3, nodes=None, cells=None, \
        groupsOfNodes=None, groupsOfCells=None):
        """Initialization of the mesh

        Arguments:
            input_format (str): format of the original mesh
            mesh_name (str): name of the mesh
            dimension=3 (str): topological dimension of the mesh
            nodes (list or tuple of Node): list of nodes in the mesh
            cells (list or tuple of Cell): list of cells in the cells
            groupsOfNodes (list or tuple of Group): list of groups of nodes in the mesh
            groupsOfCells (list or tuple of Group): list of groups of cells in the mesh
        """
        if input_format is None:
            self.input_format = None
        else:
            self.setInputFormat(input_format)

        self.mesh_name = mesh_name
        self.dimension = dimension

        if nodes is not None:
            self.nodes = nodes
        else:
            self.nodes = []

        if cells is not None:
            self.cells = cells
        else:
            self.cells = []

        if groupsOfNodes is not None:
            self.groupsOfNodes = groupsOfNodes
        else:
            self.groupsOfNodes = []

        if groupsOfCells is not None:
            self.groupsOfCells = groupsOfCells
        else:
            self.groupsOfCells = []

    def setInputFormat(self, input_format):
        """Set original mesh format

        Arguments:
            input_format (str): format of the original mesh
        """

        if input_format in ("MED", "ABAQUS", "SYSTUS"):
            self.input_format = input_format

            if self.input_format is not "MED":
                self.e_conv = ElementTypeConverter(self.input_format)
                self.c_renum = ConnectivityRenumberer(self.input_format)
        else:
            raise MedConverterError("Unknown mesh format: {}".format(input_format))

    def getInputFormat(self):
        """Get original mesh format

        Returns:
            (str): format of the original mesh
        """

        return self.input_format

    def setMeshName(self, mesh_name):
        """Set name of the mesh

        Arguments:
            mesh_name (str): name of the mesh
        """

        self.mesh_name = mesh_name

    def getMeshName(self):
        """Get name of the mesh

        Returns:
            (str): name of the mesh
        """

        return self.mesh_name

    def getNodesCoordinates(self):
        """Get a tuple with the coordinates of the nodes (x0,y0,z0,x1,y1,z1...)

        Returns:
            (tuple): a tuple with the coordinates of the nodes (x0,y0,z0,x1,y1,z1...)
                     3 items for each node
        """

        coor = []
        for node in self.nodes:
            coor_node = node.getCoordinates()
            for xx in coor_node:
                coor.append(xx)

        return tuple(coor)

    def getNumberOfNodes(self):
        """Get the number of nodes in the mesh

        Returns:
            (int): number of nodes in the mesh
        """

        return len(self.nodes)

    def getNumberOfCells(self):
        """Get the number of cells in the mesh

        Returns:
            (int): number of cells in the mesh
        """

        return len(self.cells)

    def getNumberOfGroupsOfNodes(self):
        """Get the number of groups of nodes in the mesh

        Returns:
            (int): number of groups of nodes in the mesh
        """

        return len(self.groupsOfNodes)

    def getNumberOfGroupsOfCells(self):
        """Get the number of groups of cells in the mesh

        Returns:
            (int): number of groups of cells in the mesh
        """

        return len(self.groupsOfCells)

    def setDimension(self, dimension):
        """Set toplogical dimension of the mesh

        Arguments:
            (int): topological dimension of the mesh
        """

        self.dimension = dimension

    def getDimension(self):
        """Get toplogical dimension of the mesh

        Returns:
            (int): topological dimension of the mesh
        """

        return self.dimension

    def addNode(self, node_id, node_coordinates):
        """Add a group of nodes

        Arguments:
            node_id (integer or str): identifier of the node
            node_coordinates (list or tuple): coordinates with 3 values [x,y,z]
        """

        self.nodes.append(Node(node_id, node_coordinates))

    def addCell(self, cell_type, cell_id, cell_nodes, finite_element=None):
        """Add a cell (MED-geometric type and MED-connectivity will be created automaticaly \
            if the input_format is not MED)

        Arguments:
            cell_type (str): geometric type of cell
            cell_id (integer or str): identifier of the cell
            cell_nodes (list or tuple): list of the identifier of the nodes of the cell
            finite_element (str): finite element attached to the cell
        """

        if self.input_format is "MED":
            self.cells.append(Cell(cell_type, cell_id, cell_nodes, finite_element))
        else:
            medcoupling_type = self.e_conv.external_to_medcoupling(cell_type)
            elements_nodes = map(int, cell_nodes)

            nbnodes = MEDCouplingUMesh.GetNumberOfNodesOfGeometricType(medcoupling_type)

            element_nodes_asc = tuple(k for k in elements_nodes)
            assert nbnodes == len(element_nodes_asc)
            medcoupling_nodes = self.c_renum.external_to_medcoupling(medcoupling_type, element_nodes_asc)

            self.cells.append(Cell(medcoupling_type, cell_id, medcoupling_nodes, finite_element))


    def addGroupOfNodes(self, name, nodes):
        """Add a group of nodes

        Arguments:
            name (str or int): name of the group
            nodes (list or tuple): list of identifiers of the nodes
        """

        self.groupsOfNodes.append(Group(name, nodes))

    def addGroupOfCells(self, name, cells):
        """Add a group of cells

        Arguments:
            name (str or int): name of the group
            cells (list or tuple): list of identifiers of the cells
        """

        self.groupsOfCells.append(Group(name, cells))

    def renumbering(self):
        """Renumbering the nodes and cells of the mesh from 0 with continuous numbering"""

        # check nodes
        self.corresponding_nodes = {}
        for idx, node in enumerate(self.nodes):
            if int(node.getId()) in self.corresponding_nodes :
                raise KeyError("Two nodes with identical id: {0}".format(node.getId()))
            else:
                self.corresponding_nodes[int(node.getId())] = idx
                node.setId(idx)

        # check groups of nodes
        self.corresponding_group_nodes = {}
        for group_n in self.groupsOfNodes:
            if str(group_n.getId()) in self.corresponding_group_nodes:
                raise KeyError("Two groups of nodes with identical id: {0}".format(group_n.getId()))
            else:
                self.corresponding_group_nodes[str(group_n.getId())] = group_n.getId()

            l_nodes = []
            for node_id in group_n.getElements():
                l_nodes.append(self.corresponding_nodes[int(node_id)])

            group_n.setElements(l_nodes)


        # check cells
        self.corresponding_cells = {}
        for idx, cell in enumerate(self.cells):
            if int(cell.getId()) in self.corresponding_cells :
                raise KeyError("Two cells with identical id: {0}".format(cell.getId()))
            else:
                self.corresponding_cells[int(cell.getId())] = idx
                cell.setId(idx)

        # check groups of cells
        self.corresponding_group_cells = {}
        for group_c in self.groupsOfCells:
            if str(group_c.getId()) in self.corresponding_group_cells:
                raise KeyError("Two groups of cells with identical id: {0}".format(group_c.getId()))
            else:
                self.corresponding_group_cells[str(group_c.getId())] = group_c.getId()

            l_cells = []
            for cell_id in group_c.getElements():
                l_cells.append(self.corresponding_cells[int(cell_id)])

            group_c.setElements(l_cells)

    def _sortCellIdsByDimension(self, cells_id):
        """Sort cell identifiers sorted by dimension

        Returns:
            (dict): cells identifiers sorted by dimension (the keys are the dimension)
        """

        cellsbydim = {}
        for cell_id in cells_id:
            dim = self.cells[cell_id].getDimension()
            if not dim in cellsbydim : cellsbydim[dim] = []
            cellsbydim[dim].append(cell_id)

        return cellsbydim

    def _sortCellIdsByType(self, cells_id):
        """Sort cell identifiers sorted  by type

        Returns:
            (dict(dict)): cells identifiers sorted geometric type (key)
        """

        cellsbytyp = {}
        for cell_id in cells_id:
            typ = self.cells[cell_id].getType()
            if not typ in cellsbytyp[typ] : cellsbytyp = []
            cellsbytyp[typ].append(cell_id)

        return cellsbytyp

    def _sortCellIdsByDimensionAndType(self, cells_id):
        """Sort cell identifiers sorted by dimension then by type

        Returns:
            (dict(dict)): cells identifiers sorted by dimension (first key)
                            and type (second key)
        """

        cells_sorted = {}
        cellsbydim = self._sortCellIdsByDimension(cells_id)
        for dim, cells_dim in cellsbydim.items():
            cells_sorted[dim] = self._sortCellIdsByType(cells_dim)

        return cells_sorted

    def getCellIdsByDimension(self):
        """Get cell identifiers sorted by dimension

        Returns:
            (dict): cells identifiers sorted by dimension (the keys are the dimension)
        """

        return self._sortCellIdsByDimension(tuple(cell.getId() for cell in self.cells))

    def getCellIdsByType(self):
        """Get cell identifiers sorted by geometric type

        Returns:
            (dict): cells identifiers sorted by geometric type (key)
        """

        return self._sortCellIdsByType(tuple(cell.getId() for cell in self.cells))

    def getCellIdsByDimensionAndType(self):
        """Get cell identifiers sorted by dimension then by type

        Returns:
            (dict): cells identifiers sorted by dimension (first key) and type (second key)
        """

        return self._sortCellIdsByDimensionAndType(tuple(cell.getId() for cell in self.cells))

    def getGroupsOfCellIdsByDimension(self):
        """Get groups of cells sorted by dimension

        Returns:
            (dict): groups of cells sorted by dimension (the keys are the dimension)
        """

        groupsbydim = {}
        for group in self.groupsOfCells:
            group_id = group.getId()
            cellsbydim = self._sortCellIdsByDimension(group.getElements())

            for dim, cells in cellsbydim.items():
                if not dim in groupsbydim : groupsbydim[dim] = []
                groupsbydim[dim].append(Group(group_id, cells))

        return groupsbydim
