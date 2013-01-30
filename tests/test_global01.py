'''
Created on 15.04.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('global01.py')

import ast

from typegraph    import *
from utils        import findNode

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)

    def test_walk_var_foo(self):
        node = findNode(self.ast, line=3, kind=ast.FunctionDef)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 1 and                                              \
                        any([isinstance(elem, FuncDefTypeGraphNode) for elem in nodeType]), \
                        'type is a function definition')
        funcDef  = list(nodeType)[0]
        self.assertEqual(len(funcDef.templates.keys()), 2,
                         'there must be 2 templates') 
        self.assertEqual(node.link.name, 'foo', 'name is not "foo"')

    def test_walk_var_res(self):
        node = findNode(self.ast, line=1, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_int
        type2 = self.type_float
        type3 = self.type_none
        self.assertTrue(len(nodeType) == 3 and                                             \
                        any([type1 == elem for elem in nodeType]) and                      \
                        any([type2 == elem for elem in nodeType]) and                      \
                        any([type3 == elem for elem in nodeType]),                         \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'res', 'name is not "res"')

if __name__ == '__main__':
    unittest.main()
