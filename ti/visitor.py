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

    def __init__(self, filename, isGlobal = True):
        self.filename  = filename
        self.filtered  = None
        self.filtering = False
        self.getValue  = False
        self.leftPart  = False
        self.loseName  = False
        self.noFScope  = False
        self.isGlobal  = isGlobal

    def visit_Num(self, node):
        setLink(node, ti.tgnode.ConstTGNode(node, self.getValue))
    
    def visit_Str(self, node):
        setLink(node, ti.tgnode.ConstTGNode(node, True))
        
    def visit_Name(self, node):
        if node.id == 'None':
            link = ti.tgnode.ConstTGNode(node)
        else:
            if self.leftPart:
                try:
                    importer = config.data.importer
                    if self.noFScope:
                        fileScope = None
                    else:
                        fileScope = importer.getFileScope(node.fileno)
                except AttributeError:
                    fileScope = None
                loseName = self.loseName and self.isGlobal
                link = config.data.currentScope.findOrAddName(node.id,
                                                              True,
                                                              fileScope,
                                                              loseName)
            else:
                link = config.data.currentScope.findOrAddName(node.id)
        if self.getValue and link is not None:
            link.commonRetrieve('constants', EdgeType.isNotReverse) 
        setLink(node, link)
        if self.filtering:
            addSubvariable(link, EdgeType.ASSIGN_TRUE, True, self.filtered)
       
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
                saveLose = self.loseName
                if isinstance(ast_el, ast.Name):
                    self.loseName = True
                self.visit(ast_el)
                self.loseName = saveLose
            self.leftPart = save
            index = 0
            for ast_el in target.elts:
                getLink(node.value).addEdge(EdgeType.ASSIGN_ELEMENT,
                                            getLink(ast_el),
                                            index)
                index += 1
        else:
            saveLose = self.loseName
            if isinstance(target, ast.Name):
                self.loseName = True
            self.visit(target)
            self.loseName = saveLose
            self.leftPart = save
            getLink(node.value).addEdge(EdgeType.ASSIGN, getLink(target))
        setLink(node, getLink(node.value))

    def visit_AugAssign(self, node):
        self.visit(node.value)
        target = node.target
        save   = self.leftPart
        self.leftPart = True
        self.visit(target)
        self.leftPart = save
        var = self.visit_Op(node.op)
        link = ti.tgnode.FunctionCallTGNode(node, var)
        setLink(node, link)
        link.addEdge(EdgeType.ASSIGN, getLink(target))

    def visit_List(self, node):
        self.generic_visit(node)
        setLink(node, ti.tgnode.ListTGNode(node))

    def visit_common_subscript(self, collection, index):
        hasIndex = not isinstance(index, ast.Slice)
        link = ti.tgnode.SubscriptTGNode(hasIndex)
        if hasIndex:
            save = self.getValue
            self.getValue = True
            self.visit(index)
            self.getValue = save
            indexLink = getLink(index)
            link.addEdge(EdgeType.ASSIGN_INDEX, indexLink)
            indexLink.addEdge(EdgeType.ATTR_INDEX, link)
        else:
            self.visit(index)
            if index.lower:
                indexLowerLink = getLink(index.lower)
                link.addEdge(EdgeType.ASSIGN_SLICE, indexLowerLink, 0)
                indexLowerLink.addEdge(EdgeType.ATTR_SLICE, link)
            if index.upper:
                indexUpperLink = getLink(index.upper)
                link.addEdge(EdgeType.ASSIGN_SLICE, indexUpperLink, 1)
                indexUpperLink.addEdge(EdgeType.ATTR_SLICE, link)
            if index.step:
                indexStepLink  = getLink(index.step )
                link.addEdge(EdgeType.ASSIGN_SLICE, indexStepLink , 2)
                indexStepLink.addEdge(EdgeType.ATTR_SLICE , link)
        collectionLink = getLink(collection)
        link.addEdge(EdgeType.ASSIGN_OBJECT, collectionLink)
        collectionLink.addEdge(EdgeType.ATTR_OBJECT, link)
        return link
        
    def visit_Dict(self, node):
        setLink(node, ti.tgnode.DictTGNode())
        for number in range(len(node.keys)):
            key = node.keys  [number]
            val = node.values[number]
            self.visit(val)
            link = self.visit_common_subscript(node, key)
            getLink(val).addEdge(EdgeType.ASSIGN, link)
 
    def visit_Tuple(self, node):
        self.generic_visit(node)
        setLink(node, ti.tgnode.TupleTGNode(node))

    def visit_Import(self, node):
        importer = config.data.importer
        for alias in node.names:
            importer.importFile(self.filename, alias)

    def visit_ImportFrom(self, node):
        importer = config.data.importer
        importer.importFromFile(self.filename, node.module, node.names)

    def visit_Module(self, node):
        if not getLink(node).isInherited():
            nodeType = {ti.sema.LiteralValueSema(True)} 
            trueVariable = ti.tgnode.VariableTGNode('True', nodeType)
            config.data.currentScope.addVariable(trueVariable)

            nodeType = {ti.sema.LiteralValueSema(False)} 
            falseVariable = ti.tgnode.VariableTGNode('False', nodeType)
            config.data.currentScope.addVariable(falseVariable)

        self.generic_visit(node)

        if not getLink(node).isInherited():
           config.data.currentScope = config.data.currentScope.getParent()

    def visit_arguments(self, node, link, oldScope):
        nonDefs = len(node.args) - len(node.defaults)
        index = 0
        for param in node.args:
            self.visit(param)
            paramLink = getLink(param)
            defPos = index - nonDefs
            defVal = node.defaults[defPos] if defPos >= 0 else None
            if defVal:
                saveScope = config.data.currentScope
                saveLeft  = self.leftPart
                config.data.currentScope = oldScope
                self.leftPart = False
                self.visit(defVal)
                defValLink = getLink(defVal)
                self.leftPart = saveLeft
                config.data.currentScope = saveScope
                link.defaults[paramLink.name] = defValLink
            index += 1
            getLink(param).setNumber(index)

    def visit_FunctionDef(self, node):
        save = config.data.currentScope
        name = node.name
        link = ti.tgnode.UsualFunctionDefinitionTGNode(node, name, save, self)
        var  = save.findOrAddName(name)
        link.addEdge(EdgeType.ASSIGN, var)
        setLink(node, link)

    def visit_Call(self, node):
        saveFiltering = self.filtering
        self.filtering = False
        for arg in node.args:
            self.visit(arg)
        if node.starargs:
            self.visit(node.starargs)
        if node.kwargs:
            self.visit(node.kwargs)
        for pair in node.keywords:
            self.visit(pair.value)
        self.visit(node.func)
        setLink(node, ti.tgnode.FunctionCallTGNode(node))
        self.filtering = saveFiltering
        if self.filtering:
            obj_link = getLink(node.args[0])
            addSubvariable(obj_link, EdgeType.ASSIGN_LIST, True, self.filtered)

    def visit_common_iter(self, node):
        self.visit(node.iter)
        link = getLink(node.iter)
        var  = ti.tgnode.VariableTGNode(None)
        link.addEdge(EdgeType.ASSIGN_ELEMENT, var, None)
        var.addEdge(EdgeType.REV_ASSIGN_ELEMENT, link)
        return var

    def visit_common_target(self, var, target, ifs = None):
        save = self.leftPart
        self.leftPart = True
        if isinstance(target, ast.Tuple):
            saveNo = self.noFScope
            self.noFScope = True
            for elem in target.elts:
                self.visit(elem)
            self.noFScope = saveNo
            self.leftPart = save
            index = 0
            for elem in target.elts:
                var.addEdge(EdgeType.ASSIGN_ELEMENT, getLink(elem), index)
                index += 1
        else:
            saveNo = self.noFScope
            self.noFScope = True
            self.visit(target)
            self.noFScope = saveNo
            self.leftPart = save
            if ifs:
                test = checkComprehension(ifs, target)
                var.addEdge(EdgeType.ASSIGN_CUSTOM, getLink(target), test)
            else:
                var.addEdge(EdgeType.ASSIGN, getLink(target))

    def visit_For(self, node):
        scope = config.data.currentScope
        var   = self.visit_common_iter(node)
        args  = [QuasiNode(var)]
        func  = QuasiNode(ti.tgnode.ForFunctionDefinitionTGNode(node, scope))
        quasiCall = QuasiCall(func, args, node)
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
        setLink(node, ti.tgnode.FunctionCallTGNode(node, var))

    def visit_UnaryOp(self, node):
        self.visit(node.operand)
        var = self.visit_Op(node.op)
        setLink(node, ti.tgnode.FunctionCallTGNode(node, var))
        
    def visit_BoolOp(self, node):
        link = ti.tgnode.BooleanOperationTGNode(node.op)
        save = self.filtering
        for value in node.values:
            self.filtering = checkFilteringOperand(value)
            self.visit(value)
            getLink(value).addEdge(EdgeType.ASSIGN, link)
        self.filtering = save
        setLink(node, link)

    def visit_Compare(self, node):
        self.generic_visit(node)
        setLink(node, ti.tgnode.UnknownTGNode(node))

    def visit_common_ret(self, node):
        if node.value:
            self.visit(node.value)
            setLink(node, getLink(node.value))
        else:
            setLink(node, ti.tgnode.ConstTGNode(node))

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
        setLink(node, link)

    def visit_Attribute(self, node):
        save = self.leftPart
        self.leftPart = False
        collection = node.value
        self.visit(collection)
        link = ti.tgnode.AttributeTGNode(node.attr)
        collectionLink = getLink(collection) 
        link.addEdge(EdgeType.ASSIGN_OBJECT, collectionLink)
        collectionLink.addEdge(EdgeType.ATTR_OBJECT, link)
        setLink(node, link)
        self.leftPart = save

    def visit_Subscript(self, node):
        self.visit(node.value)
        index = getattr(node.slice, 'value', node.slice)
        setLink(node, self.visit_common_subscript(node.value, index))

    def visit_ListComp(self, node):
        for elem in node.generators:
            self.visit(elem)
        self.visit(node.elt)
        setLink(node, ti.tgnode.ListTGNode(node))

    def visit_IfExp(self, node):
        self.generic_visit(node)
        link = ti.tgnode.VariableTGNode(None)
        head = node.body
        tail = node.orelse
        getLink(head).addEdge(EdgeType.ASSIGN, link)
        getLink(tail).addEdge(EdgeType.ASSIGN, link)
        setLink(node, link)

    def visit_If(self, node):
        saveScope = config.data.currentScope
        condition = node.test
        save = self.filtering
        saveGlobal = self.isGlobal
        self.isGlobal  = False
        self.filtering = checkFilteringCondition(condition)
        saveFiltered   = self.filtered
        self.filtered  = filtered = {}
        self.visit(condition)
        self.filtered  = saveFiltered
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
        for link, edgeType in filtered.items():
            addSubvariable(link, edgeType, False)
        if not skipElse:
            for stmt in node.orelse:
                res = self.visit(stmt)
                if res == self.SKIP_NEXT:
                    break
        config.data.currentScope = saveScope
        self.isGlobal = saveGlobal

    def visit_GeneratorExp(self, node):
        self.generic_visit(node)
        setLink(node, ti.tgnode.ListTGNode(node))

    def visit_Global(self, node):
        config.data.currentScope.addGlobalNames(node.names)

    def visit_ClassDef(self, node):
        for base in node.bases:
            self.visit(base)
        name = node.name
        save = config.data.currentScope
        saveGlobal = self.isGlobal
        self.isGlobal = False
        link = ti.tgnode.ClassTGNode(name, node.bases, save)
        var  = save.findOrAddName(name)
        setLink(node, link)
        config.data.currentScope = link.getScope()
        basesVar  = ti.tgnode.VariableTGNode('__bases__')
        tupleNode = ti.tgnode.TupleTGNode(node)
        tupleNode.addEdge(EdgeType.ASSIGN, basesVar)
        config.data.currentScope.addVariable(basesVar)
        for stmt in node.body:
            self.visit(stmt)
        self.isGlobal = saveGlobal
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
        setLink(node, ti.tgnode.UnknownTGNode(node))

    def visit_comprehension(self, node):
        var = self.visit_common_iter(node)
        self.visit_common_target(var, node.target, node.ifs)

    def visit_TryExcept(self, node):
        filtered = set()
        save = config.data.currentScope
        saveGlobal = self.isGlobal
        self.isGlobal = False
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
        self.isGlobal = saveGlobal

    def visit_Break(self, node):
        return self.SKIP_NEXT

    def visit_Continue(self, node):
        return self.SKIP_NEXT

    def visit_While(self, node):
        self.visit(node.test)
        saveGlobal = self.isGlobal
        self.isGlobal = False
        for stmt in node.body:
            res = self.visit(stmt)
            if res == self.SKIP_NEXT:
                break
        for stmt in node.orelse:
            res = self.visit(stmt)
            if res == self.SKIP_NEXT:
                break
        self.isGlobal = saveGlobal
