'''
Created on 03.03.2012

@author: bronikkk
'''

import os

from codegen   import to_source
from typenodes import *

asserts_directory = 'asserts_dir'

class AssertGenerator():
    def flush(self):
        self.tabs_level  = 0
        self.func_list   = []
        self.func_number = 0

    def __init__(self, file_handle = None):
        self.file_handle = file_handle
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
        res = ''
        for item in types_set:
            res += 'not ' + self.generate(item) + '(item) and '
        res += 'True'
        return res

    def generate_var_conds_list(self, var_name, func_names):
        res = ''
        for func_name in func_names:
            res += '%s(%s) or ' % (func_name, var_name)
        res += 'False'
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

    def generate_for_types(self, var):
        from typegraph import FuncDefTypeGraphNode, ModuleTypeGraphNode
        if any([isinstance(elem, (FuncDefTypeGraphNode, ModuleTypeGraphNode)) for elem in var.nodeType]):
            return
        func_names = []
        for var_type in var.nodeType:
            func_names.append(self.generate(var_type))
        conds = self.generate_var_conds_list(var.name, func_names)
        tabs_level      = self.tabs_level
        self.tabs_level = 0
        self.func_list.append('check_variable("%s", %s)' % (var.name, conds))
        self.tabs_level = tabs_level

    def print_code(self):
        first = True
        for item in self.func_list:
            if first:
                first = False
            else:
                self.file_handle.write('\n\n')
            self.file_handle.write(item)

def ensure_directory(filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

def transform_to_relative(filename):
    if filename.startswith('/'):
        filename = filename[1:]
    return filename

def generate_check_function(output_file):
    output_line =                                          \
                  'total  = 0\n'                         + \
                  'hits   = 0\n'                         + \
                  'misses = 0\n'                         + \
                  '\n'                                   + \
                  'def check_variable(name, cond):\n'    + \
                  '    global total, hits, misses\n'     + \
                  '    total += 1\n'                     + \
                  '    if cond:\n'                       + \
                  '        hits   += 1\n'                + \
                  '    else:\n'                          + \
                  '        print "Miss: %s" % name\n'    + \
                  '        misses += 1\n'                + \
                  '\n'

    output_file.write(output_line)

def generate_asserts(module):
    scope    = module.getScope()
    filename = os.path.join(asserts_directory, transform_to_relative(module.name))
    ensure_directory(filename)
    with open(filename, 'w') as output_file:
        assert_generator = AssertGenerator(output_file)
        output_file.write(to_source(module.ast))
        output_file.write('\n\n')
        generate_check_function(output_file)
        variables = sorted(scope.variables.values(), \
                           lambda x, y: cmp((x.line, x.col), (y.line, y.col)))
        for var in variables:
            assert_generator.generate_for_types(var)
        assert_generator.print_code()
        output_file.write('\n\n')
        output_file.write('print "Total: %d, hits: %d, misses: %d" % (total, hits, misses)\n')
