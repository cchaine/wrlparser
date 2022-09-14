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
        # reset the not-implemented flag
        global found_nimp
        found_nimp = False

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
            console.print("")
            console.print("Info: Some types encountered have not been implemented yet")
            console.print("      Please consider contributing or submitting an issue on github.")
            console.print("      https://github.com/cchaine/wrlparser/issues")

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

    def print(self):
        pass

class Shape:
    def __init__(self, content):
        self.geometry = None
        self.appearance = None

        for element in content:
            if element["type"] == "field":
                if element["name"] == "geometry":
                    # there should only be one node in the geometry field
                    if len(element["content"]) == 1 and element["content"][0]["type"] == "node":
                        node = element["content"][0]
                        if node["name"] == "IndexedFaceSet":
                            self.geometry = IndexedFaceSet(node["content"])
                        else:
                            _nimp("Found node name '{}' in field 'geometry' which is not implemented".format(node["name"]))
                    else:
                        wasfound = "[" + "".join(["'{}',".format(x[0]) for x in element["content"]])[:-1] + "]"
                        _error("Content of field 'geometry' should be 'node' but found {}".format(wasfound))
                elif element["name"] == "appearance":
                    self.appearance = Appearance(element["content"])
                else:
                    _nimp("Found field type '{}' in node 'Shape' which is not implemented".format(element["name"]))
            else:
                _nimp("Found element type '{}' in node 'Shape' which is not implemented".format(element["type"]))

class Appearance:
    def __init__(self, content):
        pass

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
    
    """ Process field coordIndex """
    def _process_coordIndex(self, content):
        faces = []
        face = []
        for value in content:
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

    """ Process field coord """
    def _process_coord(self, content):
        # there should only be one node in the coord field
        if len(content) == 1 and content[0]["type"] == "node":
            node = content[0]
            if node["name"] == "Coordinate":
                self.coord = Coordinate(node["content"])
            else:
                _error("Found node type '{}' in field 'coord' which should be 'Coordinate'".format(node["name"]))
        else:
            wasfound = "[" + "".join(["'{}',".format(x[0]) for x in content])[:-1] + "]"
            _error("Content of 'coord' should be 'node' but found {}".format(wasfound))

class Coordinate:
    def __init__(self, content):
        print(content)
