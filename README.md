# wrlparser

Python library to parse VRML files (.wrl) using an LALR parser with a Context-Free Grammar.

# Getting started

## Installing

```python
pip install wrlparser
```

## Sample program

This program parses the file which name has been given as a command line argument. Two sample models have been provided in the `tests/models` folder.

```python
from wrlparser import parse
import sys

file = sys.argv[1]
with open(file) as f:
    l = "".join(f.readlines())
    f.close()

scene = parse(l)
```

# Documentation

## Context-Free Grammar

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

## Intermediate Representation (IR)

Once parsed, the file's content is returned to the user as classes. Their structure strictly corresponds to the one described in the specification.

For instance, a `material` node has the following fields :
```
  - ambientIntensity : float
  - diffuseColor     : list[3]
  - specularColor    : list[3]
  - emissiveColor    : list[3]
  - transparency     : float
  - shininess        : float
```

It should be noted that the specification doesn't require a file to specify every field of a node. They should therefore be check before accessed as follows:
```python
m = Material()
if m.ambientIntensity != None:
  # Use the value
```

# Tests

This parser has been tester with models from the KiCad catalog.

# Issues

Even though the parser fully supports VRML's grammar, a very small subset of the intermediate representation has been implemented. This is due to the lack of test models for specific node types.

If you every need to parse a file which has an unimplemented feature, feel free to share the file in a ticket so that I can support it.
