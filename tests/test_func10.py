'''
Created on 25.03.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('func10.py')

import ast

from typegraph    import *
from utils        import findNode

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)

    def test_walk_var_foo(self):
        node = findNode(self.ast, line=1, kind=ast.FunctionDef)
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

    def test_walk_var_x(self):
        node = findNode(self.ast, line=4, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = TypeDict()
        type1.add_key(get_new_string('foo'))
        type1.add_key(get_new_string('bar'))
        type1.add_val(self.type_int)
        type1.add_val(self.type_float)
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
        type1 = TypeDict()
        type1.add_key(get_new_string('mama'))
        type1.add_key(get_new_string('papa'))
        type1.add_val(self.type_int)
        type1.add_val(self.type_float)
        self.assertTrue(len(nodeType) == 1 and                                             \
                        any([type1 == elem for elem in nodeType]),                         \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

if __name__ == '__main__':
    unittest.main()
