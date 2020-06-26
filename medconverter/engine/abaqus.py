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


class AbaqusPart:

    def __init__(self):
        self.name = " "
        self.Nodes = []
        self.Elements = []
        self.Elset = []
        self.Nset = []

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name


class AbaqusInstance:

    def __init__(self):
        self.name = " "
        self.Part = []
        self.Nodes = []
        self.Elements = []
        self.Elset = []
        self.Nset = []
        self.translation = [0.0, 0.0, 0.0]

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setPart(self, part_name):
        self.Part = part_name

    def getPart(self):
        return self.Part

class AbaqusAssembly:

    def __init__(self):
        self.name = " "
        self.Instance = []
        self.Nodes = []
        self.Elements = []
        self.Elset = []
        self.Nset = []

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def addInstance(self, Instance):
        self.Instance.append(Instance)

    def getInstance(self):
        return self.Instance


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

        Assembly = AbaqusAssembly()
        Nodes, Elements, Nset, Elset, Parts= [], [], [], [], []

        # Lecture du fichier .inp où les blocs sont separés par des *Instance et *End Instance
        with open(filename, 'r', encoding = self._get_file_encoding(filename)) as file :
            self.filename = filename
            self.mesh_name = self._read_meshname(filename)

            # a priori, this is a 3D mesh
            self.space_dim = 3

            for line in file :
                self.line = line
                print("READ:", self.line)
                self._read_data(file, Nodes, Elements, Nset, Elset, Parts, Assembly)


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

    def _read_meshname(self, filename):
        return osp.splitext(osp.basename(filename))[0]

    def _read_data(self, file, Nodes, Elements, Nset, Elset, Parts, Assembly):
        self.line = self.line.replace("*", '').strip()

        print("KEYWORD: ", self.line)

        if(self.line.upper().startswith("NODE")):
            self._read_nodes(file, Nodes, Nset)
            # print("Nodes")
            # print(Nodes)
            self._read_data(file, Nodes, Elements, Nset, Elset, Parts, Assembly)
        elif(self.line.upper().startswith("ELEMENT")):
            self._read_cells(file, Elements, Elset)
            # print("Cells")
            # print(Elements)
            self._read_data(file, Nodes, Elements, Nset, Elset, Parts, Assembly)
        elif(self.line.upper().startswith("NSET")):
            self._read_group(file, "NSET", Nset)
            # print("Nset")
            # print(Nset)
            self._read_data(file, Nodes, Elements, Nset, Elset, Parts, Assembly)
        elif self.line.upper().startswith('ELSET'):
            self._read_group(file, "ELSET", Elset)
            # print("Elset")
            # print(Elset)
            self._read_data(file, Nodes, Elements, Nset, Elset, Parts, Assembly)
        elif self.line.upper().startswith('INCLUDE'):
            self._read_include_file(file, Nodes, Elements, Nset, Elset)
        elif self.line.upper().startswith('INSTANCE,'):
            self._read_instance(file,  Assembly)

            if(len(Parts) > 1):
                raise RuntimeError("Only one part allowed")
        elif self.line.upper().startswith('PART,'):
            self._read_part(file, Parts)

            if(len(Parts) > 1):
                raise RuntimeError("Only one part allowed")
        elif self.line.upper().startswith('ASSEMBLY,'):
            self._read_assembly(file, Assembly)
            self.nbAssembly += 1

            if(self.nbAssembly > 1):
                raise RuntimeError("Only one Assembly allowed")
        elif self.line.upper().startswith('NGEN'):
            raise RuntimeError("Keyword not supported: NGEN")
        elif self.line.upper().startswith('NFILL',):
            raise RuntimeError("Keyword not supported: NFILL")
        elif self.line.upper().startswith('NMAP'):
            raise RuntimeError("Keyword not supported: NMAP")
        elif self.line.upper().startswith('NCOPY'):
            raise RuntimeError("Keyword not supported: NMAP")

    def _read_nodes(self, file, Nodes, Nset):
        # get informations about nodes
        params_map = self._get_param_map(self.line)

        # this is not a list of node
        if("NODE" not in params_map):
            self.line = file.readline()
            return

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
            self.line = file_to_read.readline()
            print("NODE: ",self.line)
            l_process_line = True
            if(l_extern_file):
                if self.line.startswith("*"):
                    self.line = self.line.replace("*", '').strip()
                    if(self.line.upper().startswith("NODE")):
                        self._read_nodes(file_to_read, Nodes, Nset)
                    else:
                        l_process_line = False

                if self.line == "":
                    break
                elif self.line in ['\n', '\r\n']:
                    break
            elif self.breakLoop(self.line):
                break

            if l_process_line:
                entries = self._read_continuous_line(file_to_read, ',')
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

                if self.line.lstrip().startswith("*"):
                    break

        # add group in Nset
        if create_nset:
            name = params_map["NSET"]
            Nset.append(AbaqusGroup(name, 'internal', [int(n) for n in list_nodes]))

        if(l_extern_file):
            file_to_read.close()
            self.line = file.readline()


    # Read a list of element
    def _read_cells(self, file, Elements, Elset):
        # get informations about elements
        params_map = self._get_param_map(self.line)

        # this is not a list of element
        if("ELEMENT" not in params_map):
            self.line = file.readline()
            return

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
        print(params_map)

        # loop on list of elements
        while True:
            self.line = file_to_read.readline()
            print("ELE: ",self.line)

            l_process_line = True
            if(l_extern_file):
                if self.line.startswith("*"):
                    self.line = self.line.replace("*", '').strip()
                    if(self.line.upper().startswith("ELEMENT")):
                        self._read_cells(file_to_read, Elements, Elset)
                    else:
                        l_process_line = False

                if self.line == "":
                    break
                elif self.line in ['\n', '\r\n']:
                    break
            elif self.breakLoop(self.line):
                break

            if l_process_line:
                entries= self._read_continuous_line(file_to_read, ",")
                print(entries)
                # get id and list of nodes
                eid, nodes = entries[0], entries[1:]
                # add element
                Elements.append(AbaqusElement(etype, eid, [int(n) for n in nodes]))
                # add element in the group
                if create_elset:
                    list_elem.append(eid)

                if self.line.lstrip().startswith("*"):
                    break

        # add group in Elset
        if create_elset:
            name = params_map["ELSET"]
            Elset.append(AbaqusGroup(name, 'internal', [int(n) for n in list_elem]))

        if(l_extern_file):
            file_to_read.close()
            self.line = file.readline()


    def _read_group(self, file, param, Group):
        # find type of element
        params_map = self._get_param_map(self.line)

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
            self.line = file.readline()
            print("GRP: ",self.line)

            if self.breakLoop(self.line):
                break

            entries = [x.strip() for x in self.line.strip().rstrip(",").split(",")]

            try:
                int(entries[0])
                l_list_grp = False
            except:
                l_list_grp = True
            if(l_list_grp):
                for grp_name in entries:
                    for grp in Group:
                        if(grp.getName() == grp_name):
                            # this is a copy of group
                            list_item += grp.getGroup()
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


    # Read an included file
    def _read_include_file(self, file, Nodes, Elements, Nset, Elset):
        # get informations about file
        params_map = self._get_param_map(self.line)

        # this is not an included file
        if("INPUT" not in params_map):
            return file.readline()

        # open external file
        filename_elem = osp.dirname(self.filename) + "/"+ params_map["INPUT"]
        file_to_read = open(filename_elem, 'r')

        # read external file
        for self.line in file_to_read :
            self._read_data(file_to_read, Nodes, Elements, Nset, Elset, Parts, Assembly)

        file_to_read.close()

    def _read_part(self, file, Parts):
         # get informations about part
        params_map = self._get_param_map(self.line)

        print(params_map)
        # this is not an included file
        if("PART" not in params_map):
            return

        Part = AbaqusPart()

        Part.setName(params_map["NAME"])

        for line in file :
            self.line = line
            self._read_data(file, Part.Nodes, Part.Elements, Part.Nset, Part.Elset, Part, None)
            print("PART: ",self.line)
            if self.line.strip().lstrip("*").upper().startswith("END PART"):
                break

        Parts.append(Part)



    def _read_assembly(self, file, Assembly):
         # get informations about part
        params_map = self._get_param_map(self.line)

        print(params_map)
        # this is not an included file
        if("ASSEMBLY" not in params_map):
            return file.readline()

        Assembly.setName(params_map["NAME"])

        for line in file :
            self.line = line
            self._read_data(file, Assembly.Nodes, Assembly.Elements, Assembly.Nset, Assembly.Elset, None, Assembly)
            print("ASS: ",self.line)
            if self.line.strip().lstrip("*").upper().startswith("END ASSEMBLY"):
                break


    def _read_instance(self, file, Assembly):
         # get informations about part
        params_map = self._get_param_map(self.line)

        print(params_map)
        # this is not an included file
        if("INSTANCE" not in params_map):
            return file.readline()

        Instance = AbaqusInstance()

        Instance.setName(params_map["NAME"])
        Instance.setPart(params_map["PART"])

        for line in file :
            self.line = line
            self._read_data(file, Instance.Nodes, Instance.Elements, Instance.Nset,Instance.Elset, None, None)
            print("INSTANCE: ", self.line)
            if self.line.strip().lstrip("*").upper().startswith("END INSTANCE"):
                break

        Assembly.addInstance(Instance)

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

    # read a string which are in more that one line. If terminates by separator
    def _read_continuous_line(self, file, separator):

        # read the line
        entries= [x.strip() for x in self.line.strip().rstrip(separator).split(separator)]

        # more than one line to read
        if self.line.rstrip().endswith(separator):
            self.line = file.readline()

            if not self.line.lstrip().startswith("*"):
                entries += self._read_continuous_line(file, separator)

        return entries

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

    def splitAndCleanLine(self, my_string, separator):
        return [x.strip() for x in my_string.split(separator)]

    def create_abaqus_mesh(self):
        raise Exception("Not yet implemented")

    def write_abaqus_mesh(self, filename_abaqus):
        raise Exception("Not yet implemented")
