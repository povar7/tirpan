'''
Created on 25.03.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('builtin01.py')

import ast

from importer  import Importer
from init      import common_init
from scope     import Scope
from tiparser  import TIParser
from typegraph import *
from typenodes import *

from utils     import findNode

import tirpan

class TestTirpan(unittest.TestCase):
    def setUp(self):
        global global_scope, current_scope, current_res, importer, verbose
        global_scope  = Scope(None)
        current_scope = global_scope
        current_res   = None
        importer      = Importer()
        verbose       = False
        common_init(global_scope)
        tirpan.run(test_file_name)
        import __main__
        self.ast = __main__.importer.imported_files['__main__'].ast

        self.type_int     = TypeInt()
        self.type_float   = TypeFloat()

    def test_walk_var_x(self):
        node = findNode(self.ast, line=4, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_int
        self.assertTrue(len(nodeType) == 1 and                                             \
                        any([type1 == elem for elem in nodeType]),                         \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_walk_var_y(self):
        node = findNode(self.ast, line=5, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_int
        self.assertTrue(len(nodeType) == 1 and                                             \
                        any([type1 == elem for elem in nodeType]),                         \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_walk_var_z(self):
        node = findNode(self.ast, line=6, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_int
        self.assertTrue(len(nodeType) == 1 and                                             \
                        any([type1 == elem for elem in nodeType]),                         \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

if __name__ == '__main__':
    unittest.main()
