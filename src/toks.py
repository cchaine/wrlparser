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

reserved = {
    'DEF'          : 'DEF',
    'USE'          : 'USE',
    'PROTO'        : 'PROTO',
    'eventIn'      : 'EVENTIN',
    'eventOut'     : 'EVENTOUT',
    'field'        : 'FIELD',
    'exposedField' : 'EXPOSEDFIELD',
    'EXTERNPROTO'  : 'EXTERNPROTO',
    'ROUTE'        : 'ROUTE',
    'TO'           : 'TO',
    'Script'       : 'SCRIPT',
    'IS'           : 'IS',
    'MFColor'      : 'MFCOLOR',
    'MFFloat'      : 'MFFLOAT',
    'MFInt32'      : 'MFINT32',
    'MFNode'       : 'MFNODE',
    'MFRotation'   : 'MFROTATION',
    'MFString'     : 'MFSTRING',
    'MFTime'       : 'MFTIME',
    'MFVec2f'      : 'MFVEC2F',
    'MFVec3f'      : 'MFVEC3F',
    'SFBool'       : 'SFBOOL',
    'SFColor'      : 'SFCOLOR',
    'SFFloat'      : 'SFFLOAT',
    'SFImage'      : 'SFIMAGE',
    'SFInt32'      : 'SFINT32',
    'SFNode'       : 'SFNODE',
    'SFRotation'   : 'SFROTATION',
    'SFString'     : 'SFSTRING',
    'SFTime'       : 'SFTIME',
    'SFVec2f'      : 'SFVEC2F',
    'SFVec3f'      : 'SFVEC3F',
    'TRUE'         : 'TRUE',
    'FALSE'        : 'FALSE'
}

tokens = [
    'NULL',
    'OSB', # Open Square Bracket
    'CSB', # Close Square Bracket
    'OCB', # Open Curly Bracket
    'CCB', # Close Curly Bracket
    'DOT',
    'FLOAT',
    'INT32',
    'ID',
    'STRING'
] + list(reserved.values())

t_NULL          =  r'NULL'
t_OSB           =  r'\['
t_CSB           =  r'\]'
t_OCB           =  r'{'
t_CCB           =  r'}'
t_FLOAT = r'([+/-]?((([0-9]*\.[0-9]+)|([0-9]+(\.)?))([eE][+\-]?[0-9]+)?))'
t_INT32 = r'([+\-]?(([0-9]+)|(0[xX][0-9a-fA-F]+)))'
t_STRING = r'\".*\"'
t_DOT = r'\.'

def t_ID(t):
    r'[^\u0030-\u0039\u0000-\u0020\u0022\u0023\u0027\u002b\u002c\u002d\u002e\u005b\u005c\u005d\u007b\u007d\u007f][^\u0000-\u0020\u0022\u0023\u0027\u002c\u002e\u005b\u005c\u005d\u007b\u007d\u007f]*'
    t.type = reserved.get(t.value,'ID')
    return t

t_ignore_COMMENT = r'\#[^\n]*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignore CR, LF, Space, Tab, Comma
t_ignore = '\u000d\u000a\u0020\u0009\u002c'

def t_error(t):
    print("Illegal character '{}' at line {}".format(t.value[0], t.lexer.lineno))
    t.lexer.skip(1)
