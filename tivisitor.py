'''
Created on 03.01.2012

@author: ramil
'''

import ast

import __main__

from typegraph import *

class TIVisitor(ast.NodeVisitor):
    filename = None 

    def __init__(self, filename):
        self.filename = filename

    def visit(self, node):
        #print node
        super(TIVisitor, self).visit(node)

    def visit_Num(self, node):
        node.link = ConstTypeGraphNode(node.n)
    
    def visit_Str(self, node):
        node.link = ConstTypeGraphNode(node.s)

    def visit_True(self, node):
        node.link = ConstTypeGraphNode(True)

    def visit_False(self, node):
        node.link = ConstTypeGraphNode(False)

    def visit_None(self, node):
        node.link = ConstTypeGraphNode(None)
        
    def visit_Name(self, node):
        if node.id == 'True':
            self.visit_True(node)
        elif node.id == 'False':
            self.visit_False(node)
        elif node.id == 'None':
            self.visit_None(node)
        else:
            node.link = __main__.current_scope.find_or_add(node.id)
        
    def visit_Assign(self, node):
        target = node.targets[0]
        if target.__class__.__name__ == 'Tuple':
            self.visit(node.value)
            for ast_el in target.elts:
                self.visit(ast_el)
                node.value.link.addDependency(DependencyType.AssignElem, ast_el.link)                    
        else:
            self.generic_visit(node)
            node.value.link.addDependency(DependencyType.Assign, target.link)
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
        __main__.import_files(self.filename, node.names)

    def visit_Module(self, node):
        __main__.current_scope = node.link.get_scope()
        self.generic_visit(node)
        __main__.current_scope = __main__.current_scope.get_parent()
    def visit_For(self, node):
        self.generic_visit(node)
        node.iter.link.addDependency(DependencyType.AssignElem, node.target.link)

