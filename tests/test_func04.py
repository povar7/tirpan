'''
Created on 18.03.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('func04.py')

import ast

from init       import common_init
from scope      import Scope
from tiimporter import Importer, QuasiAlias
from tiparser   import TIParser
from typegraph  import *
from typenodes  import *
from utils      import findNode

import tirpan

class TestTirpan(unittest.TestCase):
    def setUp(self):
        global global_scope, current_scope, current_res, importer, verbose
        global_scope  = Scope(None)
        current_scope = global_scope
        current_res   = None
        importer      = Importer()
        verbose       = False

        common_init(global_scope)
        tirpan.run(test_file_name)
        self.ast = importer.imported_files['__main__'].ast

        self.type_int     = TypeInt()
        self.type_long    = TypeLong()

    def test_walk_var_z(self):
        node = findNode(self.ast, line=7, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = self.type_int
        type2 = self.type_long
        self.assertTrue(len(nodeType) == 2 and                                              \
                        any([type1 == elem for elem in nodeType]) and                       \
                        any([type2 == elem for elem in nodeType]),                          \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

if __name__ == '__main__':
    unittest.main()
