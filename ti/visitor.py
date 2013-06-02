'''
Created on 26.05.2013

@author: bronikkk
'''

import ast

import config
import ti.tgnode
import ti.sema

from ti.tgnode import EdgeType

class Visitor(ast.NodeVisitor):

    def __init__(self, filename):
        self.filename  = filename
        self.leftPart  = False

    def visit_Num(self, node):
        node.link = ti.tgnode.ConstTGNode(node)
    
    def visit_Str(self, node):
        node.link = ti.tgnode.ConstTGNode(node)
        
    def visit_Name(self, node):
        if node.id == 'None':
            link = ti.tgnode.ConstTGNode(node)
        else:
            if self.leftPart:
                fileScope = config.data.globalScope
                #try:
                #    fileScope = importer.getFileScope(node.fileno)
                #except AttributeError:
                #    fileScope = None
                link = config.data.currentScope.findOrAddName(node.id,
                                                              True,
                                                              fileScope)
            else:
                link = config.data.currentScope.findOrAddName(node.id)
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
                node.value.link.addEdge(EdgeType.ASSIGN_ELEMENT,
                                        ast_el.link,
                                        index)
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
        node.link = ti.tgnode.ListTGNode(node)

    def visit_common_subscript(self, collection, index):
        hasIndex = index is not None
        link = ti.tgnode.SubscriptTGNode(hasIndex)
        link.addEdge(EdgeType.ASSIGN_OBJECT, collection.link)
        collection.link.addEdge(EdgeType.ATTR_OBJECT, link)
        if hasIndex:
            self.visit(index) 
            link.addEdge(EdgeType.ASSIGN_SLICE, index.link)
            index.link.addEdge(EdgeType.ATTR_SLICE, link)
        return link
        
    def visit_Dict(self, node):
        node.link = ti.tgnode.DictTGNode()
        for number in range(len(node.keys)):
            key = node.keys  [number]
            val = node.values[number]
            self.visit(val)
            link = self.visit_common_subscript(node, key)
            val.link.addEdge(EdgeType.ASSIGN, link)
 
    def visit_Tuple(self, node):
        self.generic_visit(node)
        node.link = ti.tgnode.TupleTGNode(node)

    def visit_Import(self, node):
        pass

    def visit_ImportFrom(self, node):
        pass

    def visit_Module(self, node):
        nodeType = {ti.sema.LiteralValueSema(True)} 
        trueVariable = ti.tgnode.VariableTGNode('True', nodeType)
        config.data.currentScope.addVariable(trueVariable)

        nodeType = {ti.sema.LiteralValueSema(False)} 
        falseVariable = ti.tgnode.VariableTGNode('False', nodeType)
        config.data.currentScope.addVariable(falseVariable)

        self.generic_visit(node)

    def visit_arguments(self, node):
        pass
           
    def visit_FunctionDef(self, node):
        pass

    def visit_Call(self, node):
        pass

    def visit_common_in(self, node):
        self.visit(node.iter)
        link   = node.iter.link
        target = node.target
        save   = self.leftPart
        self.leftPart = True
        if isinstance(target, ast.Tuple):
            for elem in target.elts:
                self.visit(elem)
            self.leftPart = save
            index = 0
            for elem in target.elts:
                link.addEdge(EdgeType.ASSIGN_DOUBLE, elem.link, index)
                index += 1
        else:
            self.visit(target)
            self.leftPart = save
            link.addEdge(EdgeType.ASSIGN_ELEMENT, target.link, None)

    def visit_For(self, node):
        self.visit_common_in(node)
        for stmt in node.body:
            self.visit(stmt)

    def visit_BinOp(self, node):
        pass

    def visit_UnaryOp(self, node):
        pass
        
    def visit_BoolOp(self, node):
        pass

    def visit_Compare(self, node):
        node.link = ti.tgnode.ConstTGNode(False)

    def visit_Return(self, node):
        pass

    def visit_Yield(self, node):
        pass

    def visit_Lambda(self, node):
        pass

    def visit_Attribute(self, node):
        pass

    def visit_Subscript(self, node):
        self.visit(node.value)
        index = getattr(node.slice, 'value', None)
        node.link = self.visit_common_subscript(node.value, index)

    def visit_ListComp(self, node):
        pass

    def visit_IfExp(self, node):
        pass

    def visit_If(self, node):
        pass

    def visit_GeneratorExp(self, node):
        node.link = ti.tgnode.UnknownTGNode()

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
        node.link = ti.tgnode.UnknownTGNode()

    def visit_comprehension(self, node):
        pass

    def visit_TryExcept(self, node):
        pass
