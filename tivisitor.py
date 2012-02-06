'''
Created on 03.01.2012

@author: ramil
'''

import ast

import __main__

from typegraph    import *
from errorprinter import *

class TIVisitor(ast.NodeVisitor):
    filename = None 

    def __init__(self, filename):
        self.filename = filename

    def visit(self, node):
        print node
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
            node.link = __main__.current_scope.findOrAdd(node.id)
        
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
        __main__.current_scope = node.link.getScope()
        self.generic_visit(node)
        __main__.current_scope = __main__.current_scope.getParent()

    def visit_arguments(self, node):
        nonDefs = len(node.args) - len(node.defaults)
        for i in range(len(node.args)):
            arg    = node.args[i]
            defPos = i - nonDefs
            defVal = node.defaults[defPos] if defPos >= 0 else None
            self.visit(arg)
            if defVal:
                self.visit(defVal)
                defVal.link.addDependency(arg.link)
            
    def visit_FunctionDef(self, node):
        funcDefNode = FuncDefTypeGraphNode(node.body, __main__.current_scope)
        node.link   = __main__.current_scope.findOrAdd(node.name)
        funcDefNode.addDependency(node.link)
        node.link.addValue(funcDefNode)
        __main__.current_scope = funcDefNode.getParams()
        self.visit(node.args) 
        __main__.current_scope = __main__.current_scope.getParent()

    def visit_Call(self, node):
        node.link = CallTypeGraphNode()
        funcName  = node.func.id
        varNode   = __main__.current_scope.find(funcName)
        if not varNode:
            __main__.error_printer.printError(CallNotResolvedError(node, funcName))
            return
        funcsList = list(varNode.nodeValue)
        if len(funcsList) == 0:
            __main__.error_printer.printError(CallNotResolvedError(node, funcName))
            return

    def visit_For(self, node):
        self.generic_visit(node)
        node.iter.link.addDependency(DependencyType.AssignElem, node.target.link)
