'''
Created on 07.01.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('std01.py')

import ast

from init         import common_init
from errorprinter import ErrorPrinter
from scope        import Scope
from tiimporter   import Importer, QuasiAlias
from tiparser     import TIParser
from typegraph    import *
from typenodes    import *
from utils        import findNode

import tirpan

class TestTirpan(unittest.TestCase):
    def setUp(self):
        global global_scope, current_scope, current_res, error_printer, importer, verbose, test_results, test_precision, types_number
        global_scope   = Scope(None)
        current_scope  = global_scope
        current_res    = None
        error_printer  = ErrorPrinter()
        importer       = Importer()
        verbose        = False
        test_results   = False
        test_precision = False
        types_number   = 10

        common_init(global_scope, importer)
        tirpan.run(test_file_name)
        self.ast = importer.imported_files['__main__'].ast

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

    def test_walk_float(self):
        node = findNode(self.ast, line=1, col=9)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type is not a constant')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([isinstance(elem, TypeFloat) for elem in nodeType]),     \
                        'type of node is not a float')

    def test_walk_str(self):
        node = findNode(self.ast, line=1, col=15)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type is not a constant')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([isinstance(elem, TypeStr) for elem in nodeType]),       \
                        'type of node is not a str')

    def test_walk_unicode(self):
        node = findNode(self.ast, line=1, col=22)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, ConstTypeGraphNode), 'type is not a constant')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([isinstance(elem, TypeUnicode) for elem in nodeType]),   \
                        'type of node is not a unicode')

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
        type1.elems = (self.type_int, self.type_float,                               \
                       self.type_str, self.type_unicode)
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
        type1.elems = (self.type_int, self.type_float,                               \
                       self.type_str, self.type_unicode)
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
