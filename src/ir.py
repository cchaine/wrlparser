#           __        _
#  ________/ /  ___ _(_)__  ___
# / __/ __/ _ \/ _ `/ / _ \/ -_)
# \__/\__/_//_/\_,_/_/_//_/\__/
# 
# Copyright (C) Clément Chaine
# This file is part of wrlparser <https://github.com/cchaine/wrlparser>
# 
# wrlparser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# wrlparser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with wrlparser.  If not, see <http://www.gnu.org/licenses/>.

from log import iprint
import inspect, sys
from rich.console import Console

console = Console()

def _log(message, level=0):
    indent = "  "*level
    console.print("{}{}".format(indent, message))

def _error(message):
    console.print("Error: {}".format(message), style="red")

def _nimp(message):
    # this variable is a flag indicating something was not implemented
    global found_nimp
    found_nimp = True

    console.print("Warning: {}".format(message), style="orange3")

class Scene:
    """Extract the content of the scene"""
    def __init__(self, content):
        # initialize global variables
        # used to check if a not-implemented warning appeared
        global found_nimp
        found_nimp = False
        # used to keep track of defined nodes
        global defined_nodes
        defined_nodes = []

        # extract the nodes
        self.nodes = []

        for element in content:
            element_type = element["type"]
            if element_type == "defined_node":
                self._add_defined_node(element["name"], element["content"])
            elif element_type == "node":
                self._add_node(element["name"], element["content"])
            else:
                _nimp("Found element type '{}' in scene which is not implemented".format(element_type))
                return

        if found_nimp:
            _log("")
            _log("Some types encountered have not been implemented yet")
            _log("Please consider contributing or submitting an issue on github.", 1)
            _log("https://github.com/cchaine/wrlparser/issues", 1)

    def _add_node(self, name, content):
        if name == "Shape":
            node = Shape(content)
            self.nodes += [node]
        else:
            _nimp("Found node type '{}' which is not implemented".format(name))

    def _add_defined_node(self, name, node):
        # the content must be a node
        if node["type"] == "node":
            self._add_node(node["name"], node["content"]) 
        else:
            _error("Content of '{}' should be 'node' but found '{}'".format(name, node["type"]))

class Shape:
    def __init__(self, content):
        self.geometry = None
        self.appearance = None

        for element in content:
            if element["type"] == "field":
                if element["name"] == "geometry":
                    self._process_geometry(element["content"])
                elif element["name"] == "appearance":
                    self._process_appearance(element["content"])
                else:
                    _nimp("Found field type '{}' in node 'Shape' which is not implemented".format(element["name"]))
            else:
                _nimp("Found element type '{}' in node 'Shape' which is not implemented".format(element["type"]))
    
    """ process geometry field """
    def _process_geometry(self, content):
        if len(content) > 1:
            _error("There should only be one element in field of type 'geometry'")
            return

        element = content[0]
        if element["type"] == "node":
            if element["name"] == "IndexedFaceSet":
                self.geometry = IndexedFaceSet(element["content"])
            else:
                _nimp("Found node name '{}' in field 'geometry' which is not implemented".format(element["name"]))
        else:
            _error("Content of 'geometry' should be 'node' but found '{}'".format(element["type"]))

    """ process appearance field """
    def _process_appearance(self, content):
        if len(content) > 1:
            _error("There should only be one element in field of type 'appearance'")
            return

        element = content[0]
        if element["type"] == "node":
            if element["name"] == "Appearance":
                self.appearance = Appearance(element["content"])
            else:
                _nimp("Found node name '{}' in field 'appearance' which is not implemented".format(element["name"]))
        else:
            _error("Content of 'appearance' should be 'node' but found '{}'".format(element["type"]))

class Appearance:
    def __init__(self, content):
        self.material = None

        for element in content:
            if element["type"] == "field":
                if element["name"] == "material":
                    self._process_material(element["content"])
                else:
                    _nimp("Found field named '{}' in node 'Appearance' which is not implemented".format(element["name"]))
            else:
                _nimp("Found element type '{}' in node 'Appearance' which is not implemented".format(element["type"]))

    def _process_material(self, content):
        if len(content) > 1:
            _error("There should only be one node in field of type 'material'")
            return

        element = content[0]
        if element["type"] == "defined_node":
            global defined_nodes
            # a defined node has a name and a node associated
            if element["content"]["type"] == "node":
                node = element["content"]
                if node["name"] == "Material":
                    self.material = Material(node["content"])
                    # add the node to the list of defined_nodes
                    defined_nodes += [{"name": element["name"], "content": self.material}]
                else:
                    _error("Found node type '{}' in field 'material' which should be 'Material'".format(element["name"]))
            else:
                _error("Content of 'defined_node' should be 'node' but found '{}'".format(element["content"]["type"]))
        elif element["type"] == "used_node":
            # look for a node previously defined in the defined_nodes global array
            used_node = None
            for node in defined_nodes:
                if node["name"] == element["name"]:
                    self.material = node["content"]
        else:
            _error("Content of 'material' should be in ['defined_node', 'used_node'] but found '{}'".format(element["type"]))

class IndexedFaceSet:
    def __init__(self, content):
        self.coordIndex = None
        self.coord = None

        for element in content:
            if element["type"] == "field":
                if element["name"] == "coordIndex":
                    self._process_coordIndex(element["content"])
                elif element["name"] == "coord":
                    self._process_coord(element["content"])
                else:
                    _nimp("Found field named '{}' in node 'IndexedFaceSet' which is not implemented".format(element["name"]))
            else:
                _nimp("Found element type '{}' in node 'IndexedFaceSet' which is not implemented".format(element["type"]))
    
    """ Process coordIndex field"""
    def _process_coordIndex(self, content):
        if len(content) > 1:
            _error("There should only be one node in field of type 'coordIndex'")
            return

        element = content[0]

        faces = []
        face = []
        for value in element:
            # a face ends with the value -1
            if value == -1:
                faces += [face]
                face = []
            else:
                face += [value]
        # the last face doesn't have to end with a -1
        if len(face) != 0:
            faces += [face]
        # set the field
        self.coordIndex = faces

    """ Process coord field """
    def _process_coord(self, content):
        if len(content) > 1:
            _error("There should only be one node in field of type 'material")
            return

        element = content[0]
        if element["type"] == "node":
            if element["name"] == "Coordinate":
                self.coord = Coordinate(element["content"])
            else:
                _error("Found node type '{}' in field 'coord' which should be 'Coordinate'".format(element["name"]))
        else:
            _error("Content of 'material' should be 'node' but found '{}'".format(element["type"]))

class Coordinate:
    def __init__(self, content):
        self.point = None

        for element in content:
            if element["type"] == "field":
                if element["name"] == "point":
                    self._process_point(element["content"])
                else:
                    _nimp("Found field named '{}' in node 'IndexedFaceSet' which is not implemented".format(element["name"]))
            else:
                _nimp("Found element type '{}' in node 'Coordinate' which is not implemented".format(element["type"]))

    """ Process point field """
    def _process_point(self, content):
        if len(content) > 1:
            _error("There should only be one node in field of type 'point'")
            return

        element = content[0]

        self.point = []
        for i in range(0, len(element), 3):
            self.point += [element[i:i + 3]]

class Material:
    def __init__(self, content):
        self.ambientIntensity  =  None;
        self.diffuseColor      =  None;
        self.specularColor     =  None;
        self.emissiveColor     =  None;
        self.transparency      =  None;
        self.shininess         =  None;

        for element in content:
            if element["type"] == "field":
                if element["name"] == "ambientIntensity":
                    self._process_ambientIntensity(element["content"])
                elif element["name"] == "diffuseColor":
                    self._process_diffuseColor(element["content"])
                elif element["name"] == "specularColor":
                    self._process_specularColor(element["content"])
                elif element["name"] == "emissiveColor":
                    self._process_emissiveColor(element["content"])
                elif element["name"] == "transparency":
                    self._process_transparency(element["content"])
                elif element["name"] == "shininess":
                    self._process_shininess(element["content"])
                else:
                    _nimp("Found field type '{}' in node 'Shape' which is not implemented".format(element["name"]))
            else:
                _nimp("Found element type '{}' in node 'Shape' which is not implemented".format(element["type"]))

    def _process_ambientIntensity(self, content):
        if len(content) > 1:
            _error("There should only be one node in field of type 'ambientIntensity'")
            return

        element = content[0]
        self.ambientIntensity = element[0]

    def _process_diffuseColor(self, content):
        if len(content) > 1:
            _error("There should only be one node in field of type 'diffuseColor'")
            return

        element = content[0]
        self.diffuseColor = element

    def _process_specularColor(self, content):
        if len(content) > 1:
            _error("There should only be one node in field of type 'specularColor'")
            return

        element = content[0]
        self.specularColor = element

    def _process_emissiveColor(self, content):
        if len(content) > 1:
            _error("There should only be one node in field of type 'emissiveColor'")
            return

        element = content[0]
        self.emissiveColor = element

    def _process_transparency(self, content):
        if len(content) > 1:
            _error("There should only be one node in field of type 'transparency'")
            return

        element = content[0]
        self.transparency = element[0]

    def _process_shininess(self, content):
        if len(content) > 1:
            _error("There should only be one node in field of type 'shininess'")
            return

        element = content[0]
        self.shininess = element[0]
