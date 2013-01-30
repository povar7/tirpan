'''
Created on 07.10.2012

@author: bronikkk
'''

import unittest
from tests_common import *

test_file_name_1 = get_test_file_name('import07_1.py')
test_file_name_2 = get_test_file_name('import07_3.py')

import ast

from typegraph    import *
from utils        import findNode

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name_1)
        self.nodes     = (config.importer.imported_files['__main__'].ast,                          \
                          config.importer.imported_files[test_file_name_2].ast)

    def test_walk_var_a(self):
        node = findNode(self.nodes[1], line=1, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_int
        self.assertTrue(len(nodeType) == 1 and                                              \
                        any([type1 == elem for elem in nodeType]),                          \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

if __name__ == '__main__':
    unittest.main()
