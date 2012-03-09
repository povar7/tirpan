'''
Created on 09.03.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('assign01.py')

import ast

from importer  import Importer
from scope     import Scope
from tiparser  import TIParser
from typegraph import *
from typenodes import *

from utils     import findNode

import tirpan

class TestTirpan(unittest.TestCase):
    def setUp(self):
        global current_scope, importer, verbose
        current_scope = None
        importer      = Importer()
        verbose       = False
        tirpan.run(test_file_name)
        import __main__
        self.ast = __main__.importer.imported_files['__main__'].ast

        self.type_int     = TypeInt()
        self.type_float   = TypeFloat()
        self.type_str     = TypeStr()
        self.type_unicode = TypeUnicode()

    def test_walk_var_a(self):
        node = findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = TypeList()
        type1.add_elem(self.type_int)
        type2 = TypeUnicode()
        self.assertTrue(len(nodeType) == 2 and                                       \
                        any([type1 == elem for elem in nodeType]) and                \
                        any([type2 == elem for elem in nodeType]),                   \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_walk_var_b(self):
        node = findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        tmp_type1 = TypeList()
        tmp_type1.add_elem(self.type_int)
        tmp_type2 = TypeUnicode()
        type1 = TypeList()
        type1.add_elem(self.type_str)
        type1.add_elem(tmp_type1)
        type2 = TypeList()
        type2.add_elem(self.type_str)
        type2.add_elem(tmp_type2)
        type3 = TypeFloat()
        self.assertTrue(len(nodeType) == 3 and                                       \
                        any([type1 == elem for elem in nodeType]) and                \
                        any([type2 == elem for elem in nodeType]) and                \
                        any([type3 == elem for elem in nodeType]),                   \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

if __name__ == '__main__':
    unittest.main()
