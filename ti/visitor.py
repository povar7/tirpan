'''
Created on 26.05.2013

@author: bronikkk
'''

import ast

import config
import ti.tgnode
import ti.sema

from ti.lookup import getOperatorName
from ti.tgnode import EdgeType
from ti.skips  import *
from utils     import *

class Visitor(ast.NodeVisitor):

    SKIP_NEXT = 'SKIP_NEXT'

    def __init__(self, filename):
        self.filename  = filename
        self.filtering = False
        self.leftPart  = False
        self.getValue  = False

    def visit_Num(self, node):
        node.link = ti.tgnode.ConstTGNode(node, self.getValue)
    
    def visit_Str(self, node):
        node.link = ti.tgnode.ConstTGNode(node, True)
        
    def visit_Name(self, node):
        if node.id == 'None':
            link = ti.tgnode.ConstTGNode(node)
        else:
            if self.leftPart:
                try:
                    importer  = config.data.importer
                    fileScope = importer.getFileScope(node.fileno)
                except AttributeError:
                    fileScope = None
                link = config.data.currentScope.findOrAddName(node.id,
                                                              True,
                                                              fileScope)
            else:
                link = config.data.currentScope.findOrAddName(node.id)
        if self.getValue and link is not None:
            link.commonRetrieve('constants', EdgeType.isNotReverse) 
        node.link = link
        if self.filtering:
            if link is not None:
                addSubvariable(link, EdgeType.ASSIGN_TRUE, True)
       
    def visit_Assign(self, node):
        saveValue = self.getValue
        if (isinstance(node.value, ast.Num) and
            isinstance(node.value.n, int)):
            self.getValue = True
        self.visit(node.value)
        self.getValue = saveValue
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
        self.visit(node.value)
        target = node.target
        save   = self.leftPart
        self.leftPart = True
        self.visit(target)
        self.leftPart = save
        var = self.visit_Op(node.op)
        node.link = ti.tgnode.FunctionCallTGNode(node, var)
        node.link.addEdge(EdgeType.ASSIGN, target.link)

    def visit_List(self, node):
        self.generic_visit(node)
        node.link = ti.tgnode.ListTGNode(node)

    def visit_common_subscript(self, collection, index):
        hasIndex = not isinstance(index, ast.Slice)
        link = ti.tgnode.SubscriptTGNode(hasIndex)
        link.addEdge(EdgeType.ASSIGN_OBJECT, collection.link)
        collection.link.addEdge(EdgeType.ATTR_OBJECT, link)
        if hasIndex:
            save = self.getValue
            self.getValue = True
            self.visit(index)
            self.getValue = save
            link.addEdge(EdgeType.ASSIGN_INDEX, index.link)
            index.link.addEdge(EdgeType.ATTR_INDEX, link)
        else:
            self.visit(index)
            if index.lower:
                link.addEdge(EdgeType.ASSIGN_SLICE, index.lower.link, 0)
                index.lower.link.addEdge(EdgeType.ATTR_SLICE, link)
            if index.upper:
                link.addEdge(EdgeType.ASSIGN_SLICE, index.upper.link, 1)
                index.upper.link.addEdge(EdgeType.ATTR_SLICE, link)
            if index.step:
                link.addEdge(EdgeType.ASSIGN_SLICE, index.upper.link, 2)
                index.step.link.addEdge(EdgeType.ATTR_SLICE, link)
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
        importer = config.data.importer
        for alias in node.names:
            importer.importFile(self.filename, alias)

    def visit_ImportFrom(self, node):
        importer = config.data.importer
        importer.importFromFile(self.filename, node.module, node.names)

    def visit_Module(self, node):
        if not node.link.isInherited():
            nodeType = {ti.sema.LiteralValueSema(True)} 
            trueVariable = ti.tgnode.VariableTGNode('True', nodeType)
            config.data.currentScope.addVariable(trueVariable)

            nodeType = {ti.sema.LiteralValueSema(False)} 
            falseVariable = ti.tgnode.VariableTGNode('False', nodeType)
            config.data.currentScope.addVariable(falseVariable)

        self.generic_visit(node)

        if not node.link.isInherited():
           config.data.currentScope = config.data.currentScope.getParent()

    def visit_arguments(self, node, link, oldScope):
        nonDefs = len(node.args) - len(node.defaults)
        index = 0
        for param in node.args:
            self.visit(param)
            defPos = index - nonDefs
            defVal = node.defaults[defPos] if defPos >= 0 else None
            if defVal:
                saveScope = config.data.currentScope
                saveLeft  = self.leftPart
                config.data.currentScope = oldScope
                self.leftPart = False
                self.visit(defVal)
                self.leftPart = saveLeft
                config.data.currentScope = saveScope
                link.defaults[param.link.name] = defVal.link
            index += 1
            param.link.setNumber(index)

    def visit_FunctionDef(self, node):
        save = config.data.currentScope
        name = node.name
        link = ti.tgnode.UsualFunctionDefinitionTGNode(node, name, save, self)
        var  = save.findOrAddName(name)
        link.addEdge(EdgeType.ASSIGN, var)
        node.link = link

    def visit_Call(self, node):
        for arg in node.args:
            self.visit(arg)
        if node.starargs:
            self.visit(node.starargs)
        if node.kwargs:
            self.visit(node.kwargs)
        for pair in node.keywords:
            self.visit(pair.value)
        self.visit(node.func)
        node.link = ti.tgnode.FunctionCallTGNode(node)

    def visit_common_iter(self, node):
        self.visit(node.iter)
        link = node.iter.link
        var  = ti.tgnode.VariableTGNode(None)
        link.addEdge(EdgeType.ASSIGN_ELEMENT, var, None)
        var.addEdge(EdgeType.REV_ASSIGN_ELEMENT, link)
        return var

    def visit_common_target(self, var, target, ifs = None):
        save = self.leftPart
        self.leftPart = True
        if isinstance(target, ast.Tuple):
            for elem in target.elts:
                self.visit(elem)
            self.leftPart = save
            index = 0
            for elem in target.elts:
                var.addEdge(EdgeType.ASSIGN_ELEMENT, elem.link, index)
                index += 1
        else:
            self.visit(target)
            self.leftPart = save
            if ifs:
                test = checkComprehension(ifs, target)
                var.addEdge(EdgeType.ASSIGN_CUSTOM, target.link, test)
            else:
                var.addEdge(EdgeType.ASSIGN, target.link)

    def visit_For(self, node):
        scope = config.data.currentScope
        var   = self.visit_common_iter(node)
        args  = [QuasiNode(var)]
        func  = QuasiNode(ti.tgnode.ForFunctionDefinitionTGNode(node, scope))
        quasiCall = QuasiCall(func, args)
        ti.tgnode.FunctionCallTGNode(quasiCall)

    def visit_Op(self, node):
        name = getOperatorName(node)
        return config.data.currentScope.findName(name)

    def visit_BinOp(self, node):
        save = self.getValue
        self.visit(node.left)
        if isinstance(node.op, ast.Mod):
            self.getValue = True
        self.visit(node.right)
        self.getValue = save
        var = self.visit_Op(node.op)
        node.link = ti.tgnode.FunctionCallTGNode(node, var)

    def visit_UnaryOp(self, node):
        self.visit(node.operand)
        var = self.visit_Op(node.op)
        node.link = ti.tgnode.FunctionCallTGNode(node, var)
        
    def visit_BoolOp(self, node):
        link = ti.tgnode.BooleanOperationTGNode(node.op)
        save = self.filtering
        for value in node.values:
            self.filtering = isinstance(value, ast.Name)
            self.visit(value)
            value.link.addEdge(EdgeType.ASSIGN, link)
        self.filtering = save
        node.link = link

    def visit_Compare(self, node):
        self.generic_visit(node)
        node.link = ti.tgnode.UnknownTGNode(node)

    def visit_common_ret(self, node):
        if node.value:
            self.visit(node.value)
            node.link = node.value.link
        else:
            node.link = ti.tgnode.ConstTGNode(node)

    def visit_Return(self, node):
        self.visit_common_ret(node)
        config.data.currentScope.connectReturn(node)
        return self.SKIP_NEXT

    def visit_Yield(self, node):
        self.visit_common_ret(node)
        config.data.currentScope.connectYield(node)
        return self.SKIP_NEXT

    def visit_Lambda(self, node):
        save = config.data.currentScope
        link = ti.tgnode.UsualFunctionDefinitionTGNode(node, None, save, self)
        node.link = link

    def visit_Attribute(self, node):
        save = self.leftPart
        self.leftPart = False
        collection = node.value
        self.visit(collection)
        link = ti.tgnode.AttributeTGNode(node.attr)
        link.addEdge(EdgeType.ASSIGN_OBJECT, collection.link)
        collection.link.addEdge(EdgeType.ATTR_OBJECT, link)
        node.link = link
        self.leftPart = save

    def visit_Subscript(self, node):
        self.visit(node.value)
        index = getattr(node.slice, 'value', node.slice)
        node.link = self.visit_common_subscript(node.value, index)

    def visit_ListComp(self, node):
        for elem in node.generators:
            self.visit(elem)
        self.visit(node.elt)
        node.link = ti.tgnode.ListTGNode(node)

    def visit_IfExp(self, node):
        node.link = ti.tgnode.UnknownTGNode(node)

    def visit_If(self, node):
        saveScope = config.data.currentScope
        condition = node.test
        save = self.filtering
        self.filtering = checkFilteringCondition(condition)
        self.visit(condition)
        self.filtering = save
        skipIf   = checkSkipIf  (condition)
        skipElse = checkSkipElse(condition)
        if not skipIf:
            for stmt in node.body:
                res = self.visit(stmt)
                if res == self.SKIP_NEXT:
                    if checkSkipAfterIf(condition):
                        return self.SKIP_NEXT
                    else:
                        break
        config.data.currentScope = saveScope
        if not skipElse:
            for stmt in node.orelse:
                res = self.visit(stmt)
                if res == self.SKIP_NEXT:
                    break

    def visit_GeneratorExp(self, node):
        self.generic_visit(node)
        node.link = ti.tgnode.UnknownTGNode(node)

    def visit_Global(self, node):
        config.data.currentScope.addGlobalNames(node.names)

    def visit_ClassDef(self, node):
        for base in node.bases:
            self.visit(base)
        name = node.name
        save = config.data.currentScope
        link = ti.tgnode.ClassTGNode(name, node.bases, save)
        var  = save.findOrAddName(name)
        node.link = link
        config.data.currentScope = link.getScope()
        basesVar  = ti.tgnode.VariableTGNode('__bases__')
        tupleNode = ti.tgnode.TupleTGNode(node)
        tupleNode.addEdge(EdgeType.ASSIGN, basesVar)
        config.data.currentScope.addVariable(basesVar)
        for stmt in node.body:
            self.visit(stmt)
        config.data.currentScope = save
        link.addEdge(EdgeType.ASSIGN, var)

    def visit_Print(self, node):
        for value in node.values:
            self.visit(value)

    def visit_Index(self, node):
        self.generic_visit(node)

    def visit_Slice(self, node):
        self.generic_visit(node)

    def visit_Set(self, node):
        self.generic_visit(node)
        node.link = ti.tgnode.UnknownTGNode(node)

    def visit_comprehension(self, node):
        var = self.visit_common_iter(node)
        self.visit_common_target(var, node.target, node.ifs)

    def visit_TryExcept(self, node):
        filtered = set()
        save = config.data.currentScope
        for stmt in node.body:
            res = self.visit(stmt)
            var = checkSkipNotIterable(stmt)
            if var is not None:
                filtered.add(var)
                addSubvariable(var, EdgeType.ASSIGN_ITER, True)
            if res == self.SKIP_NEXT:
                break
        config.data.currentScope = save
        for var in filtered:
            if var is not None:
                addSubvariable(var, EdgeType.ASSIGN_ITER, False)
        scope = config.data.currentScope
        for handler in node.handlers:
            if checkHandlerType(handler):
                config.data.currentScope = scope
            else:
                config.data.currentScope = save
            for stmt in handler.body:
                res = self.visit(stmt)
                if res == self.SKIP_NEXT:
                    break
        config.data.currentScope = save
        for stmt in node.orelse:
            res = self.visit(stmt)
            if res == self.SKIP_NEXT:
                break

    def visit_Break(self, node):
        return self.SKIP_NEXT

    def visit_Continue(self, node):
        return self.SKIP_NEXT
