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
    p[0] = p[1]

def p_statements(p):
    '''statements : statement statements
                    | empty'''
    if(p[1] == None):
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_statement(p):
    '''statement  : nodeStatement
                  | protoStatement
                  | routeStatement'''
    p[0] = p[1]

def p_nodeStatement(p):
    '''nodeStatement : node
                     | DEF ID node
                     | USE ID
                     | NULL'''
    if(len(p[1:]) == 1):
        if(p[1] != "NULL"):
            p[0] = p[1]
        else:
            p[0] = None
    else:
        if(p[1] == 'DEF'):
            p[0] = {"type": "defined_node", "name": p[2], "content": p[3]}
        elif(p[1] == 'USE'):
            p[0] = {"type": "used_node", "name": p[2]}

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
        p[0] = {"type":"node", "name": p[1], "content": p[3]}

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
        if(p[2] != 'IS'):
            p[0] = {"type": "field", "name": p[1], "content": p[2]}

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
    if(len(p[1:]) == 2):
        p[0] = []
    else:
        p[0] = [p[1]]
# Bool values
def p_sfboolValue(p):
    '''sfboolValue : TRUE
                   | FALSE'''
    p[0] = True if p[1] == "TRUE" else False
# Float values
def p_sffloatValues(p):
    '''sffloatValues : FLOAT sffloatValues
                     | empty'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = [float(p[1])] + p[2]
def p_mffloatValue(p):
    '''mffloatValue : sffloatValues
                    | OSB sffloatValues CSB'''
    if len(p[1:]) > 1:
        p[0] = p[2]
    else:
        p[0] = p[1]
# Int Values
def p_sfint32Values(p):
    '''sfint32Values : INT32 sfint32Values
                     | empty'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = [int(p[1])] + p[2]
def p_mfint32Value(p):
    '''mfint32Value : sfint32Values
                    | OSB sfint32Values CSB'''
    if len(p[1:]) > 1:
        p[0] = p[2]
    else:
        p[0] = p[1]
# Node values
def p_nodeStatements(p):
    '''nodeStatements : nodeStatement nodeStatements
                      | empty'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]
def p_mfnodeValue(p):
    '''mfnodeValue : nodeStatement
                   | OSB nodeStatements CSB'''
    if len(p[1:]) > 1:
        p[0] = p[2]
    else:
        p[0] = p[1]
# String values
def p_sfstringValues(p):
    '''sfstringValues : STRING sfstringValues
                      | empty'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]
def p_mfstringValue(p):
    '''mfstringValue : sfstringValues
                     | OSB sfstringValues CSB'''
    if len(p[1:]) > 1:
        p[0] = p[2]
    else:
        p[0] = p[1]
def p_empty(p):
    '''empty : '''
    pass

def p_error(p):
    if p == None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")

def parse(data):
    # Create the lexer
    lexer = lex.lex(module=toks)
    # Create the parser
    parser = yacc.yacc()
    # Parse the file
    content = parser.parse(data,tracking=True, debug=False)
    scene = Scene(content)
    return scene 

def parse_file(filename):
    with open(filename) as f:
        content = "".join(f.readlines())
        f.close()
        return parse(content)
