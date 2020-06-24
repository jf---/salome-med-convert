#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .medconverter import *
import os.path as osp


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
        if(len(self.coordinates) != 3):
            raise RuntimeError("Coordinates have to have 3 elements")
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
        self.nbParts = 0
        self.nbAssembly = 0

    def read_abaqus_mesh(self, filename):
        logger.debug("Reading Abaqus mesh file : %s"%filename)

        Nodes, Elements, Nset, Elset = [], [], [], []

        # Lecture du fichier .inp où les blocs sont separés par des *Instance et *End Instance
        with open(filename, 'r', encoding = self._get_file_encoding(filename)) as file :
            next(file)
            self.filename = filename

            # Lecture du nom du maillage si disponible
            line_1 = next(file).strip()
            # self.mesh_name = line_1 if line_1 else 'Mesh'
            self.mesh_name = line_1 if line_1 else osp.splitext(osp.split(filename)[-1])[0]

            # a priori, this is a 3D mesh
            self.space_dim = 3

            for line in file :
                if(line.startswith("*Instance")):
                    self._read_name_mesh(line)

                self._read_data(file, line, Nodes, Elements, Nset, Elset)


        file.close()

        logger.debug("Mesh name : %s"%self.mesh_name)
        logger.debug("Space Dimension : %d"%self.space_dim)
        logger.debug("Number of nodes : %d"%(len(Nodes)))
        logger.debug("Number of elements : %d"%(len(Elements)))
        logger.debug("Number of groups : %d"%(len(Nset) + len(Elset)))

        # nodes of the mesh (collection of double)
        corresponding_nodes = {}
        coor = []
        for idx, node in enumerate(Nodes):
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
            # print(element_dim, element_abaqus_type, element_medcoupling_type, nbnodes)
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


    def _read_data(self, file, line, Nodes, Elements, Nset, Elset):
        keyword = line.strip().strip("*").strip()

        if(keyword.startswith( ("Node", "NODE", "node"))):
            line0 = self._read_nodes(file, keyword, Nodes, Nset)
            # print("Nodes")
            # print(Nodes)
            self._read_data(file, line0, Nodes, Elements, Nset, Elset)
        elif(keyword.startswith(("Element", "ELEMENT", "element"))):
            line0 = self._read_cells(file, keyword, Elements, Elset)
            # print("Cells")
            # print(Elements)
            self._read_data(file, line0, Nodes, Elements, Nset, Elset)
        elif(keyword.startswith(("Nset", "NSET", "nset"))):
            line0 = self._read_group(file, keyword, "NSET", Nset)
            # print("Nset")
            # print(Nset)
            self._read_data(file, line0, Nodes, Elements, Nset, Elset)
        elif keyword.startswith(('Elset', 'ELSET', "elset")):
            line0 = self._read_group(file, keyword, "ELSET", Elset)
            # print("Elset")
            # print(Elset)
            self._read_data(file, line0, Nodes, Elements, Nset, Elset)
        elif keyword.startswith(('Include', 'INCLUDE')):
            line0 = self._read_include_file(file, keyword, Nodes, Elements, Nset, Elset)
        elif keyword.startswith(('Part,', 'PART,')):
            self.nbParts += 1

            if(self.nbParts > 1):
                raise RuntimeError("Only one part allowed")
        elif keyword.startswith(('Assembly,', 'ASSEMBLY,')):
            self.nbAssembly += 1

            if(self.nbAssembly > 1):
                raise RuntimeError("Only one Assembly allowed")
        elif keyword.startswith(('Ngen', 'NGEN','NGen','ngen')):
            raise RuntimeError("Keyword not supported: NGEN")
        elif keyword.startswith(('Nfill', 'NFILL','NFill', 'nfill')):
            raise RuntimeError("Keyword not supported: NFILL")
        elif keyword.startswith(('Nmap', 'NMAP','NMap','nmap')):
            raise RuntimeError("Keyword not supported: NMAP")
        elif keyword.startswith(('Ncopy', 'NCOPY','Ncopy','ncopy')):
            raise RuntimeError("Keyword not supported: NMAP")

    def _read_name_mesh(self, line0):
        # find type of element
        sline = line0.split(",")[1:]
        etype_sline = sline[0].upper()
        assert "NAME" in etype_sline, etype_sline
        self.mesh_name = sline[0].split("=")[1].strip()

    def _read_nodes(self, file, line0, Nodes, Nset):
        # get informations about nodes
        params_map = self._get_param_map(line0, )

        # this is not a list of node
        if("NODE" not in params_map):
            return file.readline()

        # create directly a group from the list of nodes
        if "NSET" in params_map:
            create_nset = True
            list_nodes = []
        else:
            create_nset = False

        # the coordinates are in an external file
        if "INPUT" in params_map:
            l_extern_file = True
            filename_node = osp.dirname(self.filename) + "/"+ params_map["INPUT"]
            file_to_read = open(filename_node, 'r')
        else:
            l_extern_file = False
            file_to_read = file

        # loop on nodes
        while True:
            line = file_to_read.readline()
            if self.breakLoop(line):
                break
            entries = line.strip().rstrip(",").split(",")
            # read id and coordinatines
            nid, x = entries[0], entries[1:]

            # fill with zero if not enougth coordinates
            if (len(x) < 3):
                for i in range(0, 3-len(x)):
                    x.append("0.0")
            assert len(x) == 3

            Nodes.append(AbaqusNode(nid, [float(xx) for xx in x]))

            # add node in the group
            if create_nset:
                list_nodes.append(nid)

        # add group in Nset
        if create_nset:
            name = params_map["NSET"]
            Nset.append(AbaqusGroup(name, 'internal', [int(n) for n in list_nodes]))

        if(l_extern_file):
            file_to_read.close()
            line = file.readline()

        return line

    # read a string which are in more that one line. If terminates by separator
    def _read_continuous_line(self, file, line, separator):

        # read the line
        entries= line.strip().rstrip(",").split(",")

        # more than one line to read
        if line.rstrip().endswith(separator):
            line = file.readline()
            entries += self._read_continuous_line(file, line, separator)

        return entries


    # Read a list of element
    def _read_cells(self, file, line0, Elements, Elset):
        # get informations about elements
        params_map = self._get_param_map(line0)

        # this is not a list of element
        if("ELEMENT" not in params_map):
            return file.readline()

        # create directly a group from the list of elements
        if "ELSET" in params_map:
            create_elset = True
            list_elem = []
        else:
            create_elset = False

        # the elements are in an external file
        if "INPUT" in params_map:
            l_extern_file = True
            filename_elem = osp.dirname(self.filename) + "/"+ params_map["INPUT"]
            file_to_read = open(filename_elem, 'r')
        else:
            l_extern_file = False
            file_to_read = file

        # get type of element to create
        etype = params_map["TYPE"]

        # loop on list of elements
        while True:
            line = file_to_read.readline()
            if self.breakLoop(line):
                break
            entries = self._read_continuous_line(file_to_read, line, ",")
            # get id and list of nodes
            eid, nodes = entries[0], entries[1:]
            # add element
            Elements.append(AbaqusElement(etype, eid, [int(n) for n in nodes]))
            # add element in the group
            if create_elset:
                list_elem.append(eid)

        # add group in Elset
        if create_elset:
            name = params_map["ELSET"]
            Elset.append(AbaqusGroup(name, 'internal', [int(n) for n in list_elem]))

        if(l_extern_file):
            file_to_read.close()
            line = file.readline()

        return line

    def _read_group(self, file, line0, param, Group):
        # find type of element
        params_map = self._get_param_map(line0)

        # this is not a group
        if param not in params_map:
            return file.readline()

        list_item = []

        # to generate groups
        if("GENERATE" in params_map.keys()):
            generate = True
        else:
            generate = False

        while True:
            line = file.readline()
            if self.breakLoop(line):
                break
            entries = line.strip().rstrip(",").split(",")

            if(len(entries) == 1):
                list_item = [entries[0]]
                for grp in Group:
                    if(grp.getName() == entries[0]):
                        # this is a copy of group
                        list_item = grp.getGroup()
                        break
            else:
                if(generate):
                    # default value is 1
                    if(len(entries) == 2):
                        entries.append("1")
                    # generate elements in group
                    # first element, last_element, step
                    list_item += [int(n) for n in range(int(entries[0]), int(entries[1])+1, int(entries[2]))]
                else:
                    # read directely list of elements
                    list_item += entries

        # add group
        name = params_map[param]
        Group.append(AbaqusGroup(name, 'internal', [int(n) for n in list_item]))

        return line

    # Read an included file
    def _read_include_file(self, file, line0, Nodes, Elements, Nset, Elset):
        # get informations about elements
        params_map = self._get_param_map(line0)

        # this is not an included file
        if("INPUT" not in params_map):
            return file.readline()
        else:
            # Not allowed
            raise RuntimeError("Keyword not supported: INCLUDE")

        return file.readline()

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
                key = wordi.strip().upper()
                value = None
            else:
                sword = wordi.split("=")
                assert len(sword) == 2, sword
                key = (sword[0].strip()).upper()
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

    def breakLoop(self, line):
        if line.startswith("*"):
            return True
        elif line == "":
            return True
        elif line in ['\n', '\r\n']:
            return True

        return False

    def create_abaqus_mesh(self):
        raise Exception("Not yet implemented")

    def write_abaqus_mesh(self, filename_abaqus):
        raise Exception("Not yet implemented")
