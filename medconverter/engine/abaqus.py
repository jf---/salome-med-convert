#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .medconverter import *

class AbaqusNode:


    def __init__(self, node_id=-1, node_coordinates = []):
        self.id = node_id
        self.coordinates = node_coordinates

    def __repr__(self):
        return "<Node> Id: {0}, Coordinates: {1}".format(self.id, self.coordinates)

    def __str__(self):
        return "<Node> Id: {0}, Coordinates: {1}".format(self.id, self.coordinates)

    def setId(self, node_id):
        self.id = node_id

    def getId(self):
        return self.id

    def setCoordinates(self, node_coordinates):
        self.coordinates = node_coordinates

    def getCoordinates(self):
        return self.coordinates

class AbaqusElement:

    def __init__(self, elem_type="", elem_id=-1, elem_nodes=[]):
        self.id = elem_id
        self.nodes = elem_nodes
        self.type = elem_type

    def __repr__(self):
        return "<Element> Id: {0}, Type: {1}, Nodes: {2}".format(self.id, self.type, self.nodes)

    def __str__(self):
        return "<Element> Id: {0}, Type: {1}, Nodes: {2}".format(self.id, self.type, self.nodes)

    def setId(self, elem_id):
        self.id =  elem_id

    def getId(self):
        return self.id

    def setNodes(self, elem_nodes):
        self.nodes = elem_nodes

    def getNodes(self):
        return self.nodes

    def setType(self, elem_type):
        self.type = elem_type

    def getType(self):
        return self.type


class AbaqusGroup:

    def __init__(self, name="", instance="", group=[]):
        self.name = name
        self.instance = instance
        self.group = group

    def __repr__(self):
        return "<Group> Name: {0}, Instance: {1}, Group: {2}".format(self.name, self.instance, self.group)

    def __str__(self):
        return "<Group> Name: {0}, Instance: {1}, Group: {2}".format(self.name, self.instance, self.group)

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setInstance(self, instance):
        self.instance = instance

    def getInstance(self):
        return self.instance

    def setGroup(self, group):
        self.group = group

    def getGroup(self):
        return self.group





class MedConverterAbaqus(MedConverter):

    @staticmethod
    def convert_abaqus_to_med(filename_abaqus, filename_med, verbose = False):
        if verbose : logger.setLevel(logging.DEBUG)
        c = MedConverterAbaqus()
        c.read_abaqus_mesh(filename_abaqus)
        c.create_med_mesh()
        c.write_med_mesh(filename_med)

    @staticmethod
    def convert_med_to_abaqus(filename_med, filename_abaqus, verbose = False):
        if verbose : logger.setLevel(logging.DEBUG)
        c = MedConverterAbaqus()
        c.read_med_mesh(filename_med)
        c.create_abaqus_mesh()
        c.write_abaqus_mesh(filename_abaqus)

    def __init__(self):
        super(MedConverterAbaqus, self).__init__()
        self.abaqusmesh = None

    def read_abaqus_mesh(self, filename):
        logger.debug("Reading Abaqus mesh file : %s"%filename)

        Node, Elements, Nset, Elset = [], [], [], []

        # Lecture du fichier .inp où les blocs sont separés par des *Instance et *End Instance
        with open(filename, 'r', encoding = self._get_file_encoding(filename)) as f :
            next(f)

            # Lecture du nom du maillage si disponible
            line_1 = next(f).strip()
            # self.mesh_name = line_1 if line_1 else 'Mesh'
            self.mesh_name = line_1 if line_1 else osp.splitext(osp.split(filename)[-1])[0]

            # a priori, this is a 3D mesh
            self.space_dim = 3

            for line in f :
                if(line.startswith("*Instance")):
                    self._read_name_mesh(line)

                self._read_data(f, line, Node, Elements, Nset, Elset)


        f.close()

        logger.debug("Mesh name : %s"%self.mesh_name)
        logger.debug("Space Dimension : %d"%self.space_dim)
        logger.debug("Number of nodes : %d"%(len(Node)))
        logger.debug("Number of elements : %d"%(len(Elements)))
        logger.debug("Number of groups : %d"%(len(Nset) + len(Elset)))

        # nodes of the mesh (collection of double)
        corresponding_nodes = {}
        coor = []
        for idx, node in enumerate(Node):
            if(self.checkKey(corresponding_nodes, int(node.getId()))):
                raise KeyError("Two nodes with identical id: {0}".format(node.getId()))
            else:
                corresponding_nodes[int(node.getId())] = idx

            coor_node = node.getCoordinates()
            for xx in coor_node:
                coor.append(xx)

        self.nodes = tuple(coor)

        # Les elements, triés par dimension
        corresponding_elements = {}
        max_dim_elements = '0D'
        e_conv = ElementTypeConverter('ABAQUS')
        c_renum = ConnectivityRenumberer('ABAQUS')

        for elem in Elements :
            idx_element_abaqus = elem.getId()
            element_abaqus_type = elem.getType()
            elements_nodes_abaqus = map(int, elem.getNodes())

            element_medcoupling_type = e_conv.external_to_medcoupling(element_abaqus_type)
            element_dim = MEDCouplingUMesh.GetDimensionOfGeometricType(element_medcoupling_type)
            nbnodes = MEDCouplingUMesh.GetNumberOfNodesOfGeometricType(element_medcoupling_type)

            assert nbnodes == len(elem.getNodes())
            element_nodes_asc = tuple(corresponding_nodes[k] for k in elements_nodes_abaqus)
            element_nodes_med = c_renum.external_to_medcoupling(element_medcoupling_type, element_nodes_asc)

            key = '%dD'%element_dim
            if not key in self.elements : self.elements[key] = []
            if not key in corresponding_elements : corresponding_elements[key] = {}
            self.elements[key].append((element_medcoupling_type, element_nodes_med))
            corresponding_elements[key][idx_element_abaqus] = len(corresponding_elements[key])
            max_dim_elements = max(max_dim_elements, key)

        # Les groups, triés par dimension
        # Nodes' group
        for group in Nset :
            group_name = group.getName()
            group_nodes_abaqus = map(int, group.getGroup())
            self.groups_n[group_name] = tuple(corresponding_nodes[k] for k in group_nodes_abaqus)

        # Element's group
        for group in Elset :
            group_name = group.getName()
            group_element_abaqus = map(str, group.getGroup())

            for element_abaqus in group_element_abaqus :
                for key in self.elements.keys():
                    if element_abaqus in corresponding_elements[key]:
                        if not key in self.groups_e : self.groups_e[key] = {}
                        if not group_name in self.groups_e[key]:  self.groups_e[key][group_name] = []
                        self.groups_e[key][group_name].append(corresponding_elements[key][element_abaqus])


    def _read_data(self, f, line, Node, Elements, Nset, Elset):
        keyword = line.strip().strip("*").strip()

        if(keyword == "Node"):
            line0 = self._read_nodes(f, Node)
            # print("Nodes")
            # print(Node)
            self._read_data(f, line0, Node, Elements, Nset, Elset)
        elif(keyword.startswith("Element")):
            line0 = self._read_cells(f, keyword, Elements)
            # print("Cells")
            # print(Elements)
            self._read_data(f, line0, Node, Elements, Nset, Elset)
        elif(keyword.startswith("Nset")):
            line0 = self._read_group(f, keyword, "NSET", Nset)
            # print("Nset")
            # print(Nset)
            self._read_data(f, line0, Node, Elements, Nset, Elset)
        elif keyword.startswith(('Elset', 'ELSET')):
            line0 = self._read_group(f, keyword, "ELSET", Elset)
            # print("Elset")
            # print(Elset)
            self._read_data(f, line0, Node, Elements, Nset, Elset)

    def _read_name_mesh(self, line0):
        # find type of element
        sline = line0.split(",")[1:]
        etype_sline = sline[0].upper()
        assert "NAME" in etype_sline, etype_sline
        self.mesh_name = sline[0].split("=")[1].strip()

    def _read_nodes(self, f, Node):
        while True:
            line = f.readline()
            if line.startswith("*"):
                break
            entries = line.strip().rstrip(",").split(",")
            nid, x = entries[0], entries[1:]
            Node.append(AbaqusNode(nid, [float(xx) for xx in x]))

        return line

    def _read_cells(self, f, line0, Elements):
        # find type of element
        sline = line0.split(",")[1:]
        etype_sline = sline[0].upper()
        assert "TYPE" in etype_sline, etype_sline
        etype = etype_sline.split("=")[1].strip()

        while True:
            line = f.readline()
            if line.startswith("*"):
                break
            entries = line.strip().rstrip(",").split(",")
            eid, nodes = entries[0], entries[1:]
            Elements.append(AbaqusElement(etype, eid, [int(n) for n in nodes]))

        return line

    def _read_group(self, f, line0, param, Group):
        # find type of element
        params_map = self._get_param_map(line0)
        name = params_map[param]
        list_nodes = []

        if("generate" in params_map.keys()):
            generate = True
        else:
            generate = False

        while True:
            line = f.readline()
            if line.startswith("*"):
                break
            if(generate):
                gener = line.strip().rstrip(",").split(",")
                list_nodes += [int(n) for n in range(int(gener[0]), int(gener[1])+1, int(gener[2]))]
            else:
                list_nodes += line.strip().rstrip(",").split(",")

        Group.append(AbaqusGroup(name, 'internal', [int(n) for n in list_nodes]))

        return line

    def _get_param_map(self, word, required_keys=None):
        """
        get the optional arguments on a line
        Example
        -------
        >>> word = 'elset,instance=dummy2,generate'
        >>> params = get_param_map(word, required_keys=['instance'])
        params = {
            'elset' : None,
            'instance' : 'dummy2,
            'generate' : None,
        }
        """
        if required_keys is None:
            required_keys = []
        words = word.split(",")
        param_map = {}
        for wordi in words:
            if "=" not in wordi:
                key = wordi.strip()
                value = None
            else:
                sword = wordi.split("=")
                assert len(sword) == 2, sword
                key = sword[0].strip().upper()
                value = sword[1].strip()
            param_map[key] = value

        msg = ""
        for key in required_keys:
            if key not in param_map:
                msg += "%r not found in %r\n" % (key, word)
        if msg:
            raise RuntimeError(msg)
        return param_map

    def checkKey(self, dico, key):
        if(key in dico):
            return True
        else:
            return False

    def create_abaqus_mesh(self):
        raise Exception("Not yet implemented")

    def write_abaqus_mesh(self, filename_abaqus):
        raise Exception("Not yet implemented")
