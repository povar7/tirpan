'''
Created on 09.12.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('builtin12.py')

import ast
import const

from typegraph    import *
from utils        import findNode

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)
 
    def test_walk_var_z(self):
        node = findNode(self.ast, line=11, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = TypeList()
        type2 = TypeList()
        type2.add_elem(get_new_string(const.REPORT_KEY))
        self.assertTrue(len(nodeType) == 2 and                                             \
                        any([type1 == elem for elem in nodeType]) and                      \
                        any([type2 == elem for elem in nodeType]),                         \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

if __name__ == '__main__':
    unittest.main()
