'''
Created on 18.03.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('func03.py')

import ast

from typegraph    import *
from utils        import findNode

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)
#        config.types_number = 15

    def test_walk_var_z(self):
        node = findNode(self.ast, line=12, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = TypeList()
        type1.add_elem(self.type_int)
        type2 = self.type_float
        type3 = self.type_int
        type4 = self.type_unicode
        type5 = TypeList()
        type5.add_elem(self.type_str)
        type5.add_elem(type1)
        type6 = TypeList()
        type6.add_elem(type2)
        type6.add_elem(type1)
        type7 = TypeList()
        type7.add_elem(type2)
        type7.add_elem(type4)
        type8 = TypeList()
        type8.add_elem(type3)
        type8.add_elem(type1)
        type9 = TypeList()
        type9.add_elem(type3)
        type9.add_elem(type4)
        type10 = TypeList()
        type10.add_elem(type5)
        type10.add_elem(type1)
        type11 = TypeList()
        type11.add_elem(type5)
        type11.add_elem(type4)
        print nodeType
        print len(nodeType)
        print any([type9  == elem for elem in nodeType])
        print type9
        self.assertTrue(len(nodeType) == 11 and                                             \
                        any([type1  == elem for elem in nodeType]) and                      \
                        any([type2  == elem for elem in nodeType]) and                      \
                        any([type3  == elem for elem in nodeType]) and                      \
                        any([type4  == elem for elem in nodeType]) and                      \
                        any([type5  == elem for elem in nodeType]) and                      \
                        any([type6  == elem for elem in nodeType]) and                      \
                        any([type7  == elem for elem in nodeType]) and                      \
                        any([type8  == elem for elem in nodeType]) and                      \
                        any([type9  == elem for elem in nodeType]) and                      \
                        any([type10 == elem for elem in nodeType]) and                      \
                        any([type11 == elem for elem in nodeType]),                         \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

if __name__ == '__main__':
    unittest.main()
