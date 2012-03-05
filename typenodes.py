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
		return hash( (self.__class__, self.instance_hash()) )


class TypeInt(TypeNode):
	pass;

class TypeFloat(TypeNode):
	pass; 

class TypeStr(TypeNode):
	pass;

class TypeUnicode(TypeNode):
	pass;

class TypeBool(TypeNode):
	pass;

class TypeList(TypeNode):
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

class TypeTuple(TypeList):
	pass;

class TypeDict(TypeNode):
	def __init__(self):
		self.elems = set([])
		self.keys = set([])

	def add_elem(self, elem):
		self.elems.add(elem)

	def add_key(self, key):
		self.keys.add(key)

	def instance_eq_to(self, other):
		return (self.elems == other.elems) and (self.keys == other.keys)

	def instance_hash(self):
		return hash((tuple(self.elems), tuple(self.keys)))

	def elem_types(self):
		return self.elems


		