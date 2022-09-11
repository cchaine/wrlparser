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

class Node:
    def __init__(self, name, body):
        self.name = name
        self.fields = []
        self.events = []

    def add_field(self, field):
        self.fields += [field]

    def add_event(self, event):
        self.events += [event]

#class GroupingNode(Node):

#class ScriptNode(Node):
#    def __init__(self):
#        self.name = "Script"

class Field:
    def __init__(self, id):
        self.id = id

class Event:
    def __init__(self):
        print("event")
