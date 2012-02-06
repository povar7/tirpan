'''
Created on 07.01.2012

@author: bronikkk
'''

import ast
import unittest

import os
from os import sys
tests_dir      = os.path.dirname(sys.argv[0])
test_file_name = os.path.join(tests_dir, 'std01.py')
sys.path.append(os.path.join(tests_dir, '..'))

from importer  import Importer
from scope     import Scope
from tiparser  import TIParser
from typegraph import *

from utils     import findNode

import tirpan

class TestTirpan(unittest.TestCase):
    classIsSetup = False

    def setUp(self):
        global current_scope, importer, verbose
        current_scope = None
        importer      = Importer()
        verbose       = False
        tirpan.run(test_file_name)
        import __main__
        self.ast = __main__.importer.imported_files['__main__'].ast

    def test_walk_int(self):
        node = findNode(self.ast, line=1, col=6)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type info is not const')
        self.assertEqual(node.link.nodeType, set([int]), 'type of node is not int')
        self.assertEqual(node.link.nodeValue, 1, 'value of node is not 1')

    def test_walk_float(self):
        node = findNode(self.ast, line=1, col=9)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type is not a constant')
        self.assertEqual(node.link.nodeType, set([float]), 'type of node is not float')
        self.assertEqual(node.link.nodeValue, 3.14, 'value of node is not 3.14')

    def test_walk_str(self):
        node = findNode(self.ast, line=1, col=15)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type is not a constant')
        self.assertEqual(node.link.nodeType, set([str]), 'type of node is not str')
        self.assertEqual(node.link.nodeValue, 'abc', 'value of node is not "abc"')

    def test_walk_unicode(self):
        node = findNode(self.ast, line=1, col=22)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type is not a constant')
        self.assertEqual(node.link.nodeType, set([unicode]), 'type of node is not unicode')
        self.assertEqual(node.link.nodeValue, u'XYZ', 'value of node is not u"XYZ"')

    def test_walk_list(self):
        node = findNode(self.ast, line=1, kind=ast.List)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ListTypeGraphNode), 'type is not a list')

    def test_walk_tuple(self):
        node = findNode(self.ast, line=2, kind=ast.Tuple)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, TupleTypeGraphNode), 'type is not a tuple')

    def test_walk_dict(self):
        node = findNode(self.ast, line=3, kind=ast.Dict)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, DictTypeGraphNode), 'type is not a dict')

    def test_walk_var_a(self):
        node = findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_walk_var_b(self):
        node = findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

    def test_walk_var_c(self):
        node = findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        self.assertEqual(node.link.name, 'c', 'name is not "c"')

if __name__ == '__main__':
    unittest.main()