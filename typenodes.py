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

class TypeInt(TypeNode):
    def __str__(self):
        return 'int'

class TypeLong(TypeNode):
    def __str__(self):
        return 'long'

class TypeFloat(TypeNode):
    def __str__(self):
        return 'float'

class TypeComplex(TypeNode):
    def __str__(self):
        return 'complex'

class TypeStr(TypeNode):
    def __str__(self):
        return 'str'

class TypeUnicode(TypeNode):
    def __str__(self):
        return 'unicode'

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