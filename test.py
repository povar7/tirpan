#!/usr/bin/env python

'''
Created on 01.06.2013

@author: bronikkk
'''

import ast
import unittest

import tirpan
import utils

from ti.sema   import *
from ti.tgnode import VariableTGNode

class TestAssign01(unittest.TestCase):
    
    ast = tirpan.run('tests/assign01.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode), 'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [LiteralSema(int)]
        type1.freeze()
        type2 = LiteralSema(unicode)
        self.assertTrue(len(nodeType) == 2 and
                        any([type1 == elem for elem in nodeType]) and
                        any([type2 == elem for elem in nodeType]),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_b(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode), 'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = ListSema()
        childType1.elems = [LiteralSema(int)]
        childType1.freeze()
        childType2 = LiteralSema(unicode)
        type1 = ListSema()
        type1.addElement(LiteralSema(str))
        type1.addElement(childType1)
        type1.addElement(childType2)
        type1.freeze()
        type2 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 2 and
                        any([type1 == elem for elem in nodeType]) and
                        any([type2 == elem for elem in nodeType]),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

    def test_c(self):
        node = utils.findNode(self.ast, line=6, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode), 'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = ListSema()
        childType1.elems = [LiteralSema(int)]
        childType1.freeze()
        childType2 = LiteralSema(unicode)
        type1 = TupleSema()
        type1.addElement(LiteralSema(str))
        type1.addElement(childType1)
        type1.addElement(childType2)
        type1.freeze()
        type2 = LiteralSema(complex)
        self.assertTrue(len(nodeType) == 2 and
                        any([type1 == elem for elem in nodeType]) and
                        any([type2 == elem for elem in nodeType]),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'c', 'name is not "c"')

class TestStd01(unittest.TestCase):
    
    ast = tirpan.run('tests/std01.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode), 'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [LiteralSema(int), LiteralSema(float), LiteralSema(str), LiteralSema(unicode)]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any([type1 == elem for elem in nodeType]),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_b(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode), 'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = TupleSema()
        type1.elems = [LiteralSema(int), LiteralSema(float), LiteralSema(str), LiteralSema(unicode)]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any([type1 == elem for elem in nodeType]),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

    def test_c(self):
        node = utils.findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode), 'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = DictSema()
        type1.elems[LiteralSema(int)] = {LiteralSema(float)}
        type1.elems[LiteralSema(str)] = {LiteralSema(unicode)}
        type1.elems[LiteralValueSema(1    )] = {LiteralSema(float)}
        type1.elems[LiteralValueSema('abc')] = {LiteralSema(unicode)}
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any([type1 == elem for elem in nodeType]),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'c', 'name is not "c"')

class TestStd02(unittest.TestCase):
    
    ast = tirpan.run('tests/std02.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode), 'type is not a var')
        type1 = DictSema()
        type1.elems[LiteralSema(int)] = {LiteralSema(float)}
        type1.elems[LiteralSema(str)] = {LiteralSema(float)}
        type1.elems[LiteralValueSema(1  )] = {LiteralSema(float)}
        type1.elems[LiteralValueSema('2')] = {LiteralSema(float)}
        type1.freeze()
        nodeType = freezeSet(node.link.nodeType)
        self.assertTrue(len(nodeType) == 1 and
                        any([type1 == elem for elem in nodeType]),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_b(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode), 'type is not a var')
        type1 = ListSema()
        type1.addElement(LiteralSema(int))
        type1.freeze()
        nodeType = freezeSet(node.link.nodeType)
        self.assertTrue(len(nodeType) == 1 and
                        any([type1 == elem for elem in nodeType]),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

    def test_c(self):
        node = utils.findNode(self.ast, line=7, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode), 'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.addElement(LiteralSema(int))
        type1.addElement(LiteralSema(float))
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any([type1 == elem for elem in nodeType]),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'c', 'name is not "c"')

    def test_d(self):
        node = utils.findNode(self.ast, line=10, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode), 'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.addElement(LiteralSema(int))
        type1.addElement(LiteralSema(float))
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any([type1 == elem for elem in nodeType]),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'd', 'name is not "d"')

    def test_e(self):
        node = utils.findNode(self.ast, line=12, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode), 'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.addElement(LiteralSema(int))
        type1.addElement(LiteralSema(float))
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any([type1 == elem for elem in nodeType]),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'e', 'name is not "e"')

    def test_f(self):
        node = utils.findNode(self.ast, line=13, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode), 'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.addElement(LiteralSema(int))
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any([type1 == elem for elem in nodeType]),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'f', 'name is not "f"')

if __name__ == '__main__':
    unittest.main()
