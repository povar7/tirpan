'''
Created on 25.02.2012

@author: rahimsiz
'''
import unittest
from binops import *
from typegraph import *

class TestPlus(unittest.TestCase):


    def setUp(self):
        self.binop = BinOps()
        self.res = BinOpTypeGraphNode('add')

    def test_simple_int_add(self):
        op1 = ConstTypeGraphNode(1)
        op2 = ConstTypeGraphNode(2)
        self.binop.add(self.res, op1, op2)
        self.assertSetEqual(self.res.nodeType, set(['int']))
            
    def test_int_float_add(self):
        op1 = ConstTypeGraphNode(2.0)
        op2 = ConstTypeGraphNode(2)
        self.binop.add(self.res, op1, op2)
        self.assertSetEqual(self.res.nodeType, set(['float']))

    def test_str_add(self):
        op1 = ConstTypeGraphNode("test")
        op2 = ConstTypeGraphNode("t")
        self.binop.add(self.res, op1, op2)
        self.assertSetEqual(self.res.nodeType, set(['str']))
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()