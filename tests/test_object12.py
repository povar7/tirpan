'''
Created on 24.11.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('object12.py')

import ast

from init         import common_init
from errorprinter import ErrorPrinter
from scope        import Scope
from tiimporter   import Importer, QuasiAlias
from tiparser     import TIParser
from typegraph    import *
from typenodes    import *
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
        tirpan.run(test_file_name)
        self.ast = importer.imported_files['__main__'].ast

        self.type_int     = TypeInt()
        self.type_float   = TypeFloat()

    def test_walk_var_a1(self):
        node = findNode(self.ast, line=10, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 1 and                                                    \
                        all([isinstance(elem, ClassInstanceTypeGraphNode) for elem in nodeType]), \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a1', 'name is not "a1"')

    def test_walk_var_x(self):
        node = findNode(self.ast, line=11, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_int
        self.assertTrue(len(nodeType) == 1 and                                                    \
                        any([type1 == elem for elem in nodeType]),                                \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_walk_var_a2(self):
        node = findNode(self.ast, line=12, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 1 and                                                    \
                        all([isinstance(elem, ClassInstanceTypeGraphNode) for elem in nodeType]), \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a2', 'name is not "a2"')

    def test_walk_var_y(self):
        node = findNode(self.ast, line=13, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_float
        self.assertTrue(len(nodeType) == 1 and                                                    \
                        any([type1 == elem for elem in nodeType]),                                \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

if __name__ == '__main__':
    unittest.main()
