#!/usr/bin/env python

'''
Created on 01.06.2013

@author: bronikkk
'''

import ast
import os
import sys
import types
import unittest

import tirpan
import utils

from ti.sema   import *
from ti.tgnode import AttributeTGNode, VariableTGNode

import tests.const

class TestAssign01(unittest.TestCase):
    
    ast = tirpan.run('tests/assign01.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [set()] + [{LiteralSema(int)}]
        type1.freeze()
        type2 = LiteralValueSema(u'abc')
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_b(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = ListSema()
        childType1.elems = [set()] + [{LiteralSema(int)}]
        childType1.freeze()
        childType2 = LiteralValueSema(u'abc')
        type1 = ListSema()
        type1.elems  = [set()]
        type1.elems += [{LiteralValueSema('abc')}, {childType1, childType2}]
        type1.freeze()
        type2 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

    def test_c(self):
        node = utils.findNode(self.ast, line=6, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = ListSema()
        childType1.elems = [set()] + [{LiteralSema(int)}]
        childType1.freeze()
        childType2 = LiteralValueSema(u'abc')
        type1 = TupleSema()
        type1.elems  = [set()]
        type1.elems += [{LiteralValueSema('abc')}, {childType1, childType2}]
        type1.freeze()
        type2 = LiteralSema(complex)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'c', 'name is not "c"')

class TestAssign02(unittest.TestCase):
    
    ast = tirpan.run('tests/assign02.py')
        
    def test_el(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(float)
        type3 = LiteralValueSema('abc')
        self.assertTrue(len(nodeType) == 3 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'el', 'name is not "el"')

class TestAssign03(unittest.TestCase):
    
    ast = tirpan.run('tests/assign03.py')
        
    def test_el(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        type2 = LiteralValueSema('abc')
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'el', 'name is not "el"')

class TestAssign04(unittest.TestCase):
    
    ast = tirpan.run('tests/assign04.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(types.NoneType)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestBuiltin01(unittest.TestCase):
    
    ast = tirpan.run('tests/builtin01.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralSema(int)}]
        type1.freeze() 
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=5, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralSema(int)}]
        type1.freeze() 
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_z(self):
        node = utils.findNode(self.ast, line=6, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralSema(int)}]
        type1.freeze() 
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestBuiltin02(unittest.TestCase):
    
    ast = tirpan.run('tests/builtin02.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(type)
        isFunction = lambda x: isinstance(x, FunctionSema)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(isFunction(elem) for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(type)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestBuiltin03(unittest.TestCase):
    
    ast = tirpan.run('tests/builtin03.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralSema(float)}] + [{LiteralSema(int)}]
        type1.freeze() 
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralSema(float)}] + [{LiteralSema(int)}]
        type1.freeze() 
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_z(self):
        node = utils.findNode(self.ast, line=5, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralSema(float)}] + [{LiteralSema(int)}]
        type1.freeze() 
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

    def test_foo(self):
        node = utils.findNode(self.ast, line=7, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        self.assertTrue(len(nodeType) == 1,
                        'wrong types calculated')
        type1 = list(nodeType)[0]
        isFunction = lambda(x) : (isinstance(x, FunctionSema) and
                                  isinstance(x.parent, ListSema))
        self.assertTrue(len(nodeType) == 1 and
                        any(isFunction(elem) for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'foo', 'name is not "foo"')

class TestBuiltin06(unittest.TestCase):
    
    ast = tirpan.run('tests/builtin06.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=1, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema('tests/builtin06.py')
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestBuiltin07(unittest.TestCase):
    
    ast = tirpan.run('tests/builtin07.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=13, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        isModule = lambda(x) : (isinstance(x, ModuleSema) and
                                x.origin.name == 'posixpath')
        self.assertTrue(len(nodeType) == 1 and
                        any(isModule(elem) for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestBuiltin08(unittest.TestCase):
    
    ast = tirpan.run('tests/builtin08.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(tests.const.PLUGINS_DIR)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestImport01_1(unittest.TestCase):
    
    ast = tirpan.run('tests/import01_1.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=6, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems  = [set()] + [{LiteralSema(int)}]
        type1.elems += [{LiteralValueSema('abc')}, {LiteralSema(float)}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=7, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType = ListSema()
        childType.elems  = [set()] + [{LiteralSema(int)}]
        type1 = ListSema()
        type1.elems  = [set()] + [{childType}]
        type1.elems += [{LiteralValueSema('abc')}, {LiteralSema(float)}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestImport02(unittest.TestCase):
    
    ast = tirpan.run('tests/import02.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=12, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema('./test.py')
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=14, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType = LiteralValueSema(os.path.abspath('tests'))
        type1 = ListSema()
        type1.elems = [set()] + [{childType}]
        for elem in sys.path[1:]:
            type1.elems.append({LiteralValueSema(elem)})
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_z(self):
        node = utils.findNode(self.ast, line=16, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

    def test_t(self):
        node = utils.findNode(self.ast, line=18, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 't', 'name is not "t"')

class TestImport03_1(unittest.TestCase):
    
    ast = tirpan.run('tests/import03_1.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=3, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestImport03_2(unittest.TestCase):
    
    ast = tirpan.run('tests/import03_2.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=3, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_z(self):
        node = utils.findNode(self.ast, line=5, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(True)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestImport03_3(unittest.TestCase):
    
    ast = tirpan.run('tests/import03_3.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=3, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestImport04(unittest.TestCase):
    
    ast = tirpan.run('tests/import04_1.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_z(self):
        node = utils.findNode(self.ast, line=10, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestImport05_1(unittest.TestCase):
    
    ast = tirpan.run('tests/import05_1.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=14, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(float)
        type3 = LiteralSema(types.NoneType)
        type4 = LiteralValueSema(True)
        self.assertTrue(len(nodeType) == 4 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType) and
                        any(type4 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestImport06_1(unittest.TestCase):
    
    ast = tirpan.run('tests/import06_1.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=4, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestImport07_1(unittest.TestCase):
   
    ast = tirpan.run('tests/import07_1.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=3, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestImport08_1(unittest.TestCase):
    
    ast = tirpan.run('tests/import08_1.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=3, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestStd01(unittest.TestCase):
    
    ast = tirpan.run('tests/std01.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems  = [set()]
        type1.elems += [{LiteralSema(int)}, {LiteralSema(float)}]
        type1.elems += [{LiteralValueSema('abc')}, {LiteralValueSema(u'abc')}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_b(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = TupleSema()
        type1.elems  = [set()]
        type1.elems += [{LiteralSema(int)}, {LiteralSema(float)}]
        type1.elems += [{LiteralValueSema('abc')}, {LiteralValueSema(u'abc')}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

    def test_c(self):
        node = utils.findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = DictSema()
        type1.elems[LiteralValueSema(1    )] = {LiteralSema(float)}
        type1.elems[LiteralValueSema('abc')] = {LiteralValueSema(u'abc')}
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'c', 'name is not "c"')

class TestStd02(unittest.TestCase):
    
    ast = tirpan.run('tests/std02.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        type1 = DictSema()
        type1.elems[LiteralValueSema(1  )] = {LiteralSema(float)}
        type1.elems[LiteralValueSema('2')] = {LiteralSema(float)}
        type1.freeze()
        nodeType = freezeSet(node.link.nodeType)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_b(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        type1 = ListSema()
        type1.elems = [{LiteralSema(int)}] * 6
        type1.freeze()
        nodeType = freezeSet(node.link.nodeType)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

    def test_c(self):
        node = utils.findNode(self.ast, line=7, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralSema(int), LiteralSema(float)}] * 6
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'c', 'name is not "c"')

    def test_d(self):
        node = utils.findNode(self.ast, line=10, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralSema(int), LiteralSema(float)}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'd', 'name is not "d"')

    def test_e(self):
        node = utils.findNode(self.ast, line=12, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems.append({LiteralSema(int), LiteralSema(float)})
        type1.elems.append({LiteralSema(int)})
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'e', 'name is not "e"')

    def test_f(self):
        node = utils.findNode(self.ast, line=13, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralSema(int)}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'f', 'name is not "f"')

class TestStd03(unittest.TestCase):
    
    ast = tirpan.run('tests/std03.py')
        
    def test_True(self):
        node = utils.findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralValueSema(True)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'True', 'name is not "True"')

    def test_False(self):
        node = utils.findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(float)
        type2 = LiteralValueSema(False)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'False', 'name is not "False"')

class TestStd05(unittest.TestCase):
    
    ast = tirpan.run('tests/std05.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=4, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_b(self):
        node = utils.findNode(self.ast, line=4, col=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(float)
        type2 = LiteralValueSema('abc')
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

    def test_c(self):
        node = utils.findNode(self.ast, line=5, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'c', 'name is not "c"')

    def test_d(self):
        node = utils.findNode(self.ast, line=6, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(float)
        type2 = LiteralValueSema('abc')
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'd', 'name is not "d"')

class TestStd06(unittest.TestCase):
    
    ast = tirpan.run('tests/std06.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=5, col=6, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_b(self):
        node = utils.findNode(self.ast, line=5, col=9, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema('abc')
        type2 = LiteralValueSema(u'abc')
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

class TestFunc01(unittest.TestCase):
    
    ast = tirpan.run('tests/func01.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=4, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [set()] + [{LiteralSema(int)}]
        type1.freeze()
        type2 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestFunc02(unittest.TestCase):
    
    ast = tirpan.run('tests/func02.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=10, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType = ListSema()
        childType.elems = [set()] + [{LiteralSema(int)}]
        childType.freeze()
        type1 = ListSema()
        type1.elems = [set()] + [{LiteralValueSema('abc')}, {childType}]
        type1.freeze()
        type2 = LiteralSema(float)
        type3 = LiteralSema(int)
        type4 = childType
        type5 = LiteralValueSema(u'abc')
        self.assertTrue(len(nodeType) == 5 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType) and
                        any(type4 == elem for elem in nodeType) and
                        any(type5 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestFunc03(unittest.TestCase):
    
    ast = tirpan.run('tests/func03.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=12, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType = ListSema()
        childType.elems = [set()] + [{LiteralSema(int)}]
        childType.freeze()
        type1 = ListSema()
        type1.elems = [set()] + [{LiteralValueSema('abc')}, {childType}]
        type1.freeze()
        type2 = LiteralSema(float)
        type3 = LiteralSema(int)
        type4 = childType
        type5 = LiteralValueSema(u'abc')
        type6 = ListSema()
        type6.elems = [set()] + [{type1}, {type4}]
        type6.freeze()
        type7 = ListSema()
        type7.elems = [set()] + [{type1}, {type5}]
        type7.freeze()
        type8 = ListSema()
        type8.elems = [set()] + [{type2}, {type4}]
        type8.freeze()
        type9 = ListSema()
        type9.elems = [set()] + [{type2}, {type5}]
        type9.freeze()
        type10 = ListSema()
        type10.elems = [set()] + [{type3}, {type4}]
        type10.freeze()
        type11 = ListSema()
        type11.elems = [set()] + [{type3}, {type5}]
        type11.freeze()
        self.assertTrue(len(nodeType) == 11 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType) and
                        any(type4 == elem for elem in nodeType) and
                        any(type5 == elem for elem in nodeType) and
                        any(type6 == elem for elem in nodeType) and
                        any(type7 == elem for elem in nodeType) and
                        any(type8 == elem for elem in nodeType) and
                        any(type9 == elem for elem in nodeType) and
                        any(type10 == elem for elem in nodeType) and
                        any(type11 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestFunc04(unittest.TestCase):
    
    ast = tirpan.run('tests/func04.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=7, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = NoSema()
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestFunc05(unittest.TestCase):
    
    ast = tirpan.run('tests/func05.py')
        
    def test_u(self):
        node = utils.findNode(self.ast, line=25, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType = ListSema()
        childType.elems = [set()] + [{LiteralSema(int)}]
        childType.freeze()
        type1 = ListSema()
        type1.elems = [set()] + [{LiteralValueSema('abc')}, {childType}]
        type1.freeze()
        type2 = LiteralSema(float)
        type3 = LiteralSema(int)
        type4 = childType
        type5 = LiteralValueSema(u'abc')
        type6 = ListSema()
        type6.elems = [set()] + [{type1}, {type4}]
        type6.freeze()
        type7 = ListSema()
        type7.elems = [set()] + [{type1}, {type5}]
        type7.freeze()
        type8 = ListSema()
        type8.elems = [set()] + [{type2}, {type4}]
        type8.freeze()
        type9 = ListSema()
        type9.elems = [set()] + [{type2}, {type5}]
        type9.freeze()
        type10 = ListSema()
        type10.elems = [set()] + [{type3}, {type4}]
        type10.freeze()
        type11 = ListSema()
        type11.elems = [set()] + [{type3}, {type5}]
        type11.freeze()
        type12 = LiteralSema(complex)
        self.assertTrue(len(nodeType) == 12 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType) and
                        any(type4 == elem for elem in nodeType) and
                        any(type5 == elem for elem in nodeType) and
                        any(type6 == elem for elem in nodeType) and
                        any(type7 == elem for elem in nodeType) and
                        any(type8 == elem for elem in nodeType) and
                        any(type9 == elem for elem in nodeType) and
                        any(type10 == elem for elem in nodeType) and
                        any(type11 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'u', 'name is not "u"')

class TestFunc06(unittest.TestCase):
    
    ast = tirpan.run('tests/func06.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=4, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestFunc07(unittest.TestCase):
    
    ast = tirpan.run('tests/func07.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=4, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=5, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestFunc08(unittest.TestCase):
    
    ast = tirpan.run('tests/func08.py')
        
    def test_c(self):
        node = utils.findNode(self.ast, line=7, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'c', 'name is not "c"')

    def test_d(self):
        node = utils.findNode(self.ast, line=12, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'd', 'name is not "d"')

class TestFunc09(unittest.TestCase):
    
    ast = tirpan.run('tests/func09.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=4, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = LiteralSema(float)
        childType2 = LiteralValueSema('abc')
        type1 = TupleSema()
        type1.elems = [set()] + [{childType1}, {childType2}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=5, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = LiteralSema(float)
        childType2 = LiteralValueSema('abc')
        type1 = TupleSema()
        type1.elems = [set()] + [{childType1}, {childType2}, {childType1}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestFunc10(unittest.TestCase):
    
    ast = tirpan.run('tests/func10.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=4, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = DictSema()
        type1.elems[LiteralValueSema('foo')] = {LiteralSema(int)}
        type1.elems[LiteralValueSema('bar')] = {LiteralSema(float)}
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=5, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = DictSema()
        type1.elems[LiteralValueSema('mama')] = {LiteralSema(float)}
        type1.elems[LiteralValueSema('papa')] = {LiteralSema(int)}
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestFunc11(unittest.TestCase):
    
    ast = tirpan.run('tests/func11.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=5, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(types.NoneType)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=6, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(types.NoneType)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestFunc21(unittest.TestCase):
    
    ast = tirpan.run('tests/func21.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=4, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = TupleSema()
        type1.elems = [set()] + [{LiteralSema(int)}, {LiteralSema(float)}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=6, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = TupleSema()
        type1.elems = [set()] + [{LiteralSema(float)}, {LiteralSema(int)}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestFunc13(unittest.TestCase):
    
    ast = tirpan.run('tests/func13.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=7, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(types.NoneType)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=8, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(types.NoneType)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestFunc14(unittest.TestCase):
    
    ast = tirpan.run('tests/func14.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=6, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestFunc15(unittest.TestCase):
    
    ast = tirpan.run('tests/func15.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=7, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestFunc16(unittest.TestCase):
    
    ast = tirpan.run('tests/func16.py')
        
    def test_y(self):
        node = utils.findNode(self.ast, line=9, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralSema(long)}, {LiteralValueSema('abc')}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_z(self):
        node = utils.findNode(self.ast, line=10, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralSema(complex)}, {LiteralValueSema(u'abc')}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestFunc18(unittest.TestCase):
    
    ast = tirpan.run('tests/func18.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=5, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema('abc')
        type2 = LiteralSema(types.NoneType)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestFunc20(unittest.TestCase):
    
    ast = tirpan.run('tests/func20.py')
        
    def test_y(self):
        node = utils.findNode(self.ast, line=8, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = TupleSema()
        type1.elems = [set()] + [{LiteralSema(float)}, {LiteralSema(int)}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestFunc23(unittest.TestCase):
    
    ast = tirpan.run('tests/func23.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=8, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = LiteralSema(int)
        childType2 = LiteralSema(float)
        childType3 = LiteralValueSema('abc')
        childType4 = LiteralValueSema(u'abc')
        type1 = TupleSema()
        type1.elems = [set()] + [{childType3}, {childType1, childType2}]
        type1.freeze()
        type2 = TupleSema()
        type2.elems = [set()] + [{childType4}, {childType1, childType2}]
        type2.freeze()
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestGlobal01(unittest.TestCase):
    
    ast = tirpan.run('tests/global01.py')
        
    def test_res(self):
        node = utils.findNode(self.ast, line=1, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralSema(int)
        type3 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 3 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'res', 'name is not "res"')

class TestGlobal02(unittest.TestCase):
    
    ast = tirpan.run('tests/global02.py')
        
    def test_res(self):
        node = utils.findNode(self.ast, line=1, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'res', 'name is not "res"')

class TestGlobal03(unittest.TestCase):
    
    ast = tirpan.run('tests/global03.py')
        
    def test_res1(self):
        node = utils.findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralValueSema(True)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'res1', 'name is not "res1"')

    def test_res2(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'res2', 'name is not "res2"')

class TestGlobal04(unittest.TestCase):
    
    ast = tirpan.run('tests/global04.py')
        
    def test_res(self):
        node = utils.findNode(self.ast, line=8, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralSema(int)
        type3 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 3 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'res', 'name is not "res"')

class TestObject01(unittest.TestCase):
    
    ast = tirpan.run('tests/object01.py')
        
    def test_B_x(self):
        node = utils.findNode(self.ast, line=14, kind=ast.Attribute)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, AttributeTGNode),
                        'type is not an attribute')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')

    def test_b_x(self):
        node = utils.findNode(self.ast, line=15, kind=ast.Attribute)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, AttributeTGNode),
                        'type is not an attribute')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')

    def test_B_y(self):
        node = utils.findNode(self.ast, line=16, kind=ast.Attribute)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, AttributeTGNode),
                        'type is not an attribute')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')

    def test_b_y(self):
        node = utils.findNode(self.ast, line=17, kind=ast.Attribute)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, AttributeTGNode),
                        'type is not an attribute')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(long)
        type2 = LiteralValueSema('abc')
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')

    def test_b_t(self):
        node = utils.findNode(self.ast, line=18, kind=ast.Attribute)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, AttributeTGNode),
                        'type is not an attribute')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(long)
        type2 = LiteralValueSema('abc')
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')

    def test_c(self):
        node = utils.findNode(self.ast, line=21, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(complex)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'c', 'name is not "c"')

class TestObject02(unittest.TestCase):
    
    ast = tirpan.run('tests/object02.py')

    def test_b(self):
        node = utils.findNode(self.ast, line=9, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

class TestObject03(unittest.TestCase):
    
    ast = tirpan.run('tests/object03.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=12, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=13, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestObject04(unittest.TestCase):
    
    ast = tirpan.run('tests/object04.py')

    def test_d1(self):
        node = utils.findNode(self.ast, line=17, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralSema(int)
        type3 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 3 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'd1', 'name is not "d1"')

    def test_d2(self):
        node = utils.findNode(self.ast, line=18, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralSema(int)
        type3 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 3 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'd2', 'name is not "d2"')

    def test_d3(self):
        node = utils.findNode(self.ast, line=19, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralValueSema('abc')
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'd3', 'name is not "d3"')

class TestObject05(unittest.TestCase):
    
    ast = tirpan.run('tests/object05.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=14, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralSema(int)
        type3 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 3 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestObject06(unittest.TestCase):
    
    ast = tirpan.run('tests/object06.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=17, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=19, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestObject07(unittest.TestCase):
    
    ast = tirpan.run('tests/object07.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=17, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=21, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_z(self):
        node = utils.findNode(self.ast, line=23, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestObject08(unittest.TestCase):
    
    ast = tirpan.run('tests/object08.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=17, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestObject09(unittest.TestCase):
    
    ast = tirpan.run('tests/object09.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=10, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestObject10(unittest.TestCase):
    
    ast = tirpan.run('tests/object10.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=12, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema('./test.py')
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestObject11(unittest.TestCase):
    
    ast = tirpan.run('tests/object11.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=15, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=17, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_z(self):
        node = utils.findNode(self.ast, line=19, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(True)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestObject15(unittest.TestCase):
    
    ast = tirpan.run('tests/object15.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=17, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

if __name__ == '__main__':
    unittest.main()
