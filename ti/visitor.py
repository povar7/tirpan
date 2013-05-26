'''
Created on 26.05.2013

@author: bronikkk
'''

import ast

import config
from   ti.tgnode import EdgeType
from   ti.tgnode import ConstTGNode, ListTGNode
from   utils     import checkEqual

class Visitor(ast.NodeVisitor):
    def __init__(self, fileName):
        self.fileName  = fileName
        self.leftPart  = False

    def visit_Num(self, node):
        node.link = ConstTGNode(node)
    
    def visit_Str(self, node):
        node.link = ConstTGNode(node)
        
    def visit_Name(self, node):
        if node.id == 'None':
            link = ConstTGNode(node)
        else:
            if self.leftPart:
                fileScope = config.globalScope
                #try:
                #    fileScope = importer.getFileScope(node.fileno)
                #except AttributeError:
                #    fileScope = None
                link = config.currentScope.findOrAddName(node.id, True, fileScope)
            else:
                link = config.currentScope.findOrAddName(node.id)
        node.link = link
       
    def visit_Assign(self, node):
        self.visit(node.value)
        target = node.targets[0]
        save   = self.leftPart
        self.leftPart = True
        if isinstance(target, ast.Tuple):
            for ast_el in target.elts:
                self.visit(ast_el)
            self.leftPart = save
            index = 0
            for ast_el in target.elts:
                node.value.link.addEdge(EdgeType.ASSIGN_ELEMENT, ast_el.link, index)
                index += 1
        else:
            self.visit(target)
            self.leftPart = save
            node.value.link.addEdge(EdgeType.ASSIGN, target.link)
        node.link = node.value.link

    def visit_AugAssign(self, node):
        pass

    def visit_List(self, node):
        self.generic_visit(node)
        node.link = ListTGNode(node)
        
    def visit_Dict(self, node):
        pass
    
    def visit_Tuple(self, node):
        pass

    def visit_Import(self, node):
        pass

    def visit_ImportFrom(self, node):
        pass

    def visit_Module(self, node):
        self.generic_visit(node)

    def visit_arguments(self, node):
        pass
           
    def visit_FunctionDef(self, node):
        pass

    def visit_Call(self, node):
        pass

    def visit_For(self, node):
        pass

    def visit_BinOp(self, node):
        pass

    def visit_UnaryOp(self, node):
        pass
        
    def visit_BoolOp(self, node):
        pass

    def visit_Compare(self, node):
        node.link = ConstTGNode(False)

    def visit_Return(self, node):
        pass

    def visit_Yield(self, node):
        pass

    def visit_Lambda(self, node):
        pass

    def visit_Attribute(self, node):
        pass

    def visit_Subscript(self, node):
        pass

    def visit_ListComp(self, node):
        pass

    def visit_IfExp(self, node):
        pass

    def visit_If(self, node):
        pass

    def visit_GeneratorExp(self, node):
        node.link = UnknownTGNode()

    def visit_Global(self, node):
        pass

    def visit_ClassDef(self, node):
        pass

    def visit_Print(self, node):
        pass

    def visit_Index(self, node):
        self.generic_visit(node)

    def visit_Slice(self, node):
        self.generic_visit(node)

    def visit_Set(self, node):
        node.link = UnknownTGNode()

    def visit_comprehension(self, node):
        pass

    def visit_TryExcept(self, node):
        pass
