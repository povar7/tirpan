'''
Created on 18.11.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('assign03.py')

import ast

from typegraph    import *
from utils        import findNode

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)

    def test_walk_var_el(self):
        node = findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 2 and                                       \
                        any([self.type_int   == elem for elem in nodeType]) and      \
                        any([self.type_str   == elem for elem in nodeType]),         \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'el', 'name is not "el"')

if __name__ == '__main__':
    unittest.main()
