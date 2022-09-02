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

tokens = (
#    'NULL',
    'OSB', # Open Square Bracket
    'CSB', # Close Square Bracket
    'OCB', # Open Curly Bracket
    'CCB', # Close Curly Bracket
    'DEF',
    'USE',
    'PROTO',
    'EVENTIN',
    'EVENTOUT',
    'FIELD',
    'EXPOSEDFIELD',
    'EXTERNPROTO',
    'ROUTE',
    'TO',
    'SCRIPT',
    'IS',
    'MFCOLOR',
    'MFFLOAT',
    'MFINT32',
    'MFNODE',
    'MFROTATION',
    'MFSTRING',
    'MFVEC2F',
    'MFVEC3F',
    'SFBOOL',
    'SFCOLOR',
    'SFFLOAT',
    'SFIMAGE',
    'SFINT32',
    'SFNODE',
    'SFROTATION',
    'SFSTRING',
    'SFTIME',
    'SFVEC2F',
    'SFVEC3F',
    'TRUE',
    'FALSE',
    'IDFIRSTCHAR',
    'IDRESTCHARS',
    'DOT',
    'COMMA',
    'FLOAT',
#    'SFINT32VALUE',
#    'SFFLOATVALUE',
#    'SFSTRINGVALUE',
#    'SFTIMEVALUE',
    "COMMENT"
)

t_OSB           =  r'\['
t_CSB           =  r'\]'
t_OCB           =  r'{'
t_CCB           =  r'}'
t_DEF           =  r'DEF'
t_USE           =  r'USE'
t_PROTO         =  r'PROTO'
t_EVENTIN       =  r'eventIn'
t_EVENTOUT      =  r'eventOut'
t_FIELD         =  r'field'
t_EXPOSEDFIELD  =  r'exposedField'
t_EXTERNPROTO   =  r'EXTERNPROTO'
t_ROUTE         =  r'ROUTE'
t_TO            =  r'TO'
t_SCRIPT        =  r'Script'
t_IS            =  r'IS'
t_MFCOLOR       =  r'MFColor'
t_MFFLOAT       =  r'MFFloat'
t_MFINT32       =  r'MFInt32'
t_MFNODE        =  r'MFNode'
t_MFROTATION    =  r'MFRotation'
t_MFSTRING      =  r'MFString'
t_MFVEC2F       =  r'MFVec2f'
t_MFVEC3F       =  r'MFVec3f'
t_SFBOOL        =  r'SFBool'
t_SFCOLOR       =  r'SFColor'
t_SFFLOAT       =  r'SFFloat'
t_SFIMAGE       =  r'SFImage'
t_SFINT32       =  r'SFInt32'
t_SFNODE        =  r'SFNode'
t_SFROTATION    =  r'SFRotation'
t_SFSTRING      =  r'SFString'
t_SFTIME        =  r'SFTime'
t_SFVEC2F       =  r'SFVec2f'
t_SFVEC3F       =  r'SFVec3f'
t_TRUE          =  r'TRUE'
t_FALSE         =  r'FALSE'
t_FLOAT = r'([+/-]?((([0-9]+(\.)?)|([0-9]*\.[0-9]+))([eE][+\-]?[0-9]+)?))'
t_DOUBLE = r'([+/-]?((([0-9]+(\.)?)|([0-9]*\.[0-9]+))([eE][+\-]?[0-9]+)?))'
t_INT32 = r'([+\-]?(([0-9]+)|(0[xX][0-9a-fA-F]+)))'
t_IDFIRSTCHAR = r'[^\u0030-\u0039\u0000-\u0020\u0022\u0023\u0027\u002c\u002e\u005b\u005c\u005d\u007b\u007d]'
t_IDRESTCHARS = r'[^\u0000-\u0020\u0022\u0023\u0027\u002c\u002e\u005b\u005c\u005d\u007b\u007d]+'
t_STRING = r'\".*\"'
t_DOT = r'\.'
t_COMMA = r','
t_ignore_COMMENT = r'\#[^\n]*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '{}' at line {}".format(t.value[0], t.lexer.lineno))
    t.lexer.skip(1)
