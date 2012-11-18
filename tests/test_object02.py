'''
Created on 08.07.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('object02.py')

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

    def test_walk_var_a(self):
        node = findNode(self.ast, line=7, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 2 and                                                    \
                        all([isinstance(elem, ClassInstanceTypeGraphNode) for elem in nodeType]), \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_walk_var_a_x(self):
        node = findNode(self.ast, line=9, kind=ast.Attribute)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        nodeType = node.link.nodeType
        type1 = self.type_int
        type2 = self.type_float
        self.assertTrue(len(nodeType) == 2 and                                                    \
                        any([type1 == elem for elem in nodeType]) and                             \
                        any([type2 == elem for elem in nodeType]),                                \
                        'wrong types calculated')

    def test_walk_var_b(self):
        node = findNode(self.ast, line=9, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_int
        type2 = self.type_float
        self.assertTrue(len(nodeType) == 2 and                                                    \
                        any([type1 == elem for elem in nodeType]) and                             \
                        any([type2 == elem for elem in nodeType]),                                \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

if __name__ == '__main__':
    unittest.main()
