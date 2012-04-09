'''
Created on 03.01.2012

@author: ramil
'''

import ast

import __main__

from init      import get_operator_name    
from typegraph import *

class TIVisitor(ast.NodeVisitor):
    filename = None 

    def __init__(self, filename):
        self.filename = filename

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
	    try:
                node.link.setPos(node)
            except AttributeError:
                pass
        
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

    def visit_List(self, node):
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

    def visit_ImportFrom(self, node):
        __main__.import_from_file(self.filename, node.module, node.names)

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
            arg.link.setParamNumber(i + 1)
            if defVal:
                self.visit(defVal)
                defVal.link.addDependency(DependencyType.Assign, arg.link)
                arg.link.setDefaultParam()
            
    def visit_FunctionDef(self, node):
        funcDefNode = UsualFuncDefTypeGraphNode(node, __main__.current_scope)
        node.link   = __main__.current_scope.findOrAdd(node.name)
        node.link.setPos(node)
        __main__.current_scope = funcDefNode.getParams()
        self.visit(node.args) 
        __main__.current_scope = __main__.current_scope.getParent()
        funcDefNode.addDependency(DependencyType.Assign, node.link)

    def visit_Call(self, node):
        for arg in node.args:
            self.visit(arg)
        for kwarg in node.keywords:
            self.visit(kwarg.value)

        if isinstance(node.func, ast.Name):
            name = node.func.id
            var = __main__.current_scope.find(name)
            node.link = FuncCallTypeGraphNode(node, var)
            node.link.processCall()
        else:
            node.link = UnknownTypeGraphNode(node);

    def visit_For(self, node):
        self.visit(node.iter)
        self.visit(node.target)
        node.iter.link.addDependency(DependencyType.AssignElem, node.target.link)
        for nn in node.body:
            self.visit(nn)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        name = get_operator_name(node.op.__class__)
        var = __main__.current_scope.find(name)
        node.link = FuncCallTypeGraphNode(node, var)
        node.link.processCall()

    def visit_UnaryOp(self, node):
        self.visit(node.operand)
        name = get_operator_name(node.op.__class__)
        var = __main__.current_scope.find(name)
        node.link = FuncCallTypeGraphNode(node, var)
        node.link.processCall()
        
    def visit_BoolOp(self, node):
        node.link = ConstTypeGraphNode(False)

    def visit_Compare(self, node):
        node.link = ConstTypeGraphNode(False)

    def visit_Return(self, node):
        self.generic_visit(node)
        if node.value is not None:
            __main__.current_res = \
            __main__.current_res.union(set([node.value.link]))

    def visit_Lambda(self, node):
        node.link = UnknownTypeGraphNode(node)

    def visit_Attribute(self, node):
        node.link = UnknownTypeGraphNode(node)

    def visit_Subscript(self, node): 
        self.generic_visit(node)
        node.link = TypeGraphNode()
        node.value.link.addDependency(DependencyType.AssignElem, node.link)

    def visit_ListComp(self, node):
        node.link = UnknownTypeGraphNode(node)

    def visit_IfExp(self, node):
        node.link = UnknownTypeGraphNode(node)

    def visit_GeneratorExp(self, node):
        node.link = UnknownTypeGraphNode(node)
