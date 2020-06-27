#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .medconverter import *
import os.path as osp
import numpy as np
import time


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
        self.PartName = " "
        self.Nodes = []
        self.Elements = []
        self.Elset = []
        self.Nset = []
        self.translation = None
        self.rotation = None

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setPartName(self, part_name):
        self.PartName = part_name

    def getPartName(self):
        return self.PartName

    def setPart(self, Part):
        self.setPartName(Part.getName())
        self.Nodes += Part.Nodes
        self.Elements += Part.Elements
        self.Elset += Part.Elset
        self.Nset += Part.Nset

class AbaqusAssembly:

    def __init__(self):
        self.name = " "
        self.Instance = []
        self.Nodes = []
        self.Elements = []
        self.Elset = []
        self.Nset = []
        self.Parts = []

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def addInstance(self, Instance):
        self.Instance.append(Instance)

    def getInstance(self):
        return self.Instance

    def getPart(self, name):
        for part in self.Parts:
            if name == part.getName():
                return part

        raise RuntimeError("Part nod found: " + name)

class AbaqusMesh:

    def __init__(self):
        self.name = " "
        self.Nodes = []
        self.Elements = []
        self.Elset = []
        self.Nset = []
        self.nodesOffset = 0
        self.elemsOffset  = 0

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def translation(self, point, translation):
        return np.array(point) + np.array(translation)

    def matric_rotation(self, axis, angle_radian):
        u = np.array(axis)
        u = u / np.linalg.norm(u)

        c = np.cos(angle_radian)
        s = np.sin(angle_radian)

        row1 = [u[0]*u[0]*(1-c)+c, u[0]*u[1]*(1-c)-u[2]*s, u[0]*u[2]*(1-c) + u[1]*s]
        row2 = [u[0]*u[1]*(1-c)+u[2]*s ,u[1]*u[1]*(1-c)+c,  u[1]*u[2]*(1-c) - u[0]*s]
        row3 = [u[0]*u[2]*(1-c)-u[1]*s, u[1]*u[2]*(1-c) + u[0]*s, u[2]*u[2]*(1-c)+c]

        mrot = np.array([row1,row2, row3])

        return mrot

    def rotation(self, point, center, matric_rotation):
        return matric_rotation @ (np.array(point) - np.array(center)) + np.array(center)

    def geometric_transfo(self, point, translation=None, center=None, matrix_rotation=None):
        if translation is not None:
            transla = self.translation(point, translation)
        else:
            transla = point

        if matrix_rotation is not None:
            rota = self.rotation(transla, center, matrix_rotation)
        else:
            rota = transla

        return tuple(rota)

    def addNodes(self, Nodes, translation=None, rotation_param=None):
        # object for translation + rotation (optimization for large mesh)
        if translation is not None:
            translation = np.array(translation)

        if rotation_param is not None:
            assert translation is not None
            center = np.array(rotation_param[0:3])
            axis = np.array(rotation_param[3:6])
            angle = rotation_param[6]
            angle_radian = np.radians(angle)
            mrot = self.matric_rotation(axis, angle_radian)
        else:
            center, mrot = None, None

        corresponding_nodes = {}
        for idx, node in enumerate(Nodes):
            if int(node.getId()) in corresponding_nodes:
                raise KeyError("Two nodes with identical id: {0}".format(node.getId()))
            else:
                corresponding_nodes[int(node.getId())] = self.nodesOffset + idx

            # add Node
            node_id = corresponding_nodes[int(node.getId())]
            coor = node.getCoordinates()
            new_coor = self.geometric_transfo(coor, translation, center, mrot)
            self.Nodes.append(AbaqusNode(node_id, new_coor))

        self.nodesOffset += len(Nodes)

        return corresponding_nodes

    def addElements(self, Elements, corresponding_nodes):
        corresponding_elems = {}
        for idx, elem in enumerate(Elements):
            if int(elem.getId()) in corresponding_elems:
                raise KeyError("Two elements with identical id: {0}".format(elem.getId()))
            else:
                corresponding_elems[int(elem.getId())] = self.elemsOffset + idx

            nodes_elem = map(int, elem.getNodes())
            list_nodes = tuple(corresponding_nodes[k] for k in nodes_elem)
            elem_id = corresponding_elems[int(elem.getId())]
            self.Elements.append(AbaqusElement(elem.getType(), elem_id, list_nodes))

        self.elemsOffset += len(Elements)

        return corresponding_elems

    def addGroups(self, typeGrp, Groups, corresponding):
        for Group in Groups:
            # add group
            name = Group.getName()
            instance = Group.getInstance()
            items = map(int, Group.getGroup())
            list_clean = []
            # print(Group)
            for k in items:
                if k in corresponding:
                    list_clean.append(k)
                else:
                    print("Group: ", name)
                    print("Create Group: this element %d in not in the mesh"%k)

            if len(list_clean) == 0:
                raise RuntimeError("No items in group: "+name)

            list_item = tuple(corresponding[k] for k in list_clean)
            if typeGrp == "NSET":
                self.Nset.append(AbaqusGroup(name, instance, list_item))
            elif typeGrp == "ELSET":
                self.Elset.append(AbaqusGroup(name, instance, list_item))
            else:
                raise RuntimeError("Unknown type of group")

    def addFromEntities(self, Entities, translation=None, \
                         rotation_param=None):

        tic = time.perf_counter()
        corresponding_nodes = self.addNodes(Entities.Nodes, translation, rotation_param)
        toc = time.perf_counter()
        logger.debug("-> Number of nodes : %d (in %0.4f seconds)"\
            %(len(Entities.Nodes), toc-tic))

        tic = time.perf_counter()
        corresponding_elems = self.addElements(Entities.Elements, corresponding_nodes)
        toc = time.perf_counter()
        logger.debug("-> Number of elements : %d (in %0.4f seconds)"\
            %(len(Entities.Elements), toc-tic))

        tic = time.perf_counter()
        self.addGroups("NSET", Entities.Nset, corresponding_nodes)
        toc = time.perf_counter()
        logger.debug("-> Number of groups of nodes : %d (in %0.4f seconds)"\
            %(len(Entities.Nset), toc-tic))

        tic = time.perf_counter()
        self.addGroups("ELSET", Entities.Elset, corresponding_elems)
        toc = time.perf_counter()
        logger.debug("-> Number of groups of elements : %d (in %0.4f seconds)"\
            %(len(Entities.Elset), toc-tic))


    def addGroupsInRightPlace(self, Assembly):

        new_Nset = []
        for group in Assembly.Nset:
            instance_name = group.getInstance()
            #print(group.getName(), instance_name, len(group.getGroup()))
            if instance_name != "":
                for Instance in Assembly.Instance:
                    if Instance.getName() == instance_name:
                        Instance.Nset.append(group)
            else:
                new_Nset.append(group)

        Assembly.Nset = new_Nset

        new_Elset = []
        for group in Assembly.Elset:
            instance_name = group.getInstance()
            if instance_name != "":
                for Instance in Assembly.Instance:
                    if Instance.getName() == instance_name:
                        Instance.Elset.append(group)
            else:
                new_Elset.append(group)

        Assembly.Elset = new_Elset


    def assemble(self, Assembly):

        self.addGroupsInRightPlace(Assembly)

        # loop on instance of Assembly
        for Instance in Assembly.Instance:
            logger.debug("Processing Instance: "+ Instance.getName())
            self.addFromEntities(Instance, Instance.translation, Instance.rotation)

        # add others objects in assembly
        logger.debug("Processing rest of the mesh: ")
        self.addFromEntities(Assembly)

        # print(self.Nodes)
        # print(self.Elements)
        # print(self.Nset)
        # print(self.Elset)


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
        self.nbAssembly = 0

    def read_abaqus_mesh(self, filename):
        logger.debug("Reading Abaqus mesh file : %s"%filename)

        Assembly = AbaqusAssembly()

        # Lecture du fichier .inp où les blocs sont separés par des *Instance et *End Instance
        with open(filename, 'r', encoding = self._get_file_encoding(filename)) as file :
            self.filename = filename
            self.mesh_name = self._read_meshname(filename)
            # a priori, this is a 3D mesh
            self.space_dim = 3

            logger.debug("Mesh name : %s"%self.mesh_name)
            logger.debug("Space Dimension : %d"%self.space_dim)
            logger.debug("Beginning to parse mesh file")
            tic = time.perf_counter()

            for line in file :
                self.line = line
                self._read_data(file, Assembly)

            toc = time.perf_counter()
            logger.debug("Ending to parse mesh file in %0.4f seconds"%(toc-tic))


        file.close()

        # create Abaqus mesh
        logger.debug(" ")
        logger.debug("Creating Abaqus mesh:")
        tic = time.perf_counter()

        mesh = AbaqusMesh()
        mesh.setName(self.mesh_name)
        mesh.assemble(Assembly)

        toc = time.perf_counter()

        logger.debug("End creating Abaqus mesh in %0.4f seconds"%(toc-tic))



        logger.debug("Statistics of the mesh : " + mesh.getName())
        logger.debug("-> Number of nodes : %d"%(len(mesh.Nodes)))
        logger.debug("-> Number of elements : %d"%(len(mesh.Elements)))
        logger.debug("-> Number of groups of nodes : %d"%(len(mesh.Nset)))
        logger.debug("-> Number of groups of elements : %d"%(len(mesh.Elset)))

        # nodes of the mesh (collection of double)
        corresponding_nodes = {}
        coor = []
        for idx, node in enumerate(mesh.Nodes):
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

        for elem in mesh.Elements :
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
        for group in mesh.Nset :
            group_name = group.getName()
            group_nodes_abaqus = map(int, group.getGroup())
            if not group_name in self.groups_n:  self.groups_n[group_name] = []
            self.groups_n[group_name] += [corresponding_nodes[k] for k in group_nodes_abaqus]

        # Element's group
        for group in mesh.Elset :
            group_name = group.getName()
            group_element_abaqus = map(int, group.getGroup())

            for element_abaqus in group_element_abaqus :
                for key in self.elements.keys():
                    if element_abaqus in corresponding_elements[key]:
                        if not key in self.groups_e : self.groups_e[key] = {}
                        if not group_name in self.groups_e[key]:  self.groups_e[key][group_name] = []
                        self.groups_e[key][group_name].append(corresponding_elements[key][element_abaqus])

    def _read_meshname(self, filename):
        return osp.splitext(osp.basename(filename))[0]

    def _read_data(self, file, Entities):
        self.line = self.line.strip()

        if(self.line.upper().startswith("*NODE")):
            self._read_nodes(file, Entities.Nodes, Entities.Nset)
            # print("Nodes")
            # print(Entities.Nodes)
            self._read_data(file, Entities)
        elif(self.line.upper().startswith("*ELEMENT")):
            self._read_cells(file, Entities.Elements, Entities.Elset)
            # print("Cells")
            # print(Entities.Elements)
            self._read_data(file, Entities)
        elif(self.line.upper().startswith("*NSET")):
            self._read_group(file, "NSET", Entities.Nset)
            # print("Nset")
            # print(Entities.Nset)
            self._read_data(file, Entities)
        elif self.line.upper().startswith('*ELSET'):
            self._read_group(file, "ELSET", Entities.Elset)
            # print("Elset")
            # print(Entities.Elset)
            self._read_data(file, Entities)
        elif self.line.upper().startswith('*INCLUDE'):
            self._read_include_file(file, Entities)
        elif self.line.upper().startswith('*INSTANCE'):
            self._read_instance(file,  Entities)
        elif self.line.upper().startswith('*PART'):
            self._read_part(file, Entities.Parts)
        elif self.line.upper().startswith('*ASSEMBLY'):
            self._read_assembly(file, Entities)
            self.nbAssembly += 1

            if(self.nbAssembly > 1):
                raise RuntimeError("Only one Assembly allowed")
        elif self.line.upper().startswith('*NGEN'):
            raise RuntimeError("Keyword not supported: NGEN")
        elif self.line.upper().startswith('*NFILL',):
            raise RuntimeError("Keyword not supported: NFILL")
        elif self.line.upper().startswith('*NMAP'):
            raise RuntimeError("Keyword not supported: NMAP")
        elif self.line.upper().startswith('*NCOPY'):
            raise RuntimeError("Keyword not supported: NMAP")

    def _read_nodes(self, file, Nodes, Nset):
        # get informations about nodes
        params_map = self._get_param_map(self.line)

        # this is not a list of node
        if("*NODE" not in params_map):
            self.line = file.readline()
            return

        logger.debug("-> Reading Nodes")


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
            l_process_line = True
            if(l_extern_file):
                if self.line.startswith("*"):
                    if(self.line.upper().startswith("*NODE")):
                        self._read_nodes(file_to_read, Nodes, Nset)
                    else:
                        l_process_line = False

                if self.line == "":
                    break
                elif self.line in ['\n', '\r\n']:
                    break
            elif self.breakLoop(self.line):
                break

            if not self.line.startswith("**"):
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
            Nset.append(AbaqusGroup(name, "", [int(n) for n in list_nodes]))

        if(l_extern_file):
            file_to_read.close()
            self.line = file.readline()


    # Read a list of element
    def _read_cells(self, file, Elements, Elset):
        # get informations about elements
        params_map = self._get_param_map(self.line)

        # this is not a list of element
        if("*ELEMENT" not in params_map):
            self.line = file.readline()
            return

        logger.debug("-> Reading Elements : " + params_map["TYPE"])


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
            self.line = file_to_read.readline()

            l_process_line = True
            if(l_extern_file):
                if self.line.startswith("*"):
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

            if not self.line.startswith("**"):
                if l_process_line:
                    entries= self._read_continuous_line(file_to_read, ",")
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
            Elset.append(AbaqusGroup(name, "", [int(n) for n in list_elem]))

        if(l_extern_file):
            file_to_read.close()
            self.line = file.readline()


    def _read_group(self, file, typyeGroup, Group):
        # find type of element
        params_map = self._get_param_map(self.line)

        # this is not a group
        if typyeGroup not in params_map:
            self.line = file.readline()
            return

        # to generate groups
        if("GENERATE" in params_map.keys()):
            generate = True
        else:
            generate = False

        # to generate groups
        if("INSTANCE" in params_map.keys()):
            instance = params_map["INSTANCE"]
        else:
            instance = ""

        logger.debug("-> Reading Group: " + params_map[typyeGroup] + " (" + typyeGroup +")")

        list_item = []
        while True:
            self.line = file.readline()
            if self.breakLoop(self.line):
                break

            if not self.line.startswith("**"):
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

        if len(list_item) == 0:
            raise RuntimeError("No items for this group: "+params_map[typyeGroup])
        # add group
        name = params_map[typyeGroup]
        Group.append(AbaqusGroup(name, instance, [int(n) for n in list_item]))


    # Read an included file
    def _read_include_file(self, file, Entities):
        # get informations about file
        params_map = self._get_param_map(self.line)

        # this is not an included file
        if("INPUT" not in params_map):
            return

        # open external file
        filename_elem = osp.dirname(self.filename) + "/"+ params_map["INPUT"]
        file_to_read = open(filename_elem, 'r')

        logger.debug("-> Reading included file: " + filename_elem)

        # read external file
        for self.line in file_to_read :
            self._read_data(file_to_read, Entities)

        file_to_read.close()

    def _read_part(self, file, Parts):
         # get informations about part
        params_map = self._get_param_map(self.line)

        # this is not an included file
        if("*PART" not in params_map):
            return

        Part = AbaqusPart()

        Part.setName(params_map["NAME"])

        logger.debug("-> Reading Part: " + Part.getName())

        l_finish = False
        for line in file :
            self.line = line
            self._read_data(file, Part)
            if self.line.strip().upper().startswith("*END PART"):
                l_finish = True
                break

        if not l_finish:
            raise RuntimeError("Not Find: End Part")

        Parts.append(Part)


    def _read_assembly(self, file, Assembly):
         # get informations about part
        params_map = self._get_param_map(self.line)

        # this is not an included file
        if("*ASSEMBLY" not in params_map):
            return

        Assembly.setName(params_map["NAME"])

        l_finish = False
        for line in file :
            self.line = line
            self._read_data(file, Assembly)
            if self.line.strip().upper().startswith("*END ASSEMBLY"):
                l_finish = True
                break

        if not l_finish:
            raise RuntimeError("Not Find: End Assembly")


    def _read_instance(self, file, Assembly):
         # get informations about part
        params_map = self._get_param_map(self.line)

        # this is not an included file
        if("*INSTANCE" not in params_map):
            return

        Instance = AbaqusInstance()

        Instance.setName(params_map["NAME"])
        Instance.setPart(Assembly.getPart(params_map["PART"]))

        logger.debug("-> Reading Instance: " + Instance.getName())


        l_finish = False
        l_first_line = True
        for line in file :
            self.line = line
            if l_first_line:
                # read translation
                if not self.line.strip().startswith("*"):
                    Instance.translation = [float(x.strip()) for x in self.line.strip().rstrip(',').split(',')]
                    assert len(Instance.translation) == 3
                    self.line = file.readline()
                    if not self.line.strip().startswith("*"):
                        Instance.rotation = [float(x.strip()) for x in self.line.strip().rstrip(',').split(',')]
                        assert len(Instance.rotation) == 7
                        self.line = file.readline()

                l_first_line = False

            self._read_data(file, Instance)

            if self.line.strip().upper().startswith("*END INSTANCE"):
                l_finish = True
                break

        if not l_finish:
            raise RuntimeError("Not Find: End Instance")

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
        if line.startswith("*") and not line.startswith("**"):
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
