#!/usr/bin/env python

'''
Created on 01.06.2013

@author: bronikkk
'''

import ast
import datetime
import os
import platform
import re
import sys
import types
import unittest

import tirpan
import utils

from ti.sema   import *
from ti.tgnode import AttributeTGNode
from ti.tgnode import VariableTGNode, FunctionDefinitionTGNode

import tests.const
from   tests.ggettext import gettext as _

tirpan_dir  = os.path.dirname(sys.argv[0])
noattr_conf = os.path.join(tirpan_dir, 'cfg', 'orak_na.ini')

class TestAssign01(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/assign01.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
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
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
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
        node = utils.findNode(self.ast, line=12, kind=ast.Name)
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
    
    ast, defects = tirpan.run('tests/assign02.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
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
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestAssign03(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/assign03.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
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
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestAssign04(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/assign04.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        type2 = LiteralSema(types.NoneType)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestAssign05(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/assign05.py')
        
    def test_y(self):
        node = utils.findNode(self.ast, line=7, kind=ast.Name)
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

class TestBinop01(unittest.TestCase):

    ast, defects = tirpan.run('tests/binop01.py')

    tBool    = LiteralSema(bool)
    tInt     = LiteralSema(int)
    tLong    = LiteralSema(long)
    tFloat   = LiteralSema(float)
    tComplex = LiteralSema(complex)
    tStr     = LiteralSema(str)
    tUnicode = LiteralSema(unicode)

    def test_walk_var_x001(self):
        node = utils.findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x001', 'name is not "x001"')

    def test_walk_var_x002(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x002', 'name is not "x002"')

    def test_walk_var_x003(self):
        node = utils.findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x003', 'name is not "x003"')

    def test_walk_var_x004(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x004', 'name is not "x004"')

    def test_walk_var_x005(self):
        node = utils.findNode(self.ast, line=5, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x005', 'name is not "x005"')

    def test_walk_var_x006(self):
        node = utils.findNode(self.ast, line=6, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x006', 'name is not "x006"')

    def test_walk_var_x007(self):
        node = utils.findNode(self.ast, line=7, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x007', 'name is not "x007"')

    def test_walk_var_x008(self):
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x008', 'name is not "x008"')

    def test_walk_var_x009(self):
        node = utils.findNode(self.ast, line=9, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x009', 'name is not "x009"')

    def test_walk_var_x010(self):
        node = utils.findNode(self.ast, line=10, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x010', 'name is not "x010"')

    def test_walk_var_x011(self):
        node = utils.findNode(self.ast, line=11, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x011', 'name is not "x011"')

    def test_walk_var_x012(self):
        node = utils.findNode(self.ast, line=12, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x012', 'name is not "x012"')

    def test_walk_var_x013(self):
        node = utils.findNode(self.ast, line=13, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x013', 'name is not "x013"')

    def test_walk_var_x014(self):
        node = utils.findNode(self.ast, line=14, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x014', 'name is not "x014"')

    def test_walk_var_x015(self):
        node = utils.findNode(self.ast, line=15, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x015', 'name is not "x015"')

    def test_walk_var_x016(self):
        node = utils.findNode(self.ast, line=16, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x016', 'name is not "x016"')

    def test_walk_var_x017(self):
        node = utils.findNode(self.ast, line=17, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x017', 'name is not "x017"')

    def test_walk_var_x018(self):
        node = utils.findNode(self.ast, line=18, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x018', 'name is not "x018"')

    def test_walk_var_x019(self):
        node = utils.findNode(self.ast, line=19, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x019', 'name is not "x019"')

    def test_walk_var_x020(self):
        node = utils.findNode(self.ast, line=20, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x020', 'name is not "x020"')

    def test_walk_var_x021(self):
        node = utils.findNode(self.ast, line=21, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x021', 'name is not "x021"')

    def test_walk_var_x022(self):
        node = utils.findNode(self.ast, line=22, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x022', 'name is not "x022"')

    def test_walk_var_x023(self):
        node = utils.findNode(self.ast, line=23, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x023', 'name is not "x023"')

    def test_walk_var_x024(self):
        node = utils.findNode(self.ast, line=24, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x024', 'name is not "x024"')

    def test_walk_var_x025(self):
        node = utils.findNode(self.ast, line=25, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x025', 'name is not "x025"')

    def test_walk_var_x026(self):
        node = utils.findNode(self.ast, line=26, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema('11')
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x026', 'name is not "x026"')

    def test_walk_var_x027(self):
        node = utils.findNode(self.ast, line=27, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(u'11')
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x027', 'name is not "x027"')

    def test_walk_var_x028(self):
        node = utils.findNode(self.ast, line=28, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(u'11')
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x028', 'name is not "x028"')

    def test_walk_var_x029(self):
        node = utils.findNode(self.ast, line=29, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(u'11')
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x029', 'name is not "x029"')

    def test_walk_var_x030(self):
        node = utils.findNode(self.ast, line=30, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema (); type1.elems = [{self.tInt}] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x030', 'name is not "x030"')

    def test_walk_var_x031(self):
        node = utils.findNode(self.ast, line=31, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = TupleSema(); type1.elems = [{self.tInt}] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x031', 'name is not "x031"')

    def test_walk_var_x032(self):
        node = utils.findNode(self.ast, line=32, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x032', 'name is not "x032"')

    def test_walk_var_x033(self):
        node = utils.findNode(self.ast, line=33, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x033', 'name is not "x033"')

    def test_walk_var_x034(self):
        node = utils.findNode(self.ast, line=34, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x034', 'name is not "x034"')

    def test_walk_var_x035(self):
        node = utils.findNode(self.ast, line=35, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x035', 'name is not "x035"')

    def test_walk_var_x036(self):
        node = utils.findNode(self.ast, line=36, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x036', 'name is not "x036"')

    def test_walk_var_x037(self):
        node = utils.findNode(self.ast, line=37, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x037', 'name is not "x037"')

    def test_walk_var_x038(self):
        node = utils.findNode(self.ast, line=38, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x038', 'name is not "x038"')

    def test_walk_var_x039(self):
        node = utils.findNode(self.ast, line=39, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x039', 'name is not "x039"')

    def test_walk_var_x040(self):
        node = utils.findNode(self.ast, line=40, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x040', 'name is not "x040"')

    def test_walk_var_x041(self):
        node = utils.findNode(self.ast, line=41, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x041', 'name is not "x041"')

    def test_walk_var_x042(self):
        node = utils.findNode(self.ast, line=42, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x042', 'name is not "x042"')

    def test_walk_var_x043(self):
        node = utils.findNode(self.ast, line=43, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x043', 'name is not "x043"')

    def test_walk_var_x044(self):
        node = utils.findNode(self.ast, line=44, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x044', 'name is not "x044"')

    def test_walk_var_x045(self):
        node = utils.findNode(self.ast, line=45, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x045', 'name is not "x045"')

    def test_walk_var_x046(self):
        node = utils.findNode(self.ast, line=46, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x046', 'name is not "x046"')

    def test_walk_var_x047(self):
        node = utils.findNode(self.ast, line=47, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x047', 'name is not "x047"')

    def test_walk_var_x048(self):
        node = utils.findNode(self.ast, line=48, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x048', 'name is not "x048"')

    def test_walk_var_x049(self):
        node = utils.findNode(self.ast, line=49, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x049', 'name is not "x049"')

    def test_walk_var_x050(self):
        node = utils.findNode(self.ast, line=50, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x050', 'name is not "x050"')

    def test_walk_var_x051(self):
        node = utils.findNode(self.ast, line=51, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x051', 'name is not "x051"')

    def test_walk_var_x052(self):
        node = utils.findNode(self.ast, line=52, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x052', 'name is not "x052"')

    def test_walk_var_x053(self):
        node = utils.findNode(self.ast, line=53, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x053', 'name is not "x053"')

    def test_walk_var_x054(self):
        node = utils.findNode(self.ast, line=54, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x054', 'name is not "x054"')

    def test_walk_var_x055(self):
        node = utils.findNode(self.ast, line=55, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x055', 'name is not "x055"')

    def test_walk_var_x056(self):
        node = utils.findNode(self.ast, line=56, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x056', 'name is not "x056"')

    def test_walk_var_x057(self):
        node = utils.findNode(self.ast, line=57, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x057', 'name is not "x057"')

    def test_walk_var_x058(self):
        node = utils.findNode(self.ast, line=58, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x058', 'name is not "x058"')

    def test_walk_var_x059(self):
        node = utils.findNode(self.ast, line=59, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x059', 'name is not "x059"')

    def test_walk_var_x060(self):
        node = utils.findNode(self.ast, line=60, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x060', 'name is not "x060"')

    def test_walk_var_x061(self):
        node = utils.findNode(self.ast, line=61, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x061', 'name is not "x061"')

    def test_walk_var_x062(self):
        node = utils.findNode(self.ast, line=62, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tStr
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x062', 'name is not "x062"')

    def test_walk_var_x063(self):
        node = utils.findNode(self.ast, line=63, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tUnicode
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x063', 'name is not "x063"')

    def test_walk_var_x064(self):
        node = utils.findNode(self.ast, line=64, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema (); type1.elems = [set()] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x064', 'name is not "x064"')

    def test_walk_var_x065(self):
        node = utils.findNode(self.ast, line=65, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = TupleSema(); type1.elems = [set()] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x065', 'name is not "x065"')

    def test_walk_var_x066(self):
        node = utils.findNode(self.ast, line=66, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x066', 'name is not "x066"')

    def test_walk_var_x067(self):
        node = utils.findNode(self.ast, line=67, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x067', 'name is not "x067"')

    def test_walk_var_x068(self):
        node = utils.findNode(self.ast, line=68, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x068', 'name is not "x068"')

    def test_walk_var_x069(self):
        node = utils.findNode(self.ast, line=69, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x069', 'name is not "x069"')

    def test_walk_var_x070(self):
        node = utils.findNode(self.ast, line=70, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x070', 'name is not "x070"')

    def test_walk_var_x071(self):
        node = utils.findNode(self.ast, line=71, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tStr
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x071', 'name is not "x071"')

    def test_walk_var_x072(self):
        node = utils.findNode(self.ast, line=72, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tUnicode
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x072', 'name is not "x072"')

    def test_walk_var_x073(self):
        node = utils.findNode(self.ast, line=73, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema (); type1.elems = [set()] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x073', 'name is not "x073"')

    def test_walk_var_x074(self):
        node = utils.findNode(self.ast, line=74, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = TupleSema(); type1.elems = [set()] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x074', 'name is not "x074"')

    def test_walk_var_x075(self):
        node = utils.findNode(self.ast, line=75, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x075', 'name is not "x075"')

    def test_walk_var_x076(self):
        node = utils.findNode(self.ast, line=76, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x076', 'name is not "x076"')

    def test_walk_var_x077(self):
        node = utils.findNode(self.ast, line=77, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x077', 'name is not "x077"')

    def test_walk_var_x078(self):
        node = utils.findNode(self.ast, line=78, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x078', 'name is not "x078"')

    def test_walk_var_x079(self):
        node = utils.findNode(self.ast, line=79, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x079', 'name is not "x079"')

    def test_walk_var_x080(self):
        node = utils.findNode(self.ast, line=80, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tStr
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x080', 'name is not "x080"')

    def test_walk_var_x081(self):
        node = utils.findNode(self.ast, line=81, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tUnicode
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x081', 'name is not "x081"')

    def test_walk_var_x082(self):
        node = utils.findNode(self.ast, line=82, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema (); type1.elems = [set()] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x082', 'name is not "x082"')

    def test_walk_var_x083(self):
        node = utils.findNode(self.ast, line=83, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = TupleSema(); type1.elems = [set()] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x083', 'name is not "x083"')

    def test_walk_var_x084(self):
        node = utils.findNode(self.ast, line=84, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x084', 'name is not "x084"')

    def test_walk_var_x085(self):
        node = utils.findNode(self.ast, line=85, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x085', 'name is not "x085"')

    def test_walk_var_x086(self):
        node = utils.findNode(self.ast, line=86, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x086', 'name is not "x086"')

    def test_walk_var_x087(self):
        node = utils.findNode(self.ast, line=87, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x087', 'name is not "x087"')

    def test_walk_var_x088(self):
        node = utils.findNode(self.ast, line=88, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x088', 'name is not "x088"')

    def test_walk_var_x089(self):
        node = utils.findNode(self.ast, line=89, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x089', 'name is not "x089"')

    def test_walk_var_x090(self):
        node = utils.findNode(self.ast, line=90, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x090', 'name is not "x090"')

    def test_walk_var_x091(self):
        node = utils.findNode(self.ast, line=91, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x091', 'name is not "x091"')

    def test_walk_var_x092(self):
        node = utils.findNode(self.ast, line=92, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x092', 'name is not "x092"')

    def test_walk_var_x093(self):
        node = utils.findNode(self.ast, line=93, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x093', 'name is not "x093"')

    def test_walk_var_x094(self):
        node = utils.findNode(self.ast, line=94, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tStr
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x094', 'name is not "x094"')

    def test_walk_var_x095(self):
        node = utils.findNode(self.ast, line=95, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tStr
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x095', 'name is not "x095"')

    def test_walk_var_x096(self):
        node = utils.findNode(self.ast, line=96, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tStr
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x096', 'name is not "x096"')

    def test_walk_var_x097(self):
        node = utils.findNode(self.ast, line=97, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tUnicode
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x097', 'name is not "x097"')

    def test_walk_var_x098(self):
        node = utils.findNode(self.ast, line=98, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tUnicode
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x098', 'name is not "x098"')

    def test_walk_var_x099(self):
        node = utils.findNode(self.ast, line=99, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tUnicode
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x099', 'name is not "x099"')

    def test_walk_var_x100(self):
        node = utils.findNode(self.ast, line=100, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema (); type1.elems = [set()] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x100', 'name is not "x100"')

    def test_walk_var_x101(self):
        node = utils.findNode(self.ast, line=101, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema (); type1.elems = [set()] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x101', 'name is not "x101"')

    def test_walk_var_x102(self):
        node = utils.findNode(self.ast, line=102, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema (); type1.elems = [set()] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x102', 'name is not "x102"')

    def test_walk_var_x103(self):
        node = utils.findNode(self.ast, line=103, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = TupleSema(); type1.elems = [set()] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x103', 'name is not "x103"')

    def test_walk_var_x104(self):
        node = utils.findNode(self.ast, line=104, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = TupleSema(); type1.elems = [set()] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x104', 'name is not "x104"')

    def test_walk_var_x105(self):
        node = utils.findNode(self.ast, line=105, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = TupleSema(); type1.elems = [set()] + [{self.tInt}] * 2
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x105', 'name is not "x105"')

    def test_walk_var_x106(self):
        node = utils.findNode(self.ast, line=106, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x106', 'name is not "x106"')

    def test_walk_var_x107(self):
        node = utils.findNode(self.ast, line=107, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x107', 'name is not "x107"')

    def test_walk_var_x108(self):
        node = utils.findNode(self.ast, line=108, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x108', 'name is not "x108"')

    def test_walk_var_x109(self):
        node = utils.findNode(self.ast, line=109, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x109', 'name is not "x109"')

    def test_walk_var_x110(self):
        node = utils.findNode(self.ast, line=110, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x110', 'name is not "x110"')

    def test_walk_var_x111(self):
        node = utils.findNode(self.ast, line=111, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x111', 'name is not "x111"')

    def test_walk_var_x112(self):
        node = utils.findNode(self.ast, line=112, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x112', 'name is not "x112"')

    def test_walk_var_x113(self):
        node = utils.findNode(self.ast, line=113, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x113', 'name is not "x113"')

    def test_walk_var_x114(self):
        node = utils.findNode(self.ast, line=114, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x114', 'name is not "x114"')

    def test_walk_var_x115(self):
        node = utils.findNode(self.ast, line=115, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x115', 'name is not "x115"')

    def test_walk_var_x116(self):
        node = utils.findNode(self.ast, line=116, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x116', 'name is not "x116"')

    def test_walk_var_x117(self):
        node = utils.findNode(self.ast, line=117, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x117', 'name is not "x117"')

    def test_walk_var_x118(self):
        node = utils.findNode(self.ast, line=118, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x118', 'name is not "x118"')

    def test_walk_var_x119(self):
        node = utils.findNode(self.ast, line=119, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x119', 'name is not "x119"')

    def test_walk_var_x120(self):
        node = utils.findNode(self.ast, line=120, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x120', 'name is not "x120"')

    def test_walk_var_x121(self):
        node = utils.findNode(self.ast, line=121, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x121', 'name is not "x121"')

    def test_walk_var_x122(self):
        node = utils.findNode(self.ast, line=122, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x122', 'name is not "x122"')

    def test_walk_var_x123(self):
        node = utils.findNode(self.ast, line=123, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x123', 'name is not "x123"')

    def test_walk_var_x124(self):
        node = utils.findNode(self.ast, line=124, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x124', 'name is not "x124"')

    def test_walk_var_x125(self):
        node = utils.findNode(self.ast, line=125, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x125', 'name is not "x125"')

    def test_walk_var_x126(self):
        node = utils.findNode(self.ast, line=126, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x126', 'name is not "x126"')

    def test_walk_var_x127(self):
        node = utils.findNode(self.ast, line=127, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x127', 'name is not "x127"')

    def test_walk_var_x128(self):
        node = utils.findNode(self.ast, line=128, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x128', 'name is not "x128"')

    def test_walk_var_x129(self):
        node = utils.findNode(self.ast, line=129, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x129', 'name is not "x129"')

    def test_walk_var_x130(self):
        node = utils.findNode(self.ast, line=130, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x130', 'name is not "x130"')

    def test_walk_var_x131(self):
        node = utils.findNode(self.ast, line=131, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x131', 'name is not "x131"')

    def test_walk_var_x132(self):
        node = utils.findNode(self.ast, line=132, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x132', 'name is not "x132"')

    def test_walk_var_x133(self):
        node = utils.findNode(self.ast, line=133, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x133', 'name is not "x133"')

    def test_walk_var_x134(self):
        node = utils.findNode(self.ast, line=134, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x134', 'name is not "x134"')

    def test_walk_var_x135(self):
        node = utils.findNode(self.ast, line=135, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x135', 'name is not "x135"')

    def test_walk_var_x136(self):
        node = utils.findNode(self.ast, line=136, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x136', 'name is not "x136"')

    def test_walk_var_x137(self):
        node = utils.findNode(self.ast, line=137, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x137', 'name is not "x137"')

    def test_walk_var_x138(self):
        node = utils.findNode(self.ast, line=138, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x138', 'name is not "x138"')

    def test_walk_var_x139(self):
        node = utils.findNode(self.ast, line=139, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x139', 'name is not "x139"')

    def test_walk_var_x140(self):
        node = utils.findNode(self.ast, line=140, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x140', 'name is not "x140"')

    def test_walk_var_x141(self):
        node = utils.findNode(self.ast, line=141, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x141', 'name is not "x141"')

    def test_walk_var_x142(self):
        node = utils.findNode(self.ast, line=142, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x142', 'name is not "x142"')

    def test_walk_var_x143(self):
        node = utils.findNode(self.ast, line=143, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x143', 'name is not "x143"')

    def test_walk_var_x144(self):
        node = utils.findNode(self.ast, line=144, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x144', 'name is not "x144"')

    def test_walk_var_x145(self):
        node = utils.findNode(self.ast, line=145, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x145', 'name is not "x145"')

    def test_walk_var_x146(self):
        node = utils.findNode(self.ast, line=146, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x146', 'name is not "x146"')

    def test_walk_var_x147(self):
        node = utils.findNode(self.ast, line=147, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x147', 'name is not "x147"')

    def test_walk_var_x148(self):
        node = utils.findNode(self.ast, line=148, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x148', 'name is not "x148"')

    def test_walk_var_x149(self):
        node = utils.findNode(self.ast, line=149, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x149', 'name is not "x149"')

    def test_walk_var_x150(self):
        node = utils.findNode(self.ast, line=150, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x150', 'name is not "x150"')

    def test_walk_var_x151(self):
        node = utils.findNode(self.ast, line=151, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x151', 'name is not "x151"')

    def test_walk_var_x152(self):
        node = utils.findNode(self.ast, line=152, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x152', 'name is not "x152"')

    def test_walk_var_x153(self):
        node = utils.findNode(self.ast, line=153, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x153', 'name is not "x153"')

    def test_walk_var_x154(self):
        node = utils.findNode(self.ast, line=154, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x154', 'name is not "x154"')

    def test_walk_var_x155(self):
        node = utils.findNode(self.ast, line=155, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x155', 'name is not "x155"')

    def test_walk_var_x156(self):
        node = utils.findNode(self.ast, line=156, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x156', 'name is not "x156"')

    def test_walk_var_x157(self):
        node = utils.findNode(self.ast, line=157, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x157', 'name is not "x157"')

    def test_walk_var_x158(self):
        node = utils.findNode(self.ast, line=158, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x158', 'name is not "x158"')

    def test_walk_var_x159(self):
        node = utils.findNode(self.ast, line=159, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x159', 'name is not "x159"')

    def test_walk_var_x160(self):
        node = utils.findNode(self.ast, line=160, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x160', 'name is not "x160"')

    def test_walk_var_x161(self):
        node = utils.findNode(self.ast, line=161, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x161', 'name is not "x161"')

    def test_walk_var_x162(self):
        node = utils.findNode(self.ast, line=162, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x162', 'name is not "x162"')

    def test_walk_var_x163(self):
        node = utils.findNode(self.ast, line=163, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema('1')
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x163', 'name is not "x163"')

    def test_walk_var_x164(self):
        node = utils.findNode(self.ast, line=164, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(u'1')
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x164', 'name is not "x164"')

    def test_walk_var_x165(self):
        node = utils.findNode(self.ast, line=165, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x165', 'name is not "x165"')

    def test_walk_var_x166(self):
        node = utils.findNode(self.ast, line=166, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x166', 'name is not "x166"')

    def test_walk_var_x167(self):
        node = utils.findNode(self.ast, line=167, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x167', 'name is not "x167"')

    def test_walk_var_x168(self):
        node = utils.findNode(self.ast, line=168, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x168', 'name is not "x168"')

    def test_walk_var_x169(self):
        node = utils.findNode(self.ast, line=169, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x169', 'name is not "x169"')

    def test_walk_var_x170(self):
        node = utils.findNode(self.ast, line=170, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x170', 'name is not "x170"')

    def test_walk_var_x171(self):
        node = utils.findNode(self.ast, line=171, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x171', 'name is not "x171"')

    def test_walk_var_x172(self):
        node = utils.findNode(self.ast, line=172, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x172', 'name is not "x172"')

    def test_walk_var_x173(self):
        node = utils.findNode(self.ast, line=173, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x173', 'name is not "x173"')

    def test_walk_var_x174(self):
        node = utils.findNode(self.ast, line=174, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x174', 'name is not "x174"')

    def test_walk_var_x175(self):
        node = utils.findNode(self.ast, line=175, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x175', 'name is not "x175"')

    def test_walk_var_x176(self):
        node = utils.findNode(self.ast, line=176, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x176', 'name is not "x176"')

    def test_walk_var_x177(self):
        node = utils.findNode(self.ast, line=177, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x177', 'name is not "x177"')

    def test_walk_var_x178(self):
        node = utils.findNode(self.ast, line=178, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x178', 'name is not "x178"')

    def test_walk_var_x179(self):
        node = utils.findNode(self.ast, line=179, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x179', 'name is not "x179"')

    def test_walk_var_x180(self):
        node = utils.findNode(self.ast, line=180, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x180', 'name is not "x180"')

    def test_walk_var_x181(self):
        node = utils.findNode(self.ast, line=181, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x181', 'name is not "x181"')

    def test_walk_var_x182(self):
        node = utils.findNode(self.ast, line=182, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x182', 'name is not "x182"')

    def test_walk_var_x183(self):
        node = utils.findNode(self.ast, line=183, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tBool
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x183', 'name is not "x183"')

    def test_walk_var_x184(self):
        node = utils.findNode(self.ast, line=184, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x184', 'name is not "x184"')

    def test_walk_var_x185(self):
        node = utils.findNode(self.ast, line=185, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x185', 'name is not "x185"')

    def test_walk_var_x186(self):
        node = utils.findNode(self.ast, line=186, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x186', 'name is not "x186"')

    def test_walk_var_x187(self):
        node = utils.findNode(self.ast, line=187, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x187', 'name is not "x187"')

    def test_walk_var_x188(self):
        node = utils.findNode(self.ast, line=188, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x188', 'name is not "x188"')

    def test_walk_var_x189(self):
        node = utils.findNode(self.ast, line=189, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x189', 'name is not "x189"')

    def test_walk_var_x190(self):
        node = utils.findNode(self.ast, line=190, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x190', 'name is not "x190"')

    def test_walk_var_x191(self):
        node = utils.findNode(self.ast, line=191, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x191', 'name is not "x191"')

    def test_walk_var_x192(self):
        node = utils.findNode(self.ast, line=192, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tBool
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x192', 'name is not "x192"')

    def test_walk_var_x193(self):
        node = utils.findNode(self.ast, line=193, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x193', 'name is not "x193"')

    def test_walk_var_x194(self):
        node = utils.findNode(self.ast, line=194, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x194', 'name is not "x194"')

    def test_walk_var_x195(self):
        node = utils.findNode(self.ast, line=195, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x195', 'name is not "x195"')

    def test_walk_var_x196(self):
        node = utils.findNode(self.ast, line=196, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x196', 'name is not "x196"')

    def test_walk_var_x197(self):
        node = utils.findNode(self.ast, line=197, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x197', 'name is not "x197"')

    def test_walk_var_x198(self):
        node = utils.findNode(self.ast, line=198, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x198', 'name is not "x198"')

    def test_walk_var_x199(self):
        node = utils.findNode(self.ast, line=199, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x199', 'name is not "x199"')

    def test_walk_var_x200(self):
        node = utils.findNode(self.ast, line=200, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x200', 'name is not "x200"')

    def test_walk_var_x201(self):
        node = utils.findNode(self.ast, line=201, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x201', 'name is not "x201"')

    def test_walk_var_x202(self):
        node = utils.findNode(self.ast, line=202, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x202', 'name is not "x202"')

    def test_walk_var_x203(self):
        node = utils.findNode(self.ast, line=203, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x203', 'name is not "x203"')

    def test_walk_var_x204(self):
        node = utils.findNode(self.ast, line=204, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x204', 'name is not "x204"')

    def test_walk_var_x205(self):
        node = utils.findNode(self.ast, line=205, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x205', 'name is not "x205"')

    def test_walk_var_x206(self):
        node = utils.findNode(self.ast, line=206, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x206', 'name is not "x206"')

    def test_walk_var_x207(self):
        node = utils.findNode(self.ast, line=207, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x207', 'name is not "x207"')

    def test_walk_var_x208(self):
        node = utils.findNode(self.ast, line=208, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x208', 'name is not "x208"')

    def test_walk_var_x209(self):
        node = utils.findNode(self.ast, line=209, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x209', 'name is not "x209"')

    def test_walk_var_x210(self):
        node = utils.findNode(self.ast, line=210, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x210', 'name is not "x210"')

    def test_walk_var_x211(self):
        node = utils.findNode(self.ast, line=211, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x211', 'name is not "x211"')

    def test_walk_var_x212(self):
        node = utils.findNode(self.ast, line=212, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x212', 'name is not "x212"')

    def test_walk_var_x213(self):
        node = utils.findNode(self.ast, line=213, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x213', 'name is not "x213"')

    def test_walk_var_x214(self):
        node = utils.findNode(self.ast, line=214, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x214', 'name is not "x214"')

    def test_walk_var_x215(self):
        node = utils.findNode(self.ast, line=215, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x215', 'name is not "x215"')

    def test_walk_var_x216(self):
        node = utils.findNode(self.ast, line=216, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x216', 'name is not "x216"')

    def test_walk_var_x217(self):
        node = utils.findNode(self.ast, line=217, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x217', 'name is not "x217"')

    def test_walk_var_x218(self):
        node = utils.findNode(self.ast, line=218, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x218', 'name is not "x218"')

    def test_walk_var_x219(self):
        node = utils.findNode(self.ast, line=219, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x219', 'name is not "x219"')

    def test_walk_var_x220(self):
        node = utils.findNode(self.ast, line=220, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x220', 'name is not "x220"')

    def test_walk_var_x221(self):
        node = utils.findNode(self.ast, line=221, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x221', 'name is not "x221"')

    def test_walk_var_x222(self):
        node = utils.findNode(self.ast, line=222, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x222', 'name is not "x222"')

    def test_walk_var_x223(self):
        node = utils.findNode(self.ast, line=223, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x223', 'name is not "x223"')

    def test_walk_var_x224(self):
        node = utils.findNode(self.ast, line=224, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x224', 'name is not "x224"')

    def test_walk_var_x225(self):
        node = utils.findNode(self.ast, line=225, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x225', 'name is not "x225"')

class TestBoolop01(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/boolop01.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        type2 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=7, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        type2 = LiteralSema(float)
        type3 = LiteralValueSema('abc')
        self.assertTrue(len(nodeType) == 3 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_z(self):
        node = utils.findNode(self.ast, line=9, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(bool)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestBoolop02(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/boolop02.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=5, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(bool)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestBuiltin01(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin01.py')
        
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
    
    ast, defects = tirpan.run('tests/builtin02.py')
        
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
    
    ast, defects = tirpan.run('tests/builtin03.py')
        
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

class TestBuiltin04(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin04.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [set()]
        for elem in os.listdir('tests/import03'):
            type1.elems.append({LiteralValueSema(elem)})
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestBuiltin05(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin05.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=13, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        types = set()
        for x, y, z in os.walk(tests.const.DIR_FOR_BUILTIN05):
            types.add(LiteralValueSema(x))
        self.assertTrue(len(nodeType) == len(types) and
                        all(any(atype == elem for elem in nodeType)
                            for atype in types),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=14, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        types = set()
        for x, y, z in os.walk(tests.const.DIR_FOR_BUILTIN05):
            childType = ListSema()
            childType.elems = [set()]
            for elem in y:
                childType.elems.append({LiteralValueSema(elem)})
            childType.freeze()
            types.add(childType)
        self.assertTrue(len(nodeType) == len(types) and
                        all(any(atype == elem for elem in nodeType)
                            for atype in types),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_z(self):
        node = utils.findNode(self.ast, line=15, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        types = set()
        for x, y, z in os.walk(tests.const.DIR_FOR_BUILTIN05):
            childType = ListSema()
            childType.elems = [set()]
            for elem in z:
                childType.elems.append({LiteralValueSema(elem)})
            childType.freeze()
            types.add(childType)
        self.assertTrue(len(nodeType) == len(types) and
                        all(any(atype == elem for elem in nodeType)
                            for atype in types),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestBuiltin06(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin06.py')
        
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
    
    ast, defects = tirpan.run('tests/builtin07.py')
        
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
    
    ast, defects = tirpan.run('tests/builtin08.py')
        
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

    def test_y(self):
        node = utils.findNode(self.ast, line=6, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(tests.const.PLUGINS_DIR)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestBuiltin09(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin09.py')
        
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

    def test_y(self):
        node = utils.findNode(self.ast, line=5, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(tests.const.PLUGINS_DIR)
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
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestBuiltin10(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin10.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        pymod = re.compile(r"^(.*)\.py$")
        match = pymod.match(tests.const.WEBSTUFF_PYTHON_FN)
        type1 = LiteralValueSema(match.groups()[0])
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
        type1 = ListSema()
        type1.elems  = [{LiteralValueSema(tests.const.WEBSTUFF_PYTHON_DR)}]
        type1.elems += [{LiteralValueSema(os.path.abspath('tests'))}]
        for elem in sys.path[1:]:
            type1.elems.append({LiteralValueSema(elem)})
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestBuiltin11(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin11.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=46, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestBuiltin12(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin12.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=48, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralValueSema(tests.const.REPORT_KEY)}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestBuiltin13(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin13.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(tests.const.USER_HOME)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=6, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(tests.const.USER_PLUGINS)
        self.assertTrue(any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestBuiltin14(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin14.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(tests.const.CONST_PYTHON_FN)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestBuiltin16(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin16.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=7, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(_('Progress Information'))
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestBuiltin17(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin17.py')

    def test_foo(self):
        node = utils.findNode(self.ast, line=3, kind=ast.FunctionDef)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, FunctionDefinitionTGNode),
                        'type is not a function definition')
        nodeType = freezeSet(node.link.nodeType)
        isFunction = lambda x: (isinstance(x, FunctionSema) and
                                len(x.origin.templates.keys()) == 1)
        self.assertTrue(len(nodeType) == 1 and
                        any(isFunction(elem) for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'foo', 'name is not "foo"')

class TestBuiltin18(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin18.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(platform.system())
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestBuiltin19(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin19.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=15, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestBuiltin20(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin20.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=16, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems[0].add(LiteralSema(int))
        type1.elems[0].add(LiteralSema(float))
        type1.elems[0].add(LiteralValueSema('abc'))
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestBuiltin21(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin21.py')
        
    def test_y(self):
        node = utils.findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems[0].add(LiteralSema(int))
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestBuiltin22(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin22.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = ListSema()
        childType1.elems[0].add(LiteralSema(float))
        childType1.freeze()
        childType2 = ListSema()
        childType2.elems[0].add(LiteralValueSema(u'abc'))
        childType2.freeze()
        type1 = DictSema()
        type1.elems[LiteralValueSema(1    )] = {childType1}
        type1.elems[LiteralValueSema('abc')] = {childType2}
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestBuiltin23(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin23.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=14, kind=ast.Name)
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

class TestBuiltin24(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/builtin24.py')
        
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

class TestFunc01(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/func01.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=5, col=5, kind=ast.Name)
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
    
    ast, defects = tirpan.run('tests/func02.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=17, col=5, kind=ast.Name)
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
        type3 = LiteralValueSema(1)
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
    
    ast, defects = tirpan.run('tests/func03.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=19, col=5, kind=ast.Name)
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
        type3 = LiteralValueSema(1)
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
    
    ast, defects = tirpan.run('tests/func04.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=7, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(long)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestFunc05(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/func05.py')
        
    def test_u(self):
        node = utils.findNode(self.ast, line=34, col=1, kind=ast.Name)
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
        type3 = LiteralValueSema(1)
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
    
    ast, defects = tirpan.run('tests/func06.py')
        
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
    
    ast, defects = tirpan.run('tests/func07.py')
        
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
    
    ast, defects = tirpan.run('tests/func08.py')
        
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
    
    ast, defects = tirpan.run('tests/func09.py')
        
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
    
    ast, defects = tirpan.run('tests/func10.py')
        
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
    
    ast, defects = tirpan.run('tests/func11.py')

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

class TestFunc12(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/func12.py')

    def test_foo(self):
        node = utils.findNode(self.ast, line=1, kind=ast.FunctionDef)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, FunctionDefinitionTGNode),
                        'type is not a function definition')
        nodeType = freezeSet(node.link.nodeType)
        isFunction = lambda x: (isinstance(x, FunctionSema) and
                                len(x.origin.templates.keys()) == 1)
        self.assertTrue(len(nodeType) == 1 and
                        any(isFunction(elem) for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'foo', 'name is not "foo"')

    def test_x(self):
        node = utils.findNode(self.ast, line=9, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(long)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=10, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(long)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestFunc13(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/func13.py')
        
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
    
    ast, defects = tirpan.run('tests/func14.py')
        
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
    
    ast, defects = tirpan.run('tests/func15.py')
        
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
    
    ast, defects = tirpan.run('tests/func16.py')
        
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

class TestFunc17(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/func17.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=11, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(True)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestFunc18(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/func18.py')
        
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

class TestFunc19(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/func19.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=12, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        isGood = lambda x: (isinstance(x, FunctionSema) and
                            len(x.origin.templates) == 1)
        self.assertTrue(len(nodeType) == 1 and
                        any(isGood(elem) for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestFunc20(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/func20.py')
        
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

class TestFunc21(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/func21.py')
        
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

class TestFunc22(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/func22.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=19, kind=ast.Name)
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

class TestFunc23(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/func23.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=11, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = LiteralValueSema(1)
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
    
    ast, defects = tirpan.run('tests/global01.py')
        
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
    
    ast, defects = tirpan.run('tests/global02.py')
        
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
    
    ast, defects = tirpan.run('tests/global03.py')
        
    def test_res1(self):
        node = utils.findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
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
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'res2', 'name is not "res2"')

class TestGlobal04(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/global04.py')
        
    def test_res(self):
        node = utils.findNode(self.ast, line=9, col=5, kind=ast.Name)
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

class TestImport01(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/import01_1.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=6, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems  = [set()] + [{LiteralValueSema(1)}]
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
    
    ast, defects = tirpan.run('tests/import02.py')
        
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
    
    ast, defects = tirpan.run('tests/import03_1.py')
        
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
    
    ast, defects = tirpan.run('tests/import03_2.py')
        
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
    
    ast, defects = tirpan.run('tests/import03_3.py')
        
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
    
    ast, defects = tirpan.run('tests/import04_1.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralValueSema(1)
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

class TestImport05(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/import05_1.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=15, col=1, kind=ast.Name)
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

class TestImport06(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/import06_1.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=4, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestImport07(unittest.TestCase):
   
    ast, defects = tirpan.run('tests/import07_1.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=3, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestImport08(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/import08_1.py')
        
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

class TestMisc01(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc01.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=131, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(8)
        type2 = LiteralSema(int)
        type3 = LiteralSema(long)
        self.assertTrue(len(nodeType) == 3 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=132, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(long)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestMisc02(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc02.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=47, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc03(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc03.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=16, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc04(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc04.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=7, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc05(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc05.py')
        
    def test_d(self):
        node = utils.findNode(self.ast, line=16, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'd', 'name is not "d"')

class TestMisc06(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc06.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=59, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc07(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc07.py')
        
    def test_b(self):
        node = utils.findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

class TestMisc08(unittest.TestCase):

    MAX_SECONDS_LIMIT = 10
   
    startTime = datetime.datetime.now()
    ast, defects = tirpan.run('tests/misc08.py')
    endTime   = datetime.datetime.now()

    delta = endTime - startTime
        
    def test_time(self):
        self.assertTrue(self.delta.seconds < self.MAX_SECONDS_LIMIT,
                        'tirpan has exceeded its time limit')

class TestMisc09(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc09.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralSema(float)}, {LiteralSema(int)}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc10(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc10.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=31, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc11(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc11.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc12(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc12.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc13(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc13.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(tests.const.ROOT_DIR)
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
        type1 = LiteralValueSema(tests.const.PLUGINS_DIR)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestMisc14(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc14.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=14, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = LiteralSema(int)
        childType2 = LiteralSema(float)
        type1 = ListSema()
        type1.elems = [{childType1, childType2}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=16, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = LiteralSema(int)
        type1 = ListSema()
        type1.elems = [{childType1}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestMisc15(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc15.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=14, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = LiteralSema(int)
        childType2 = LiteralSema(float)
        type1 = ListSema()
        type1.elems = [{childType1, childType2}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=16, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = LiteralSema(int)
        type1 = ListSema()
        type1.elems = [{childType1}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestMisc16(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc16.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=17, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        childType1 = LiteralSema(int)
        childType2 = LiteralSema(float)
        type1 = ListSema()
        type1.elems = [{childType1, childType2}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=19, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestMisc17(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc17.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=7, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        type2 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc18(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc18.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        type2 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc19_1(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc19.py')
        
    def test_defects(self):
        self.assertEqual(len(self.defects), 1,
                         'there must be a defect')

class TestMisc19_2(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc19.py', orak_conf = noattr_conf)
        
    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc20(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc20.py')
        
    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc21(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc21.py')
        
    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc22(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc22.py')
        
    def test_defects(self):
        self.assertEqual(len(self.defects), 1,
                         'there must be a defect')

class TestMisc23(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc23.py')
        
    def test_defects(self):
        self.assertEqual(len(self.defects), 2,
                         'there must be exactly 2 defects')

class TestMisc24(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc24.py')
        
    def test_defects(self):
        self.assertEqual(len(self.defects), 3,
                         'there must be exactly 3 defects')

class TestMisc25(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc25.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=5, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc26(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc26.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=22, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems[0].add(LiteralValueSema(u'docgen.gpr.py'))
        type1.elems[0].add(LiteralValueSema(u'fanchartview.gpr.py'))
        type1.elems[0].add(LiteralValueSema(u'webstuff.gpr.py'))
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestMisc27(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc27.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=60, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems[0].add(LiteralValueSema(tests.const.WEBSTUFF_PLUGIN_ID))
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestMisc29(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc29.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=61, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems[0].add(LiteralValueSema(tests.const.WEBSTUFF_PLUGIN_ID))
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestMisc30(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc30.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=5, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc31(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc31.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=5, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems += [{LiteralValueSema(tests.const.PATH_FOR_BUILTIN08)}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestMisc32(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc32.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=28, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc33(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc33.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=25, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc34(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc34_1.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=31, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralValueSema(0)}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=32, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralValueSema('report')}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestMisc35(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc35.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=13, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc36(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc36.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=1105, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems[0].add(LiteralSema(types.NoneType))
        type1.elems[0].add(LiteralSema(float))
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=1107, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        self.assertTrue(len(nodeType) == 1,
                        'wrong types calculated')
        type1 = list(nodeType)[0]
        isPlugin = lambda x: (isinstance(x, InstanceSema) and
                              x.stub.origin.name == 'DocGenPlugin')
        self.assertTrue(isinstance(type1, ListSema) and
                        len(type1.elems)    == 1    and
                        len(type1.elems[0]) == 10   and
                        all(isPlugin(elem) for elem in type1.elems[0]),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_reg_plugins(self):
        node = utils.findNode(self.ast, line=926, kind=ast.FunctionDef)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, FunctionDefinitionTGNode),
                        'type is not a function definition')
        nodeType = freezeSet(node.link.nodeType)
        def isFunction(x):
            if not isinstance(x, FunctionSema):
                return False
            templates = x.origin.templates.keys()
            if len(templates) != 1:
                return False
            flag = templates[0][0][0][-1]
            return (isinstance(flag, LiteralValueSema) and
                    flag.value == True)
        self.assertTrue(len(nodeType) == 1 and
                        any(isFunction(elem) for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'reg_plugins',
                         'name is not "reg_plugins"')

class TestMisc37(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc37.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc38(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc38.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=6, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc39(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc39_1.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=30, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

    def test_b(self):
        node = utils.findNode(self.ast, line=31, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(False)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

class TestMisc40(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc40.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=57, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc41(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc41.py')
        
    def test_defects(self):
        self.assertEqual(len(self.defects), 2,
                         'there must be exactly 2 defects')

class TestMisc43(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc43.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=16, kind=ast.Name)
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
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestMisc44(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc44.py')

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc46(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc46.py')

    def test_defects(self):
        self.assertEqual(len(self.defects), 1,
                         'there must be a defect')

class TestMisc47(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc47.py')

    def test_defects(self):
        self.assertEqual(len(self.defects), 1,
                         'there must be a defect')

class TestMisc48(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc48.py')

    def test_defects(self):
        self.assertEqual(len(self.defects), 1,
                         'there must be a defect')

class TestMisc49(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc49.py')

    def test_defects(self):
        self.assertEqual(len(self.defects), 1,
                         'there must be a defect')

class TestMisc50(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc50.py')

    def test_defects(self):
        self.assertEqual(len(self.defects), 1,
                         'there must be a defect')

class TestMisc51(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc51.py')

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc52(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc52.py')
        
    def test_defects(self):
        self.assertEqual(len(self.defects), 2,
                         'there must be exactly 2 defects')

class TestMisc53(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc53.py')

    def test_defects(self):
        self.assertEqual(len(self.defects), 1,
                         'there must be a defect')

class TestMisc54(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc54.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=7, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'a', 'name is not "a"')

class TestMisc55(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc55.py', orak_conf = noattr_conf)

    def test_defects(self):
        self.assertEqual(len(self.defects), 1,
                         'there must be a defect')

class TestMisc56(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc56.py', orak_conf = noattr_conf)

    def test_defects(self):
        self.assertEqual(len(self.defects), 1,
                         'there must be a defect')

class TestMisc57(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc57.py', orak_conf = noattr_conf)

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc58(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc58.py', orak_conf = noattr_conf)

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc59(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc59.py', orak_conf = noattr_conf)

    def test_defects(self):
        self.assertEqual(len(self.defects), 1,
                         'there must be a defect')

class TestMisc60(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc60.py', orak_conf = noattr_conf)

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc62(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc62.py', orak_conf = noattr_conf)

    def test_x(self):
        node = utils.findNode(self.ast, line=3, kind=ast.Name)
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
        node = utils.findNode(self.ast, line=5, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc63(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc63.py', orak_conf = noattr_conf)

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc64(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc64.py', orak_conf = noattr_conf)

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc65(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc65.py', orak_conf = noattr_conf)

    def test_x(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(str)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(unicode)
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
        type1 = LiteralSema(unicode)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

    def test_t(self):
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(unicode)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 't', 'name is not "t"')

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc66(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc66.py', orak_conf = noattr_conf)

    def test_x(self):
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
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc67(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc67.py', orak_conf = noattr_conf)

    def test_x(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema('abc'.lower())
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema('abc'.upper())
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc68(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc68.py', orak_conf = noattr_conf)

    def test_x(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(str)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(unicode)
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
        type1 = LiteralSema(unicode)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

    def test_t(self):
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(unicode)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 't', 'name is not "t"')

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc69(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc69.py', orak_conf = noattr_conf)

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestMisc70(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/misc70.py', orak_conf = noattr_conf)

    def test_x(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(bool)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(bool)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_defects(self):
        self.assertEqual(len(self.defects), 0,
                         'there must be no defects')

class TestObject01(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/object01.py')
        
    def test_B_x(self):
        node = utils.findNode(self.ast, line=16, kind=ast.Attribute)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, AttributeTGNode),
                        'type is not an attribute')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')

    def test_b_x(self):
        node = utils.findNode(self.ast, line=17, kind=ast.Attribute)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, AttributeTGNode),
                        'type is not an attribute')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')

    def test_B_y(self):
        node = utils.findNode(self.ast, line=18, kind=ast.Attribute)
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
        node = utils.findNode(self.ast, line=19, kind=ast.Attribute)
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
        node = utils.findNode(self.ast, line=20, kind=ast.Attribute)
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
        node = utils.findNode(self.ast, line=23, kind=ast.Name)
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
    
    ast, defects = tirpan.run('tests/object02.py')

    def test_b(self):
        node = utils.findNode(self.ast, line=9, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        type2 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'b', 'name is not "b"')

class TestObject03(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/object03.py')

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
    
    ast, defects = tirpan.run('tests/object04.py')

    def test_d1(self):
        node = utils.findNode(self.ast, line=19, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralValueSema(1)
        type3 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 3 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'd1', 'name is not "d1"')

    def test_d2(self):
        node = utils.findNode(self.ast, line=20, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralValueSema(1)
        type3 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 3 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'd2', 'name is not "d2"')

    def test_d3(self):
        node = utils.findNode(self.ast, line=21, col=1, kind=ast.Name)
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
    
    ast, defects = tirpan.run('tests/object05.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=16, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralValueSema(1)
        type3 = LiteralSema(float)
        self.assertTrue(len(nodeType) == 3 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestObject06(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/object06.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=17, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralValueSema(1)
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
    
    ast, defects = tirpan.run('tests/object07.py')

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
    
    ast, defects = tirpan.run('tests/object08.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=17, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestObject09(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/object09.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=10, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(types.NoneType)
        type2 = LiteralValueSema(1)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestObject10(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/object10.py')

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
    
    ast, defects = tirpan.run('tests/object11.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=15, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
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

class TestObject12(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/object12.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=14, kind=ast.Name)
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
        node = utils.findNode(self.ast, line=15, kind=ast.Name)
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

class TestObject13(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/object13.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=13, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(tests.const.X)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=15, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(tests.const.Y)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_z(self):
        node = utils.findNode(self.ast, line=17, kind=ast.Name)
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

class TestObject14(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/object14.py')

    def test_x(self):
        node = utils.findNode(self.ast, line=23, kind=ast.Name)
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
        node = utils.findNode(self.ast, line=26, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems = [{LiteralSema(float)}]
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestObject15(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/object15.py')

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

class TestStd01(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/std01.py')
        
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
    
    ast, defects = tirpan.run('tests/std02.py')
        
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
    
    ast, defects = tirpan.run('tests/std03.py')
        
    def test_True(self):
        node = utils.findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(1)
        type2 = LiteralValueSema(True)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'True', 'name is not "True"')

    def test_False(self):
        node = utils.findNode(self.ast, line=6, kind=ast.Name)
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

class TestStd04(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/std04.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=42, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(8)
        type2 = LiteralSema(int)
        type3 = LiteralSema(long)
        self.assertTrue(len(nodeType) == 3 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType) and
                        any(type3 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_y(self):
        node = utils.findNode(self.ast, line=43, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralSema(int)
        type2 = LiteralSema(long)
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType) and
                        any(type2 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

class TestStd05(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/std05.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=6, col=1, kind=ast.Name)
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
        node = utils.findNode(self.ast, line=6, col=4, kind=ast.Name)
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
        node = utils.findNode(self.ast, line=8, col=1, kind=ast.Name)
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
    
    ast, defects = tirpan.run('tests/std06.py')
        
    def test_a(self):
        node = utils.findNode(self.ast, line=14, kind=ast.Name)
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
        node = utils.findNode(self.ast, line=15, kind=ast.Name)
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

class TestStd07(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/std07.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=50, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems[0].add(LiteralValueSema(tests.const.WEBSTUFF_PLUGIN_ID))
        type1.elems[0].add(LiteralValueSema(tests.const.FANCHART_PLUGIN_ID))
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestStd08(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/std08.py')
        
    def test_z(self):
        node = utils.findNode(self.ast, line=37, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(tests.const.WEBSTUFF_PLUGIN_ID)
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

class TestStd09(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/std09.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = ListSema()
        type1.elems[0].add(LiteralSema(int))
        type1.elems[0].add(LiteralSema(float))
        type1.elems[0].add(LiteralValueSema('abc'))
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestStd10(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/std10.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=5, kind=ast.Name)
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
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestStd11(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/std11.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=12, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema('abc')
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestStd12(unittest.TestCase):
    
    ast, defects = tirpan.run('tests/std12.py')
        
    def test_x(self):
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
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
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

class TestUnop01(unittest.TestCase):

    ast, defects = tirpan.run('tests/unop01.py')

    tBool    = LiteralSema(bool)
    tInt     = LiteralSema(int)
    tLong    = LiteralSema(long)
    tFloat   = LiteralSema(float)
    tComplex = LiteralSema(complex)
    tStr     = LiteralSema(str)
    tUnicode = LiteralSema(unicode)

    def test_walk_var_x01(self):
        node = utils.findNode(self.ast, line=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x01', 'name is not "x01"')

    def test_walk_var_x02(self):
        node = utils.findNode(self.ast, line=2, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x02', 'name is not "x02"')

    def test_walk_var_x03(self):
        node = utils.findNode(self.ast, line=3, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x03', 'name is not "x03"')

    def test_walk_var_x04(self):
        node = utils.findNode(self.ast, line=4, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x04', 'name is not "x04"')

    def test_walk_var_x05(self):
        node = utils.findNode(self.ast, line=5, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x05', 'name is not "x05"')

    def test_walk_var_x06(self):
        node = utils.findNode(self.ast, line=6, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = LiteralValueSema(-1)
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x06', 'name is not "x06"')

    def test_walk_var_x07(self):
        node = utils.findNode(self.ast, line=7, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 2 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x07', 'name is not "x07"')

    def test_walk_var_x08(self):
        node = utils.findNode(self.ast, line=8, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x08', 'name is not "x08"')

    def test_walk_var_x09(self):
        node = utils.findNode(self.ast, line=9, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tFloat
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x09', 'name is not "x09"')

    def test_walk_var_x10(self):
        node = utils.findNode(self.ast, line=10, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tComplex
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x10', 'name is not "x10"')

    def test_walk_var_x11(self):
        node = utils.findNode(self.ast, line=11, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x11', 'name is not "x11"')

    def test_walk_var_x12(self):
        node = utils.findNode(self.ast, line=12, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tInt
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x12', 'name is not "x12"')

    def test_walk_var_x13(self):
        node = utils.findNode(self.ast, line=13, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tLong
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x13', 'name is not "x13"')

    def test_walk_var_x14(self):
        node = utils.findNode(self.ast, line=14, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tBool
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x14', 'name is not "x14"')

    def test_walk_var_x15(self):
        node = utils.findNode(self.ast, line=15, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tBool
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x15', 'name is not "x15"')

    def test_walk_var_x16(self):
        node = utils.findNode(self.ast, line=16, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tBool
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x16', 'name is not "x16"')

    def test_walk_var_x17(self):
        node = utils.findNode(self.ast, line=17, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tBool
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x17', 'name is not "x17"')

    def test_walk_var_x18(self):
        node = utils.findNode(self.ast, line=18, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tBool
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x18', 'name is not "x18"')

    def test_walk_var_x19(self):
        node = utils.findNode(self.ast, line=19, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tBool
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x19', 'name is not "x19"')

    def test_walk_var_x20(self):
        node = utils.findNode(self.ast, line=20, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tBool
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x20', 'name is not "x20"')

    def test_walk_var_x21(self):
        node = utils.findNode(self.ast, line=21, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tBool
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x21', 'name is not "x21"')

    def test_walk_var_x22(self):
        node = utils.findNode(self.ast, line=22, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tBool
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x22', 'name is not "x22"')

    def test_walk_var_x23(self):
        node = utils.findNode(self.ast, line=23, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VariableTGNode),
                        'type is not a var')
        nodeType = freezeSet(node.link.nodeType)
        type1 = self.tBool
        type1.freeze()
        self.assertTrue(len(nodeType) == 1 and
                        any(type1 == elem for elem in nodeType),
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x23', 'name is not "x23"')

if __name__ == '__main__':
    unittest.main()
