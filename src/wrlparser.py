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

import ply.lex as lex
import ply.yacc as yacc
from toks import tokens
import toks
from ir import *

import inspect, os, logging

# GENERAL

def p_vrmlscene(p):
    '''vrmlscene : statements'''

def p_statements(p):
    '''statements : statement statements
                    | empty'''

def p_statement(p):
    '''statement  : nodeStatement
                  | protoStatement
                  | routeStatement'''

def p_nodeStatement(p):
    '''nodeStatement : node
                     | DEF ID node
                     | USE ID
                     | NULL'''

def p_rootNodeStatement(p):
    '''rootNodeStatement : node 
                         | DEF ID node'''

def p_protoStatement(p):
    '''protoStatement : proto
                      | externproto'''

def p_protoStatements(p):
    '''protoStatements : protoStatement protoStatements
                       | empty'''

def p_proto(p):
    '''proto : PROTO ID OSB interfaceDeclarations CSB OCB protoBody CCB'''

def p_protoBody(p):
    '''protoBody : protoStatements rootNodeStatement statements'''

def p_interfaceDeclarations(p):
    '''interfaceDeclarations : interfaceDeclaration interfaceDeclarations
                             | empty'''

def p_restrictedInterfaceDeclaration(p):
    '''restrictedInterfaceDeclaration : EVENTIN fieldType ID
                                      | EVENTOUT fieldType ID
                                      | FIELD fieldType ID fieldValue'''

def p_interfaceDeclaration(p):
    '''interfaceDeclaration : restrictedInterfaceDeclaration
                            | EXPOSEDFIELD fieldType ID fieldValue'''

def p_externproto(p):
    '''externproto : EXTERNPROTO ID OSB externInterfaceDeclarations CSB URLList'''

def p_externInterfaceDeclarations(p):
    '''externInterfaceDeclarations : externInterfaceDeclaration externInterfaceDeclarations
                                   | empty'''

def p_externInterfaceDeclaration(p):
    '''externInterfaceDeclaration : EVENTIN fieldType ID
                                  | EVENTOUT fieldType ID
                                  | FIELD fieldType ID
                                  | EXPOSEDFIELD fieldType ID'''

def p_routeStatement(p):
    '''routeStatement : ROUTE ID DOT ID TO ID DOT ID'''

def p_URLList(p):
    '''URLList : mfstringValue'''

# NODES

def p_node(p):
    '''node : ID OCB nodeBody CCB
            | SCRIPT OCB scriptBody CCB'''
    if(p[1] != "SCRIPT"):
        p[0] = Node(p[1], p[3])

def p_nodeBody(p):
    '''nodeBody : nodeBodyElement nodeBody 
                | empty'''
    # This is a recursive processing 
    if(p[1] == None):
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]
def p_scriptBody(p):
    '''scriptBody : scriptBodyElement scriptBody 
                  | empty'''
def p_scriptBodyElement(p):
    '''scriptBodyElement : nodeBodyElement
                         | restrictedInterfaceDeclaration
                         | EVENTIN fieldType ID IS ID
                         | EVENTOUT fieldType ID IS ID
                         | FIELD fieldType ID IS ID'''
def p_nodeBodyElement(p):
    '''nodeBodyElement : ID fieldValue
                       | ID IS ID
                       | routeStatement
                       | protoStatement'''
    # If anything other than route and proto
    if(len(p[1:]) > 1):
        p[0] = Field(p[1])

# FIELDS


def p_fieldType(p):
    '''fieldType : MFCOLOR
                 | MFFLOAT
                 | MFINT32
                 | MFNODE
                 | MFROTATION
                 | MFSTRING
                 | MFTIME
                 | MFVEC2F
                 | MFVEC3F
                 | SFBOOL
                 | SFCOLOR
                 | SFFLOAT
                 | SFIMAGE
                 | SFINT32
                 | SFNODE
                 | SFROTATION
                 | SFSTRING
                 | SFTIME
                 | SFVEC2F
                 | SFVEC3F'''
def p_fieldValue(p):
    '''fieldValue : OSB CSB
                  | sfboolValue
                  | mffloatValue
                  | mfint32Value
                  | mfnodeValue
                  | mfstringValue'''
# Bool values
def p_sfboolValue(p):
    '''sfboolValue : TRUE
                   | FALSE'''
# Float values
def p_sffloatValues(p):
    '''sffloatValues : FLOAT sffloatValues
                     | empty'''
def p_mffloatValue(p):
    '''mffloatValue : sffloatValues
                    | OSB sffloatValues CSB'''
# Int Values
def p_sfint32Values(p):
    '''sfint32Values : INT32 sfint32Values
                     | empty'''
def p_mfint32Value(p):
    '''mfint32Value : sfint32Values
                    | OSB sfint32Values CSB'''
# Node values
def p_mfnodeValue(p):
    '''mfnodeValue : nodeStatement
                   | OSB nodeStatements CSB'''
def p_nodeStatements(p):
    '''nodeStatements : nodeStatement nodeStatements
                      | empty'''
# String values
def p_sfstringValues(p):
    '''sfstringValues : STRING sfstringValues
                      | empty'''
def p_mfstringValue(p):
    '''mfstringValue : sfstringValues
                     | OSB sfstringValues CSB'''

def p_empty(p):
    '''empty : '''
    pass

def p_error(p):
    if p == None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")

def parse(data, backend):
    # Get the path to the calling function
    abs_path = os.path.abspath((inspect.stack()[1])[1])
    parsedir = os.path.dirname(abs_path)

    # Create the lexer
    lex.lex(module=toks)

    # Create the parser
    parser = yacc.yacc(outputdir=parsedir)

    # Parse the file
    parser.parse(data,tracking=True, debug=False)
