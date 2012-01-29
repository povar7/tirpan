'''
Created on 03.01.2012

@author: ramil
'''

import ast

import __main__

from typegraph import *
from vardict   import VarDict

class TIVisitor(ast.NodeVisitor):
    varDict  = None
    filename = None 

    def __init__(self, filename):
        self.varDict = VarDict()
        self.filename = filename

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
        for target in node.targets:
            node.value.link.addDependency(target.link)
        node.link = node.value.link

    def visit_List(self,node):
        self.generic_visit(node)
        node.link = ListTypeGraphNode(node)
        
    def visit_Dict(self, node):
        self.generic_visit(node)
        node.link = DictTypeGraphNode(node)
    
    def visit_Tuple(self, node):
        self.generic_visit(node)
        node.link = TupleTypeGraphNode(node)

    def visit_Import(self, node):
        try:
            import_files = __main__.import_files
        except AttributeError:
            import tirpan
            import_files = tirpan.import_files
        import_files(self.filename, [alias.name for alias in node.names])
