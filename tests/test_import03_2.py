'''
Created on 26.08.2012

@author: bronikkk
'''

import unittest
from tests_common import *

test_file_name_1 = get_test_file_name('import03_2.py')
test_file_name_2 = get_test_file_name('import03/__init__.py')

import ast

from init         import common_init
from errorprinter import ErrorPrinter
from scope        import Scope
from tiimporter   import Importer, QuasiAlias
from tiparser     import TIParser
from typegraph    import *
from utils        import findNode

import tirpan

def import_files(mainfile, aliases):
    global importer
    importer.import_files(mainfile, aliases)

def import_from_file(mainfile, module, aliases):
    global importer
    alias = QuasiAlias(module)
    importer.import_files(mainfile, [alias], aliases)

class TestTirpan(unittest.TestCase):
    def setUp(self):
        global global_scope, current_scope, current_res, error_printer, importer, verbose, test_results, test_precision, print_imports, types_number
        global_scope   = Scope(None)
        current_scope  = global_scope
        current_res    = None
        error_printer  = ErrorPrinter()
        importer       = Importer()
        verbose        = False
        test_results   = False
        test_precision = False
        print_imports  = False
        types_number   = 10

        common_init(global_scope, importer)
        tirpan.run(test_file_name_1)
        self.nodes      = (importer.imported_files['__main__'].ast,                         \
                           importer.imported_files[os.path.abspath(test_file_name_2)].ast)
        
        self.type_int     = TypeInt()
        self.type_float   = TypeFloat()
        self.type_bool    = TypeBool()
        self.type_complex = TypeComplex()

    def test_different_modules(self):
        self.assertTrue(isinstance(self.nodes[0], ast.Module), 'module 1 is not a module')
        self.assertTrue(isinstance(self.nodes[1], ast.Module), 'module 2 is not a module')
        self.assertTrue(self.nodes[0] != self.nodes[1], 'modules are the same')

    def test_basic_module_1(self):
        module = self.nodes[0].link
        self.assertTrue(isinstance(module, ModuleTypeGraphNode), 'module 1 has no link to type info')
        self.assertEquals(module.name, os.path.abspath(test_file_name_1), 'module 1 has a wrong name')
        self.assertEquals(module.ast, self.nodes[0], 'module 1 has a wrong link to ast')

    def test_basic_module_2(self):
        module = self.nodes[1].link
        self.assertTrue(isinstance(module, ModuleTypeGraphNode), 'module 2 has no link to type info')
        self.assertEquals(module.name, os.path.abspath(test_file_name_2), 'module 2 has a wrong name')
        self.assertEquals(module.ast, self.nodes[1], 'module 2 has a wrong link to ast')

    def test_walk_var_x(self):
        node = findNode(self.nodes[0], line=3, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_int
        self.assertTrue(len(nodeType) == 1 and                                              \
                        any([type1 == elem for elem in nodeType]),                          \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_walk_var_z(self):
        node = findNode(self.nodes[0], line=5, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_bool
        self.assertTrue(len(nodeType) == 1 and                                              \
                        any([type1 == elem for elem in nodeType]),                          \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

    def test_walk_var_a(self):
        node = findNode(self.nodes[1], line=1, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_complex
        self.assertTrue(len(nodeType) == 1 and                                              \
                        any([type1 == elem for elem in nodeType]),                          \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

if __name__ == '__main__':
    unittest.main()
