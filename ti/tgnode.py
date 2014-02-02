'''
Created on 26.05.2013

@author: bronikkk
'''

import ast
import types

import config
import ti.lookup

from ti.formula import *
from ti.sema    import *
from utils      import *

classes = (CollectionSema, LiteralSema, ClassSema, InstanceSema, ModuleSema)

def addTypes(left, right):
    for key, value in right.items():
        if key not in left:
            left[key] = set()
        left[key] |= value

def replaceTypes(var, updates, stack):
    res = var.nodeType
    if stack:
        value  = {tuple(stack)}
        updict = dict()
        for elem in updates:
            try:
                cond = updates[elem]
            except TypeError:
                cond = set()
            updict[elem] = addCondition(value, cond)
        if isinstance(res, set):
            new_res = dict()
            value   = {Default(new_res)}
            for elem in res:
                new_res[elem] = value 
            res = new_res
        addTypes(res, updict)
    else:
        res = updates
    var.nodeType = res

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

class FunctionDefinitionTGNode(TGNode):

    def __init__(self, name, scope, defaults):
        super(FunctionDefinitionTGNode, self).__init__()

        self.scope     = FunctionSema(self, scope)
        self.nodeType  = {self.scope}

        self.name      = name
        self.parent    = scope
        self.templates = dict()

        self.params    = ScopeSema()
        self.listParam = None
        self.dictParam = None

        self.defaults    = defaults if defaults else dict()
        self.globalNames = set()

    def getAllParams(self):
        res = self.getOrdinaryParams()
        if self.listParam:
            res.append(self.listParam)
        if self.dictParam:
            res.append(self.dictParam)
        return res

    def getDefaults(self):
        return self.defaults

    def getDictParam(self):
        return self.dictParam

    def getListParam(self):
        return self.listParam

    def getOrdinaryParams(self):
        variables = self.params.variables.values() 
        unsorted = [var for var in variables if var.number]
        return sorted(unsorted, sortParams)

    def getParams(self):
        return self.params

    def getParent(self):
        return self.parent

    def getScope(self):
        return self.scope

    def getTemplates(self):
        return self.templates

    def hasDefaultReturn(self):
        return False

    def isDictParam(self, param):
        return param and param is self.dictParam

    def isListParam(self, param):
        return param and param is self.listParam

class UsualFunctionDefinitionTGNode(FunctionDefinitionTGNode):

    def __init__(self, node, name, scope):
        super(UsualFunctionDefinitionTGNode, self).__init__(name, scope, None)

        self.ast = node.body
        self.mir = None

        if node.args.vararg:
            self.listParam = VariableTGNode(node.args.vararg)

        if node.args.kwarg:
            self.dictParam = VariableTGNode(node.args.kwarg)

class ExternalFunctionDefinitionTGNode(FunctionDefinitionTGNode):

    def __init__(self, num, quasi, name, scope, defaults, listArgs, dictArgs):
        super(ExternalFunctionDefinitionTGNode, self).__init__(name,
                                                               scope,
                                                               defaults)

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
