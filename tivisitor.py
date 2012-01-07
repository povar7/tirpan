'''
Created on 03.01.2012

@author: ramil
'''

import ast

from typegraph import *
from vardict   import VarDict
 
class TIVisitor(ast.NodeVisitor):
    varDict = None

    def __init__(self):
        self.varDict   = VarDict()

    def visit_Num(self, node):
        node.link = ConstTypeGraphNode(node.n)
    
    def visit_Str(self, node):
        node.link = ConstTypeGraphNode(node.s)

    def visit_True(self, node):
        trueNode = ConstTypeGraphNode(True)
        trueNode.addDependency(node.link)

    def visit_False(self, node):
        falseNode = ConstTypeGraphNode(False)
        falseNode.addDependency(node.link)

    def visit_None(self, node):
        noneNode = ConstTypeGraphNode(None)
        noneNode.addDependency(node.link) 
        
    def visit_Name(self, node):
        varNode = self.varDict.find(node.id)
        if not varNode:
            varNode = VarTypeGraphNode(node.id)
            self.varDict.add(node.id, varNode)
        node.link = varNode
        if node.id == 'True':
            self.visit_True(node)
        elif node.id == 'False':
            self.visit_False(node)
        elif node.id == 'None':
            self.visit_None(node)
        
    def visit_Assign(self, node):
        self.generic_visit(node)
        node.link = AssignTypeGraphNode(node)

    def visit_List(self,node):
        self.generic_visit(node)
        node.link = ListTypeGraphNode(node)
        
    def visit_Dict(self, node):
        self.generic_visit(node)
        node.link = DictTypeGraphNode(node)
    
    def visit_Tuple(self, node):
        self.generic_visit(node)
        node.link = TupleTypeGraphNode(node)
