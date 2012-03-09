'''
Created on 07.01.2012

@author: bronikkk
'''

import unittest
from test_utils import *
test_file_name = get_test_file_name('std01.py')

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

    def test_walk_int(self):
        node = findNode(self.ast, line=1, col=6)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type info is not const')
        nodeType = list(node.link.nodeType)
        self.assertTrue(len(nodeType) == 1 and isinstance(nodeType[0], TypeInt), \
                        'type of node is not an int')
        self.assertEqual(node.link.nodeValue, 1, 'value of node is not 1')

    def test_walk_float(self):
        node = findNode(self.ast, line=1, col=9)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type is not a constant')
        nodeType = list(node.link.nodeType)
        self.assertTrue(len(nodeType) == 1 and isinstance(nodeType[0], TypeFloat), \
                        'type of node is not a float')
        self.assertEqual(node.link.nodeValue, 3.14, 'value of node is not 3.14')

    def test_walk_str(self):
        node = findNode(self.ast, line=1, col=15)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type is not a constant')
        nodeType = list(node.link.nodeType)
        self.assertTrue(len(nodeType) == 1 and isinstance(nodeType[0], TypeStr), \
                        'type of node is not a str')
        self.assertEqual(node.link.nodeValue, 'abc', 'value of node is not "abc"')

    def test_walk_unicode(self):
        node = findNode(self.ast, line=1, col=22)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type is not a constant')
        nodeType = list(node.link.nodeType)
        self.assertTrue(len(nodeType) == 1 and isinstance(nodeType[0], TypeUnicode), \
                        'type of node is not a unicode')
        self.assertEqual(node.link.nodeValue, u'XYZ', 'value of node is not u"XYZ"')

    def test_walk_list(self):
        node = findNode(self.ast, line=1, kind=ast.List)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ListTypeGraphNode), 'type is not a list')
        nodeType = list(node.link.nodeType)
        self.assertTrue(len(nodeType) == 1 and isinstance(nodeType[0], TypeList),    \
                        'type is not a list')
        elemsType = list(nodeType[0].elems)
        self.assertTrue(len(elemsType) == 4 and \
                        any([isinstance(elem, TypeInt) for elem in elemsType]) and   \
                        any([isinstance(elem, TypeFloat) for elem in elemsType]) and \
                        any([isinstance(elem, TypeStr) for elem in elemsType]) and   \
                        any([isinstance(elem, TypeUnicode) for elem in elemsType]),  \
                        'elems are int, float, str and unicode')

    def test_walk_tuple(self):
        node = findNode(self.ast, line=2, kind=ast.Tuple)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, TupleTypeGraphNode), 'type is not a tuple')
        nodeType = list(node.link.nodeType)
        self.assertTrue(len(nodeType) == 1 and isinstance(nodeType[0], TypeTuple),   \
                        'type is not a tuple')
        elemsType = list(nodeType[0].elems)
        self.assertTrue(len(elemsType) == 4 and \
                        any([isinstance(elem, TypeInt) for elem in elemsType]) and   \
                        any([isinstance(elem, TypeFloat) for elem in elemsType]) and \
                        any([isinstance(elem, TypeStr) for elem in elemsType]) and   \
                        any([isinstance(elem, TypeUnicode) for elem in elemsType]),  \
                        'elems are int, float, str and unicode')

    def test_walk_dict(self):
        node = findNode(self.ast, line=3, kind=ast.Dict)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, DictTypeGraphNode), 'type is not a dict')
        nodeType = list(node.link.nodeType)
        self.assertTrue(len(nodeType) == 1 and isinstance(nodeType[0], TypeDict),    \
                        'type is not a dict')
        valsType = list(nodeType[0].vals)
        keysType = list(nodeType[0].keys)
        self.assertTrue(len(keysType) == 2 and \
                        any([isinstance(elem, TypeInt) for elem in keysType]) and    \
                        any([isinstance(elem, TypeStr) for elem in keysType]),       \
                        'keys are int, str')
        self.assertTrue(len(valsType) == 2 and \
                        any([isinstance(elem, TypeFloat) for elem in valsType]) and  \
                        any([isinstance(elem, TypeUnicode) for elem in valsType]),   \
                        'values are float, unicode')

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
