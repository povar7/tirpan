'''
Created on 16.09.2012

@author: bronikkk
'''

import unittest
from tests_common import *
from utils import findNode
from typegraph import VarTypeGraphNode
test_file_name = get_test_file_name('func15.py')

import ast

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)

    def test_walk_var_a(self):
        node = findNode(self.ast, line=7, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_float
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([type1 == elem for elem in nodeType]),                   \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

if __name__ == '__main__':
    unittest.main()
