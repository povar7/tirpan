'''
Created on 26.05.2013

@author: bronikkk
'''

import ast
import types

import config
import ti.lookup

from ti.sema import *
from utils   import *

classes = (CollectionSema, LiteralSema, ClassSema, InstanceSema, ModuleSema)

def updateSet(res, updates):
    res |= updates
    res.discard(None)

class EdgeType(object):
    @staticmethod
    def processAssign(left, right, *args):
        updateSet(right.nodeType, left.nodeType)

class TGNode(object):

    def __init__(self):
        self.nodeType = set()

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash((self.__class__, id(self)))

class ConstTGNode(TGNode):

    def __init__(self, node):
        super(ConstTGNode, self).__init__()

class VariableTGNode(TGNode):

    def __init__(self, name, nodeType = None):
        super(VariableTGNode, self).__init__()
        self.name   = name
        self.number = None

        if nodeType:
            self.nodeType = nodeType
        else:
            self.nodeType = set()

    def setNumber(self, number):
        self.number = number

class ListTGNode(TGNode):

    def __init__(self, node):
        super(ListTGNode, self).__init__()

class TupleTGNode(TGNode):

    def __init__(self, node):
        super(TupleTGNode, self).__init__()

class DictTGNode(TGNode):

    def __init__(self):
        super(DictTGNode, self).__init__()

class SetTGNode(TGNode):

    def __init__(self, node):
        super(SetTGNode, self).__init__()

class AttributeTGNode(TGNode):

    def __init__(self, attr):
        super(AttributeTGNode, self).__init__()

class SubscriptTGNode(TGNode):

    def __init__(self, hasIndex):
        super(SubscriptTGNode, self).__init__()

class FunctionDefinitionTGNode(TGNode):

    def __init__(self, name, scope, defaults):
        super(FunctionDefinitionTGNode, self).__init__()

        nodeType = FunctionSema(self, scope)
        self.nodeType  = {nodeType}

        self.name        = name
        self.parent      = scope
        self.templates   = dict()

        self.params      = ScopeSema()
        self.listParam   = None
        self.dictParam   = None

        self.defaults    = defaults if defaults else dict()
        self.globalNames = set()

    def isListParam(self, param):
        return param and param is self.listParam

    def isDictParam(self, param):
        return param and param is self.dictParam

    def getAllParams(self):
        res = self.getOrdinaryParams()
        if self.listParam:
            res.append(self.listParam)
        if self.dictParam:
            res.append(self.dictParam)
        return res

    def getOrdinaryParams(self):
        variables = self.params.variables.values() 
        unsorted = [var for var in variables if var.number]
        return sorted(unsorted, sortParams)

    def getListParam(self):
        return self.listParam

    def getDictParam(self):
        return self.dictParam

    def getParams(self):
        return self.params

    def getParent(self):
        return self.parent

    def getDefaults(self):
        return self.defaults

    def getTemplates(self):
        return self.templates

    def hasDefaultReturn(self):
        return False

class UsualFunctionDefinitionTGNode(FunctionDefinitionTGNode):

    def __init__(self, node, name, scope, visitor):
        super(UsualFunctionDefinitionTGNode, self).__init__(name, scope, None)

        if isinstance(node, ast.Lambda):
            self.ast = [node.body]
            self.defaultReturn = False
        else:
            self.ast = node.body
            self.defaultReturn = not self.checkReturns(self.ast)

        if node.args.vararg:
            self.listParam = VariableTGNode(node.args.vararg)

        if node.args.kwarg:
            self.dictParam = VariableTGNode(node.args.kwarg)

        save = config.data.currentScope
        config.data.currentScope = self.getParams()
        visitor.visit_arguments(node.args, self, save)
        config.data.currentScope = save

    def hasDefaultReturn(self):
        return self.defaultReturn

    @staticmethod
    def checkReturns(body):
        for stmt in body:
            if isinstance(stmt, ast.Return):
                return True
            elif isinstance(stmt, ast.If):
                if (UsualFunctionDefinitionTGNode.checkReturns(stmt.body) and
                    UsualFunctionDefinitionTGNode.checkReturns(stmt.orelse)):
                    return True
        return False

class ExternalFunctionDefinitionTGNode(FunctionDefinitionTGNode):

    def __init__(self, num, quasi, name, scope, defaults, listArgs, dictArgs):
        super(ExternalFunctionDefinitionTGNode, self).__init__(name,
                                                               scope,
                                                               defaults)

        self.calls = []
        self.quasi = quasi

        number = 0
        for index in range(num):
            number = index + 1
            param = VariableTGNode(str(number))
            param.setNumber(number)
            self.params.addVariable(param)

        if listArgs:
            number += 1
            self.listParam = VariableTGNode('args')
            self.listParam.setNumber(number)

        if dictArgs:
            number += 1
            self.dictParam = VariableTGNode('kwargs')
            self.dictParam.setNumber(number)

class FunctionCallTGNode(TGNode):

    def __init__(self, node, var = None):
        super(FunctionCallTGNode, self).__init__()
        self.node = node

        self._isLocked = True
        self._isLocked = False

        self.processCall()

    def getArgumentNodesNumber(self):
        return self.argsNum

    def isLocked(self):
        return self._isLocked

    def processCall(self):
        from ti.function import processFunc

        if self._isLocked:
            return
        functionNode     = self.getFunctionNode()
        oldArgumentNodes = []
        KWArgumentNodes  = self.getKWArgumentNodes()
        listArgumentNode = self.getListArgumentNode()
        if listArgumentNode:
            listArgumentTypes = []
            for oneType in listArgumentNode.nodeType:
                if isinstance(oneType, TupleSema):
                    listArgumentTypes.append(oneType.elems[1:])
        else:
            listArgumentTypes = [[]]
        for index in range(self.getArgumentNodesNumber()):
            oldArgumentNodes.append(self.getArgumentNode(index))
        for listArgumentType in listArgumentTypes:
            argumentNodes = oldArgumentNodes[:]
            for elem in listArgumentType:
                argumentNodes.append(None)
            processFunc(self, functionNode,
                        argumentNodes, KWArgumentNodes, listArgumentType)

class FunctionTemplateTGNode(TGNode):

    def __init__(self, params, function, inst, tgNode):
        super(FunctionTemplateTGNode, self).__init__()

        if isinstance(function, FunctionDefinitionTGNode):
            self.function = function
            self.parent   = function.getParent()
            self.scope    = TemplateSema(self)

            if not inst and self.function.hasDefaultReturn():
                self.nodeType.add(LiteralSema(types.NoneType))
        else:
            self.function = None
            self.parent   = None
            self.scope    = None

        if inst:
            self.nodeType.add(inst)

        self.mapping = dict()
        self.params  = params
        self.tgNode  = tgNode

    def getParams(self):
        return self.params

    def getParent(self):
        return self.parent

    def getScope(self):
        return self.scope

class ClassTGNode(TGNode):

    def __init__(self, name, scope):
        super(ClassTGNode, self).__init__()

        nodeType = ClassSema(self)
        self.nodeType = {nodeType}

        self.name   = name
        self.parent = scope
        self.scope  = nodeType
        self.body   = ScopeSema()

    def getBody(self):
        return self.body

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def getScope(self):
        return self.scope

class ModuleTGNode(TGNode):

    def __init__(self, name, parent, inheritedScope):
        super(ModuleTGNode, self).__init__()
        self.name = name

        if inheritedScope:
            self.body  = None
            self.scope = inheritedScope
            self.flag  = True
        else:
            self.body  = ScopeSema()
            self.scope = ModuleSema(self)
            self.flag  = False

        self.parent   = parent
        self.nodeType = {self.scope}

    def getBody(self):
        return self.body

    def getParent(self):
        return self.parent

    def getScope(self):
        return self.scope

    def isInherited(self):
        return self.flag

class UsualModuleTGNode(ModuleTGNode):

    def __init__(self, mir, ast, name, parentScope, inheritedScope = None):
        super(UsualModuleTGNode, self).__init__(name,
                                                parentScope,
                                                inheritedScope)
        self.ast = ast
        self.mir = mir

    def getAST(self):
        return self.ast

    def getMIR(self):
        return self.mir

class ExternalModuleTGNode(ModuleTGNode):

    def __init__(self, name, parentScope, asname = None):
        super(ExternalModuleTGNode, self).__init__(name, parentScope, None)
        self.asname = asname if asname else self.name
