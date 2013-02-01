'''
Created on 07.01.2013

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('misc18.py')

import ast
from typegraph    import *
from utils        import findNode

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)

    def test_walk_var_a(self):
        node = findNode(self.ast, line=1, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = TypeInt()
        type2 = TypeFloat()
        self.assertTrue(len(nodeType) == 2 and                                       \
                        any([type1 == elem for elem in nodeType]) and                \
                        any([type2 == elem for elem in nodeType]),                   \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

if __name__ == '__main__':
    unittest.main()