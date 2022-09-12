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
import inspect

class Scene:
    def __init__(self, content):
        self.content = content

    def print(self):
        for c in self.content:
            c.print(0)

class Node:
    def __init__(self, name, body):
        self.name = name
        self.fields = []
        self.events = []

        for el in body:
            if type(el) == Field:
                self.fields += [el]

    def print(self, level):
        iprint(level, "Node: {}".format(self.name))
        iprint(level, "Fields:")
        for f in self.fields:
            f.print(level + 1)

class DefinedNode(Node):
    def __init__(self, name, node):
        self.name = name
        self.node = node

    def print(self, level):
        iprint(level, "DEF: {}".format(self.name))
        self.node.print(level + 1)

class UsedNode(Node):
    def __init__(self, name):
        self.name = name

    def print(self, level):
        iprint(level, "USE: {}".format(self.name))

class Field:
    def __init__(self, id, content):
        self.id = id
        self.content = content

    def print(self, level):
        iprint(level, "Field: {}".format(self.id))
        for c in self.content:
            if type(c) == list:
                literals = False
                for ci in c:
                    if type(ci) in [Node, DefinedNode, UsedNode]:
                        ci.print(level + 1)
                    else:
                        literals = True
                if literals:
                    iprint(level + 1, "literals...")
            if type(c) in [Node, DefinedNode, UsedNode]:
                c.print(level + 1)
            else:
                iprint(level + 1, "literals...")

