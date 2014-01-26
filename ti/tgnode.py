'''
Created on 26.05.2013

@author: bronikkk
'''

import ast
import itertools
import types

import config
import ti.lookup

from ti.sema import *
from utils   import *

classes = (CollectionSema, LiteralSema, ClassSema, InstanceSema, ModuleSema)

bool_tuple = (False, True)

class Default(object):

    def __init__(self):
        self.data = None

def findDefault(value):
    for elem in value:
        if isinstance(elem, Default):
            return elem
    return None

def addTypes(left, right):
    for key, value in right.items():
        if key not in left:
            left[key] = set()
        left[key] |= value
    conds = getConditions(left)
    default = invertConditions(conds) 
    for value in left.values():
        obj = findDefault(value)
        if obj:
            obj.data = default

def calculateAtom(atom, mapping):
    if_node, flag = atom
    return mapping[if_node] == flag

def calculateAnd(conj, mapping):
    return all(calculateAtom(atom, mapping) for atom in conj)

def calculateCondition(cond, mapping):
    return any(calculateAnd(conj, mapping) for conj in cond)

def calculateConditions(conds, mapping):
    return not any(calculateCondition(cond, mapping) for cond in conds)

def getConditions(left):
    res = []
    for value in left.values():
        if not findDefault(value):
            res.append(value)
    return res

def getVariablesForConj(conj):
    res = set()
    for if_node, _ in conj:
        res.add(if_node)
    return res

def getVariablesForCond(cond):
    res = set()
    for conj in cond:
        res |= getVariablesForConj(conj)
    return res

def getVariablesForConds(conds):
    res = set()
    for cond in conds:
        res |= getVariablesForCond(cond)
    return tuple(res)

def invertConditions(conds):
    res = set()
    mapping = {}
    variables = getVariablesForConds(conds)
    number_of = len(variables)
    for elem_tuple in itertools.product(bool_tuple, repeat=number_of):
        index = 0
        for elem in elem_tuple:
            variable = variables[index]
            mapping[variable] = elem
            index += 1
        value = calculateConditions(conds, mapping)
        if not value:
            continue
        index = 0
        tmp_res = set()
        for elem in elem_tuple:
            variable = variables[index]
            tmp_res.add((variable, elem))
            index += 1
        res.add(tuple(tmp_res))
    return res

def replaceTypes(var, updates, stack):
    res = var.nodeType
    if stack:
        tmp   = tuple(stack)
        value = {tmp}
        dict_up = {elem : value for elem in updates}
        if isinstance(res, set):
            res = {elem : {Default()} for elem in res}
        addTypes(res, dict_up)
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
