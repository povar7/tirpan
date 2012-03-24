'''
Created on 03.03.2012

@author: ramil
'''

class TypeNode:
    def instance_eq_to(self, other):
        return True

    def instance_hash(self):
       return None

    def elem_types(self):
        return set()

    def __ne__(self, other):
        return not (self == other)

    def __eq__(self, other):
        res = self.__class__ == other.__class__
        return res and self.instance_eq_to(other)

    def __hash__(self):
        return hash((self.__class__, self.instance_hash()))

class TypeAtom(TypeNode):
    pass

class TypeInt(TypeAtom):
    def __str__(self):
        return 'int'

class TypeLong(TypeAtom):
    def __str__(self):
        return 'long'

class TypeFloat(TypeAtom):
    def __str__(self):
        return 'float'

class TypeComplex(TypeAtom):
    def __str__(self):
        return 'complex'

class TypeCommonString(TypeAtom):
    pass

class TypeStr(TypeCommonString):
    def __str__(self):
        return 'str'

class TypeUnicode(TypeCommonString):
    def __str__(self):
        return 'unicode'

class TypeBool(TypeAtom):
    def __str__(self):
        return 'bool'

class TypeNone(TypeAtom):
    def __str__(self):
        return 'NoneType'

class TypeListOrTuple(TypeNode):
    def __init__(self):
        self.elems = set([])

    def add_elem(self, elem):
        self.elems.add(elem)

    def instance_eq_to(self, other):
        return self.elems == other.elems

    def instance_hash(self):
        return hash(tuple(self.elems))

    def elem_types(self):
        return self.elems

class TypeList(TypeListOrTuple):
    def __str__(self):
        return 'list'

class TypeTuple(TypeListOrTuple):
    def __str__(self):
        return 'tuple'

class TypeDict(TypeNode):
    def __init__(self):
        self.keys = set([])
        self.vals = set([])

    def add_val(self, val):
        self.vals.add(val)

    def add_key(self, key):
        self.keys.add(key)

    def instance_eq_to(self, other):
        return (self.keys == other.keys) and (self.vals == other.vals) 

    def instance_hash(self):
        return hash((tuple(self.keys), tuple(self.vals)))

    def elem_types(self):
        return self.vals

    def __str__(self):
        return 'dict'
