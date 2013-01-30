'''
Created on 19.08.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('misc01.py')

import ast

from typegraph    import *
from utils        import findNode

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)

    def test_walk_var_answer(self):
        node = findNode(self.ast, line=121, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        tmp = TypeTuple()
        tmp.elems = (self.type_int, self.type_int)
        type1 = TypeList()
        type1.add_elem(tmp)
        self.assertTrue(any([type1 == elem for elem in nodeType]),                   \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'answer', 'name is not "answer"')

if __name__ == '__main__':
    unittest.main()
