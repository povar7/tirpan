class TypeDescrNode(object):
    pass

class TypeInt(TypeDescrNode):
    def __str__(self):
        return 'int'
    pass

class TypeLong(TypeDescrNode):
    def __str__(self):
        return 'long'
    pass

class TypeFloat(TypeDescrNode):
    def __str__(self):
        return 'float'
    pass

class TypeComplex(TypeDescrNode):
    def __str__(self):
        return 'complex'
    pass

class TypeStr(TypeDescrNode):
    def __str__(self):
        return 'str'
    pass

class TypeUnicode(TypeDescrNode):
    def __str__(self):
        return 'unicode'
    pass

class TypeList(TypeDescrNode):
    def __init__(self):
        self.elems = set()
    def __str__(self):
        return 'list'
    def add_elem(self, type_node):
        self.elems = self.elems.union(set([type_node]))

class TypeTuple(TypeDescrNode):
    def __init__(self):
        self.elems = set()
    def __str__(self):
        return 'tuple'
    def add_elem(self, type_node):
        self.elems = self.elems.union(set([type_node]))

class TypeDict(TypeDescrNode):
    def __init__(self):
        self.keys = set()
        self.vals = set()
    def __str__(self):
        return 'dict'
    def add_key(self, type_node):
        self.keys = self.keys.union(set([type_node]))
    def add_val(self, type_node):
        self.vals = self.vals.union(set([type_node]))

class AssertGenerator():
    def flush(self):
        self.tabs_level  = 0
        self.func_list   = []
        self.func_number = 0

    def __init__(self):
        self.tabs_number = 4
        self.flush()

    def inc_func_number(self):
        self.func_number += 1

    def inc_tabs_level(self):
        self.tabs_level += 1

    def dec_tabs_level(self):
        self.tabs_level -= 1

    def add_line(self, line):
        add = '\n' + ' ' * (self.tabs_level * self.tabs_number) + line
        self.func_list[self.func_number] += add

    def generate_footer(self):
        self.dec_tabs_level()

    def generate_if_header(self, test):
        self.add_line('if ' + test + ':')
        self.inc_tabs_level()
    
    def generate_if(self, test, stmt):
        self.generate_if_header(test)
        self.add_line(stmt)
        self.generate_footer()

    def generate_for_header(self, collect):
        self.add_line('for item in %s:' % collect)
        self.inc_tabs_level()

    def generate_type_assert(self, type_node):
        cond = 'not isinstance(elem, %s)' % type_node
        self.generate_if(cond, 'return False')

    def generate_conds_list(self, types_set):
        types_list = list(types_set)
        res = ''
        for item in types_list:
            res += 'not ' + self.generate(item) + '(item) and '
        res += 'True'
        return res

    def generate_iteration(self, collection, name):
        self.generate_for_header(name)
        func_number = self.func_number
        conds = self.generate_conds_list(collection)
        self.func_number = func_number
        self.generate_if(conds, 'return False')
        self.generate_footer()

    def generate(self, type_node):
        tabs_level = self.tabs_level
        self.tabs_level = 0
        self.func_number = len(self.func_list)
        func_name = 'assert_%06d' % self.func_number
        code = 'def %s(elem):' % func_name
        self.func_list.append(code)
        self.inc_tabs_level() 
        self.generate_type_assert(type_node)
        if isinstance(type_node, (TypeList, TypeTuple)):
            self.generate_iteration(type_node.elems, 'elem')
        elif isinstance(type_node, TypeDict):
            self.generate_iteration(type_node.keys, 'elem.keys()')
            self.generate_iteration(type_node.vals, 'elem.values()')
        self.add_line('return True')
        self.tabs_level = tabs_level
        return func_name

    def print_code(self):
        first = True
        for item in assert_generator.func_list:
            if first:
                first = False
            else:
                print
            print item

assert_generator = AssertGenerator()

type_int      = TypeInt()
type_long     = TypeLong()
type_float    = TypeFloat()

type_complex  = TypeComplex()

type_str      = TypeStr()
type_unicode  = TypeUnicode()

def test_001():
    type001 = TypeList()
    type001.add_elem(type_int)
    type001.add_elem(type_long)
    type001.add_elem(type_float)
    assert_generator.generate(type001)

def test_002():
    type002 = TypeTuple()
    type002.add_elem(type_complex)
    assert_generator.generate(type002)

def test_003():
    type003 = TypeDict()
    type003.add_key(type_str)
    type003.add_val(type_unicode)
    assert_generator.generate(type003)

test_001()
test_002()
test_003()
assert_generator.print_code()
