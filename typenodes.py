'''
Created on 03.03.2012

@author: ramil
'''

from types import NoneType

class TypeNode(object):
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

    def has_type(self, some_type):
        return self._type == some_type

class TypeAtom(TypeNode):
    pass

class TypeType(TypeAtom):
    def __init__(self):
        self._type = type 

class TypeNumOrBool(TypeAtom):
    pass

class TypeNum(TypeNumOrBool):
    pass
    
class TypeInt(TypeNum):
    def __init__(self):
        self._type = int

class TypeLong(TypeNum):
    def __init__(self):
        self._type = long

class TypeFloat(TypeNum):
    def __init__(self):
        self._type = float

class TypeComplex(TypeNum):
    def __init__(self):
        self._type = complex

class TypeBaseString(TypeAtom):
    pass

class TypeStr(TypeBaseString):
    def __init__(self):
        self._type = str

class TypeUnicode(TypeBaseString):
    def __init__(self):
        self._type = unicode

class TypeBool(TypeNumOrBool):
    def __init__(self):
        self._type = bool

class TypeNone(TypeAtom):
    def __init__(self):
        self._type = NoneType

class TypeStandard(TypeNode):
    pass

class TypeListOrTuple(TypeStandard):
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
    def __init__(self):
        super(TypeList, self).__init__()
        self._type = list

class TypeTuple(TypeListOrTuple):
    def __init__(self):
        super(TypeTuple, self).__init__()
        self._type = tuple

class TypeDict(TypeStandard):
    def __init__(self):
        self.keys  = set([])
        self.vals  = set([])
        self._type = dict

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

class TypeUnknown(TypeNode):
    def __init__(self):
        self.keys  = set([])
        self.vals  = set([])
        self._type = None

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
        return 'unknown'
