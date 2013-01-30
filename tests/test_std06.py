'''
Created on 03.11.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('std06.py')

import ast

from typegraph    import *
from utils        import findNode


class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)

    def test_walk_var_a(self):
        node = findNode(self.ast, line=5, col=6, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_int
        type2 = self.type_float
        self.assertTrue(len(nodeType) == 2 and                                              \
                        any([type1 == elem for elem in nodeType]) and                       \
                        any([type2 == elem for elem in nodeType]),                          \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_walk_var_b(self):
        node = findNode(self.ast, line=5, col=9, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_str
        type2 = self.type_unicode
        self.assertTrue(len(nodeType) == 2 and                                              \
                        any([type1 == elem for elem in nodeType]) and                       \
                        any([type2 == elem for elem in nodeType]),                          \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

if __name__ == '__main__':
    unittest.main()
