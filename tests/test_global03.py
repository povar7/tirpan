'''
Created on 15.04.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('global03.py')

import ast

from init       import common_init
from scope      import Scope
from tiimporter import Importer, QuasiAlias
from tiparser   import TIParser
from typegraph  import *
from typenodes  import *
from utils      import findNode

import tirpan

class TestTirpan(unittest.TestCase):
    def setUp(self):
        global global_scope, current_scope, current_res, importer, verbose
        global_scope  = Scope(None)
        current_scope = global_scope
        current_res   = None
        importer      = Importer()
        verbose       = False

        common_init(global_scope, importer)
        tirpan.run(test_file_name)
        self.ast = importer.imported_files['__main__'].ast

        self.type_bool    = TypeBool()
        self.type_int     = TypeInt()
        self.type_str     = TypeStr()

    def test_walk_var_foo(self):
        node = findNode(self.ast, line=4, kind=ast.FunctionDef)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 1 and                                              \
                        any([isinstance(elem, FuncDefTypeGraphNode) for elem in nodeType]), \
                        'type is a function definition')
        funcDef  = list(nodeType)[0]
        self.assertEqual(len(funcDef.templates.keys()), 1,
                         'there must be 1 template') 
        self.assertEqual(node.link.name, 'foo', 'name is not "foo"')

    def test_walk_var_res1(self):
        node = findNode(self.ast, line=1, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_bool
        type2 = self.type_int
        type3 = self.type_str
        self.assertTrue(len(nodeType) == 3 and                                             \
                        any([type1 == elem for elem in nodeType]) and                      \
                        any([type2 == elem for elem in nodeType]) and                      \
                        any([type3 == elem for elem in nodeType]),                         \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'res1', 'name is not "res1"')

    def test_walk_var_res2(self):
        node = findNode(self.ast, line=2, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_int
        self.assertTrue(len(nodeType) == 1 and                                             \
                        any([type1 == elem for elem in nodeType]),                         \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'res2', 'name is not "res2"')

if __name__ == '__main__':
    unittest.main()