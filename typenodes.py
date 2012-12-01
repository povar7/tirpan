'''
Created on 03.03.2012

@author: ramil
'''

from copy  import copy as shallowcopy
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
    def __init__(self, value):
        self.value = value

    def instance_eq_to(self, other):
        return self.value == other.value

    def instance_hash(self):
        return hash(self.value)

class TypeStr(TypeBaseString):
    def __init__(self, value = None):
        super(TypeStr, self).__init__(value)
        self._type = str

class TypeUnicode(TypeBaseString):
    def __init__(self, value = None):
        super(TypeUnicode, self).__init__(value)
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
        self.elems = set()

    def instance_eq_to(self, other):
        return self.elem_types() == other.elem_types()

    def instance_hash(self):
        return hash(frozenset(self.elems))

    def __deepcopy__(self, memo):
        res = shallowcopy(self)
        res.elems = shallowcopy(self.elems)
        return res

class TypeList(TypeListOrTuple):
    def add_elem(self, elem):
        if isinstance(self.elems, list):
            self.elems = set(self.elems)
        self.elems.add(elem)

    def elem_types(self):
        return set(self.elems)

    def __init__(self):
        super(TypeList, self).__init__()
        self._type = list

    def instance_eq_to(self, other):
        if isinstance(self.elems, list) and isinstance(other.elems, list):
            return self.elems == other.elems
        elif isinstance(self.elems, list) or isinstance(other.elems, list):
            return False
        else:
            return self.elem_types() == other.elem_types()

    def instance_hash(self):
        if isinstance(self.elems, list):
            return hash(tuple(self.elems))
        else:
            return hash(frozenset(self.elems))

class TypeTuple(TypeListOrTuple):
    def add_elem(self, elem):
        if isinstance(self.elems, tuple):
            self.elems = set(self.elems)
        self.elems.add(elem)

    def elem_types(self):
        return set(self.elems)

    def __init__(self):
        super(TypeTuple, self).__init__()
        self._type = tuple

    def instance_eq_to(self, other):
        if isinstance(self.elems, tuple) and isinstance(other.elems, tuple):
            return self.elems == other.elems
        elif isinstance(self.elems, tuple) or isinstance(other.elems, tuple):
            return False
        else:
            return self.elem_types() == other.elem_types()

    def instance_hash(self):
        if isinstance(self.elems, tuple):
            return hash(self.elems)
        else:
            return hash(frozenset(self.elems))

class TypeDict(TypeStandard):
    def __init__(self):
        self.keys  = set()
        self.vals  = set()
        self._dict = None
        self._type = dict

    def add_val(self, val):
        self.vals.add(val)

    def add_key(self, key):
        self.keys.add(key)

    def add_elem(self, elem):
        self.add_val(elem)

    def add_pair(self, pair):
        key, val = pair
        if self._dict is None:
            self._dict = {}
        self._dict[key] = val
        self.add_val(val)

    def instance_eq_to(self, other):
        return (self.keys == other.keys) and (self.vals == other.vals) 

    def instance_hash(self):
        return hash((tuple(self.keys), tuple(self.vals)))

    def elem_types(self):
        return self.keys

    def keys_types(self):
        return self.keys

    def vals_types(self):
        return self.vals

    def __deepcopy__(self, memo):
        res = shallowcopy(self)
        res.keys = shallowcopy(self.keys)
        res.vals = shallowcopy(self.vals)
        return res

class TypeUnknown(TypeNode):
    def __init__(self):
        self.keys  = set()
        self.vals  = set()
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

    def __deepcopy__(self, memo):
        return self

def get_new_string(value):
    if isinstance(value, str):
        return TypeStr(value)
    elif isinstance(value, unicode):
        return TypeUnicode(value)
    else:
        return TypeUnknown()
