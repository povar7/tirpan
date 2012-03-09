'''
Created on 07.01.2012

@author: bronikkk
'''

import unittest
from tests_common import *
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

        self.type_int     = TypeInt()
        self.type_float   = TypeFloat()
        self.type_str     = TypeStr()
        self.type_unicode = TypeUnicode()

    def test_walk_int(self):
        node = findNode(self.ast, line=1, col=6)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type info is not const')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([isinstance(elem, TypeInt) for elem in nodeType]),       \
                        'type of node is not an int')
        self.assertEqual(node.link.nodeValue, 1, 'value of node is not 1')

    def test_walk_float(self):
        node = findNode(self.ast, line=1, col=9)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type is not a constant')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([isinstance(elem, TypeFloat) for elem in nodeType]),     \
                        'type of node is not a float')
        self.assertEqual(node.link.nodeValue, 3.14, 'value of node is not 3.14')

    def test_walk_str(self):
        node = findNode(self.ast, line=1, col=15)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type is not a constant')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([isinstance(elem, TypeStr) for elem in nodeType]),       \
                        'type of node is not a str')
        self.assertEqual(node.link.nodeValue, 'abc', 'value of node is not "abc"')

    def test_walk_unicode(self):
        node = findNode(self.ast, line=1, col=22)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type is not a constant')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([isinstance(elem, TypeUnicode) for elem in nodeType]),   \
                        'type of node is not a unicode')
        self.assertEqual(node.link.nodeValue, u'XYZ', 'value of node is not u"XYZ"')

    def test_walk_list(self):
        node = findNode(self.ast, line=1, kind=ast.List)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ListTypeGraphNode), 'type is not a list')
        nodeType = node.link.nodeType
        type1 = TypeList()
        type1.add_elem(self.type_int)
        type1.add_elem(self.type_float)
        type1.add_elem(self.type_str)
        type1.add_elem(self.type_unicode)
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([type1 == elem for elem in nodeType]),                   \
                        'elems are int, float, str and unicode')

    def test_walk_tuple(self):
        node = findNode(self.ast, line=2, kind=ast.Tuple)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, TupleTypeGraphNode), 'type is not a tuple')
        nodeType = node.link.nodeType
        type1 = TypeTuple()
        type1.add_elem(self.type_int)
        type1.add_elem(self.type_float)
        type1.add_elem(self.type_str)
        type1.add_elem(self.type_unicode)
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([type1 == elem for elem in nodeType]),                   \
                        'elems are int, float, str and unicode')

    def test_walk_dict(self):
        node = findNode(self.ast, line=3, kind=ast.Dict)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, DictTypeGraphNode), 'type is not a dict')
        nodeType = node.link.nodeType
        type1 = TypeDict()
        type1.add_key(self.type_int)
        type1.add_val(self.type_float)
        type1.add_key(self.type_str)
        type1.add_val(self.type_unicode)
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([type1 == elem for elem in nodeType]),                   \
                        'keys are int, float; values are str and unicode')

    def test_walk_var_a(self):
        node = findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = TypeList()
        type1.add_elem(self.type_int)
        type1.add_elem(self.type_float)
        type1.add_elem(self.type_str)
        type1.add_elem(self.type_unicode)
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([type1 == elem for elem in nodeType]),                   \
                        'elems are int, float, str and unicode')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_walk_var_b(self):
        node = findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = TypeTuple()
        type1.add_elem(self.type_int)
        type1.add_elem(self.type_float)
        type1.add_elem(self.type_str)
        type1.add_elem(self.type_unicode)
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([type1 == elem for elem in nodeType]),                   \
                        'elems are int, float, str and unicode')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

    def test_walk_var_c(self):
        node = findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = TypeDict()
        type1.add_key(self.type_int)
        type1.add_val(self.type_float)
        type1.add_key(self.type_str)
        type1.add_val(self.type_unicode)
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([type1 == elem for elem in nodeType]),                   \
                        'keys are int, float; values are str and unicode')
        self.assertEqual(node.link.name, 'c', 'name is not "c"')

if __name__ == '__main__':
    unittest.main()
