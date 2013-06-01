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
        nodeType = freeze(node.link.nodeType)
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
        nodeType = freeze(node.link.nodeType)
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

if __name__ == '__main__':
    unittest.main()
