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

    def __repr__(self):
        return '?'

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
    def __init__(self, value = None):
        self._type = int
        self.value = value

    def instance_eq_to(self, other):
        return self.value == other.value

    def instance_hash(self):
        return hash(self.value)

    def __repr__(self):
        if self.value:
            return str(self.value)
        else:
            return '<int value>'

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

    def __repr__(self):
        if self.value:
            return '\'' + str(self.value) + '\''
        else:
            return '<str value>'

class TypeUnicode(TypeBaseString):
    def __init__(self, value = None):
        super(TypeUnicode, self).__init__(value)
        self._type = unicode

    def __repr__(self):
        if self.value:
            return '\'' + str(self.value) + '\''
        else:
            return '<unicode value>'

class TypeBool(TypeNumOrBool):
    def __init__(self):
        self._type = bool

    def __repr__(self):
        return '<bool value>'

class TypeNone(TypeAtom):
    def __init__(self):
        self._type = NoneType

    def __repr__(self):
        return 'None'

class TypeStandard(TypeNode):
    pass

class TypeListOrTuple(TypeStandard):
    def __init__(self):
        self.elems  = set()
        self.unique = False

    def instance_eq_to(self, other):
        return self.elem_types() == other.elem_types()

    def instance_hash(self):
        return hash(frozenset(self.elems))

    def __deepcopy__(self, memo):
        if self.unique:
            return self
        else:
            res = shallowcopy(self)
            res.elems = shallowcopy(self.elems)
            return res

    def __repr__(self):
        res = ''
        if isinstance(self, TypeList):
            res += '['
        elif isinstance(self, TypeTuple):
            res += '('
        first = True
        for elem in self.elems:
            if not first:
                res += ', '
            else:
                first = False
            res += str(elem)
        if isinstance(self, TypeList):
            res += ']'
        elif isinstance(self, TypeTuple):
            res += ')'
        return res

class TypeList(TypeListOrTuple):
    def add_elem(self, elem):
        if isinstance(self.elems, list):
            self.elems = set(self.elems)
        self.elems.add(elem)

    def elem_types(self):
        return set(self.elems)

    def __init__(self, unique = False):
        super(TypeList, self).__init__()
        self._type  = list
        self.unique = unique

    def instance_eq_to(self, other):
        if self.unique or other.unique:
            return self is other 
        elif isinstance(self.elems, list) and isinstance(other.elems, list):
            return self.elems == other.elems
        elif isinstance(self.elems, list) or isinstance(other.elems, list):
            return False
        else:
            return self.elem_types() == other.elem_types()

    def instance_hash(self):
        if self.unique:
            return hash(id(self))
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
        return hash((frozenset(self.keys), frozenset(self.vals)))

    def elem_types(self):
        return self.keys

    def keys_types(self):
        return self.keys

    def vals_types(self):
        return self.vals

    def __deepcopy__(self, memo):
        res = shallowcopy(self)
        res.keys  = shallowcopy(self.keys)
        res.vals  = shallowcopy(self.vals)
        res._dict = shallowcopy(self._dict)
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

    def __deepcopy__(self, memo):
        return self

def get_new_string(value):
    if isinstance(value, str):
        return TypeStr(value)
    elif isinstance(value, unicode):
        return TypeUnicode(value)
    else:
        return TypeUnknown()

type_unknown = TypeUnknown()

def get_unknown():
    return type_unknown

bool_type = TypeBool()