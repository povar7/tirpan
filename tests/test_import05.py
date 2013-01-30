'''
Created on 02.09.2012

@author: bronikkk
'''

import unittest
from tests_common import *

test_file_name_1 = get_test_file_name('import05_1.py')
test_file_name_2 = get_test_file_name('import05_2.py')

import ast

from typegraph    import *
from utils        import findNode

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name_1)
        self.nodes      = (config.importer.imported_files['__main__'].ast,                         \
                           config.importer.imported_files[test_file_name_2].ast)

    def test_walk_var_x(self):
        node = findNode(self.nodes[0], line=14, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_bool
        type2 = self.type_float
        type3 = self.type_int
        type4 = self.type_none
        self.assertTrue(len(nodeType) == 4 and                                              \
                        any([type1 == elem for elem in nodeType]) and                       \
                        any([type2 == elem for elem in nodeType]) and                       \
                        any([type3 == elem for elem in nodeType]) and                       \
                        any([type4 == elem for elem in nodeType]),                          \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_walk_var_data(self):
        node = findNode(self.nodes[1], line=1, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_bool
        type2 = self.type_int
        self.assertTrue(len(nodeType) == 2 and                                              \
                        any([type1 == elem for elem in nodeType]) and                       \
                        any([type2 == elem for elem in nodeType]),                          \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'data', 'name is not "data"')

if __name__ == '__main__':
    unittest.main()
