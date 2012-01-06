'''
Created on 03.01.2012

@author: ramil
'''
import ast
from graph import *
from types_hierarchy import *
from var_dict import * 
class Visitor(ast.NodeVisitor):
    hierarchyGraph = None #Types hierarchy graphs
    graph = None # Graph of variables type
    dict = None
    def __init__(self, graph):
        self.graph = graph
        self.hierarchyGraph = HierarhyGraph()
        self.dict = VarDict()
    def visit(self, node):
        print node.__class__.__name__
        super(Visitor, self).visit(node)
    
    def visit_Num(self, node):
        node.link = TConst(self.hierarchyGraph, node.n)
        self.graph.append(node.link)
    
    def visit_Str(self, node):
        node.link = TConst(self.hierarchyGraph, node.s)
        self.graph.append(node.link)
        
    def visit_Name(self, node):
        graph_node = self.dict.find(node.id)
        if graph_node == None:
            graph_node = TVar(node.id)
            self.dict.append(node.id, graph_node)
            self.graph.append(graph_node)
        node.link = graph_node
        
    def visit_Assign(self, node):
        self.generic_visit(node)
        node.link = None
        if len(node.targets) == 1:
            node.value.link.addDependency(node.targets[0].link)
            node.link = node.value.link

    def visit_List(self,node):
        self.generic_visit(node)
        node.link = TList(self.hierarchyGraph, node)
        self.graph.append(node.link)
        
    def visit_Dict(self, node):
        self.generic_visit(node)
        node.link = TDict(self.hierarchyGraph, node)
        self.graph.append(node.link)
    
    def visit_Tuple(self, node):
        self.generic_visit(node)
        node.link = TList(self.hierarchyGraph, node)
        self.graph.append(node.link)