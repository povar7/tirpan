'''
Created on 03.01.2012

@author: ramil
'''

import ast

import __main__

from init      import get_operator_name 
from typegraph import *

class TIVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename  = filename
        self.left_part = False

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
            if self.left_part:
                file_scope = __main__.importer.get_ident(node.fileno).scope 
                link       = __main__.current_scope.findOrAdd(node.id, True, file_scope)
            else:
                link       = __main__.current_scope.findOrAdd(node.id)
            node.link = link
            try:
                node.link.setPos(node)
            except AttributeError:
                pass
        
    def visit_Assign(self, node):
        self.visit(node.value)
        target = node.targets[0]
        save   = self.left_part
        self.left_part = True
        if isinstance(target, ast.Tuple):
            for ast_el in target.elts:
                self.visit(ast_el)
            self.left_part = save
            for ast_el in target.elts:
                node.value.link.addDependency(DependencyType.AssignElem, ast_el.link)
        else:
            self.visit(target)
            self.left_part = save
            node.value.link.addDependency(DependencyType.Assign, target.link)
        node.link = node.value.link

    def visit_AugAssign(self, node):
        self.visit(node.value)
        target = node.target
        save   = self.left_part
        self.left_part = True
        self.visit(target)
        self.left_part = save
        name = get_operator_name(node.op.__class__)
        var = __main__.current_scope.find(name)
        node.link = FuncCallTypeGraphNode(node, var)
        node.link.processCall()
        node.link.addDependency(DependencyType.Assign, target.link)

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
        name = node.name
        funcDefNode = UsualFuncDefTypeGraphNode(node, name, __main__.current_scope)
        var  = __main__.current_scope.findOrAdd(name)
        var.setPos(node)
        node.link = funcDefNode
        __main__.current_scope = funcDefNode.getParams()
        self.visit(node.args) 
        __main__.current_scope = __main__.current_scope.getParent()
        funcDefNode.addDependency(DependencyType.Assign, var)

    def visit_Call(self, node):
        for arg in node.args:
            self.visit(arg)
        for kwarg in node.keywords:
            self.visit(kwarg.value)

        if isinstance(node.func, ast.Name):
            name = node.func.id
            var = __main__.current_scope.find(name)
            node.func.link = var
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
        __main__.current_res = __main__.current_res.union(set([node]))

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

    def visit_Global(self, node):
        __main__.current_scope.addGlobalNames(node.names)
