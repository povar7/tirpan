'''
Created on 07.01.2012

@author: bronikkk
'''

import unittest
import ast

from tirpan import Tirpan
from utils  import findNode

from typegraph import *

class TestTirpan(unittest.TestCase):
    def setUp(self):
        app = Tirpan('tests/sample01.py')
        app.walk()
        self.ast = app.ast
        
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
