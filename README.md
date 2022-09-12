# WIP: wrl-parser

Python library to parse VRML files (.wrl) using an LALR parser with a Context-Free Grammar.

# Context-Free Grammar

This parser is based on the grammar provided by the [VRML97 specification](https://tecfa.unige.ch/guides/vrml/vrml97/spec/part1/grammar.html). The grammar described in the specification is a Context-Sensitive Grammar which isn't deterministic. The following changes have been made to make it a Context-Free Grammar.

- Recursive rules have been generalized to allow collections to be empty as this will resolve shift/reduce conflicts. This should only broaden the spectrum of parsable files.
```
elements : element                  elements : element elements
         | element elements    ->            | empty      
         | empty                     
```

- IDs have been optimized to the raw ID type

- Field values have been optimized to the raw type
```
sffloatValue :
sfcolorValue :
sfvec2fValue :  ->  sffloatValues : FLOAT sffloatValues
sfvec3fValue :                    | empty
...
```

# Intermediate Representation (IR)

The Intermediate Representation is defined with a couple of classes :
- `Node` which has a number of fields.
- `DefinedNode` which has a name and a `Node`.
- `UsedNode` which references a node by a name attribute.
- `Field` which defines a particular field in a `Node`.

Finally, instances of these classes are grouped within a `Scene` class which contains the representation of the file.

# Tests
