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

import ply.lex as lexer
import ply.yacc as yacc
from lex import tokens

# GENERAL

def p_vrmlscene(p):
    '''vrmlscene : statements'''
    p[0] = p[1]

def p_statements(p):
    '''statements : statement
                    | statement statements
                    | empty'''

def p_statement(p):
    '''statement  : nodeStatement
                  | protoStatement
                  | routeStatement'''

def p_nodeStatement(p):
    '''nodeStatement : node
                     | DEF nodeNameId node
                     | USE nodeNameId'''

def p_rootNodeStatement(p):
    '''rootNodeStatement : node 
                         | DEF nodeNameId node'''

def p_protoStatement(p):
    '''protoStatement : proto
                      | externproto'''

def p_protoStatements(p):
    '''protoStatements : protoStatement
                       | protoStatement protoStatements
                       | empty'''

def p_proto(p):
    '''proto : PROTO nodeTypeId OSB interfaceDeclarations CSB OCB protoBody CCB'''

def p_protoBody(p):
    '''protoBody : protoStatements rootNodeStatement statements'''

def p_interfaceDeclarations(p):
    '''interfaceDeclarations : interfaceDeclaration
                             | interfaceDeclaration interfaceDeclarations
                             | empty'''

def p_restrictedInterfaceDeclaration(p):
    '''restrictedInterfaceDeclaration : EVENTIN fieldType eventInId
                                      | EVENTOUT fieldType eventOutId
                                      | FIELD fieldType fieldId fieldValue'''

def p_interfaceDeclaration(p):
    '''interfaceDeclaration : restrictedInterfaceDeclaration
                            | EXPOSEDFIELD fieldType fieldId fieldValue'''

def p_externproto(p):
    '''externproto : EXTERNPROTO nodeTypeId OSB externInterfaceDeclarations CSB URLList'''

def p_externInterfaceDeclarations(p):
    '''externInterfaceDeclarations : externInterfaceDeclaration
                                   | externInterfaceDeclaration externInterfaceDeclarations
                                   | empty'''

def p_externInterfaceDeclaration(p):
    '''externInterfaceDeclaration : EVENTIN fieldType eventInId
                                  | EVENTOUT fieldType eventOutId
                                  | FIELD fieldType fieldId
                                  | EXPOSEDFIELD fieldType fieldId'''

def p_routeStatement(p):
    '''routeStatement : ROUTE nodeNameId DOT eventOutId TO nodeNameId DOT eventInId'''

def p_URLList(p):
    '''URLList : mfstringValue'''

# NODES

def p_node(p):
    '''node : nodeTypeId OCB nodeBody CCB
            | SCRIPT OCB scriptBody CCB'''
def p_nodeBody(p):
    '''nodeBody : nodeBodyElement
                | nodeBodyElement nodeBodyElements
                | empty'''
def p_scriptBody(p):
    '''scriptBody : scriptBodyElement
                  | scriptBodyElement scriptBodyElements
                  | empty'''
def p_scriptBodyElement(p):
    '''scriptBodyElement : nodeBodyElement
                         | restrictedInterfaceDeclaration
                         | EVENTIN fieldType eventInId IS eventInId
                         | EVENTOUT fieldType eventOutId IS eventOutId
                         | FIELD fieldType fieldId IS fieldId'''
def p_nodeBodyElement(p):
    '''nodeBodyElement : fieldId fieldValue
                       | fieldId IS fieldId
                       | eventInId IS eventInId
                       | eventOutId IS eventOutId
                       | routeStatement
                       | protoStatement'''
def p_nodeNameId(p):
    '''nodeNameId : Id'''
def p_nodeTypeId(p):
    '''nodeTypeId : Id'''
def p_fieldId(p):
    '''fieldId : Id'''
def p_eventInId(p):
    '''eventInId : Id'''
def p_eventOutId(p):
    '''eventOutId : Id'''
def p_Id(p):
    '''Id : IdFirstChar
          | IdFirstChar IdRestChars'''
def p_IdFirstChar(p):
    '''IdFirstChar : IDFIRSTCHAR'''
def p_IdRestChars(p):
    '''IdRestChars : IDRESTCHARS'''

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
    '''fieldValue : sfboolValue
                  | sfcolorValue
                  | sffloatValue
                  | sfimageValue
                  | sfint32Value
                  | sfnodeValue
                  | sfrotationValue
                  | sfstringValue
                  | sftimeValue
                  | sfvec2fValue
                  | sfvec3fValue
                  | mfcolorValue
                  | mffloatValue
                  | mfint32Value
                  | mfnodeValue
                  | mfrotationValue
                  | mfstringValue
                  | mftimeValue
                  | mfvec2fValue
                  | mfvec3fValue'''
def p_sfboolValue(p):
    '''sfboolValue : TRUE
                   | FALSE'''
def p_sfcolorValue(p):
    '''sfcolorValue : float float float'''
def p_sffloatValue(p):
    '''sffloatValue : float'''
def p_float(p):
    '''float : FLOAT'''
def p_sfimageValue(p):
    '''sfimageValue : int32
                    : int32 sfimaveValue
                    : empty'''
def p_sfint32Value(p):
    '''sfint32Value : int32'''
def p_int32(p):
    '''int32 : INT32'''
def p_sfnodeValue(p):
    '''sfnodeValue : nodeStatement
                   : NULL'''
def p_sfrotationValue(p):
    '''sfrotationValue : float float float float'''
def p_sfstringValue(p):
    '''sfstringValue : string'''
def p_string(p):
    '''string : STRING'''
def p_sftimeValue(p):
    '''sftimeValue : double'''
def p_double(p):
    '''double : DOUBLE'''
def p_mftimeValue(p):
    '''mftimeValue : sftimeValue
                   | OSB CSB
                   | OSB sftimeValues CSB'''
def p_sftimeValues(p):
    '''sftimeValues : sftimeValue
                    | sftimeValue sfTimeValues
                    | empty'''
def p_sfvec2fValue(p):
    '''sfvec2fValue : float float'''
def p_sfvec3fValue(p):
    '''sfvec3fValue : float float float'''
def p_mfcolorValue(p):
    '''mfcolorValue : sfcolorValue
                    | OSB CSB
                    | OSB sfcolorValues CSB'''
def p_sfcolorValues(p):
    '''sfcolorValues : sfcolorValue
                     | sfcolorValue sfcolorValues
                     | empty'''
def p_mffloatValue(p):
    '''mffloatValue : sffloatValue
                    | OSB CSB
                    | OSB sffloatValues CSB'''
def p_sffloatValues(p):
    '''sffloatValues : sffloatValue
                     | sffloatValue sffloatValues
                     | empty'''
def p_mfint32Value(p):
    '''mfint32Value : sfint32Value
                    | OSB CSB
                    | OSB sfint32Values CSB'''
def p_sfint32Values(p):
    '''sfint32Values : sfint32Value
                     | sfint32Value sfint32Values
                     | empty'''
def p_mfnodeValue(p):
    '''mfnodeValue : nodeStatement
                   | OSB CSB
                   | OSB nodeStatements CSB'''
def p_nodeStatements(p):
    '''nodeStatements : nodeStatement
                      | nodeStatement nodeStatements
                      | empty'''
def p_mfrotationValue(p):
    '''mfrotationValue : sfrotationValue
                       | OSB CSB
                       | OSB sfrotationValues CSB'''
def p_sfrotationValues(p):
    '''sfrotationValues : sfrotationValue
                        | sfrotationValue sfrotationValues
                        | empty'''
def p_mfstringValue(p):
    '''mfstringValue : sfstringValue
                     | OSB CSB
                     | OSB sfstringValues CSB'''
def p_sfstringValues(p):
    '''sfstringValues : sfstringValue
                      | sfstringValue sfstringValues
                      | empty'''
def p_mfvec2fValue(p):
    '''mfvec2fValue : sfvec2fValue
                    | OSB CSB
                    | OSB sfvec2fValues CSB'''
def p_sfvec2fValues(p):
    '''sfvec2fValues : sfvec2fValue
                     | sfvec2fValue sfvec2fValues
                     | empty'''
def p_mfvec3fValue(p):
    '''mfvec3fValue : sfvec3fValue
                    | OSB CSB
                    | OSB sfvec3fValues CSB'''
def p_sfvec3fValues(p):
    '''sfvec3fValues : sfvec3fValue
                     | sfvec3fValue sfvec3fValues
                     | empty'''

def parse(data, backend):
    parser = yacc.yacc()
