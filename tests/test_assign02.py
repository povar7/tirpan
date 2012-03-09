'''
Created on 09.03.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('assign02.py')

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

    def test_walk_var_el(self):
        node = findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 3 and                                       \
                        any([self.type_int   == elem for elem in nodeType]) and      \
                        any([self.type_float == elem for elem in nodeType]) and      \
                        any([self.type_str   == elem for elem in nodeType]),         \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'el', 'name is not "el"')

if __name__ == '__main__':
    unittest.main()
