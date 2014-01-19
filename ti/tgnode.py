'''
Created on 26.05.2013

@author: bronikkk
'''

import ast
import copy
import os
import types
import itertools

import config
import ti.lookup

from ti.sema import *
from utils   import *

classes = (CollectionSema, LiteralSema, ClassSema, InstanceSema, ModuleSema)

def updateSet(res, updates):
    res |= updates
    res.discard(None)

class EdgeType(object):

    ARGUMENT           = 'Argument'
    ASSIGN             = 'Assign'
    ASSIGN_ELEMENT     = 'AssignElement'
    ASSIGN_YIELD       = 'AssignYield'
    ATTR_INDEX         = 'AttrIndex'
    ATTR_SLICE         = 'AttrSlice'
    ATTR_OBJECT        = 'AttrObject'
    ELEMENT            = 'Element'
    FUNC               = 'Func'
    KWARGUMENT         = 'KWArgument'
    LISTARGUMENT       = 'ListArgument'

    @staticmethod
    def updateRight(right, types):
        if len(types - right.nodeType) > 0:
            length = len(right.nodeType)
            updateSet(right.nodeType, types)
            if len(right.nodeType) > length:
                right.process()
                right.walkEdges()

    @staticmethod
    def processArgument(left, right, *args):
        length = len(right.nodeType)
        right.processCall()
        if len(right.nodeType) > length:
            right.walkEdges()

    @staticmethod
    def processAssign(left, right, *args):
        EdgeType.updateRight(right, left.nodeType)

    @staticmethod
    def processAssignElement(left, right, *args):
        index = args[0]
        types = left.getElementsTypes(index)
        EdgeType.updateRight(right, types)

    @staticmethod
    def processAssignIndex(left, right, *args):
        pass

    @staticmethod
    def processAssignObject(left, right, *args):
        pass

    @staticmethod
    def processAssignSlice(left, right, *args):
        pass

    @staticmethod
    def processAssignYield(left, right, *args):
        listType = ListSema(0)
        updateSet(listType.elems[0], left.nodeType)
        types = {listType}
        EdgeType.updateRight(right, types)

    @staticmethod
    def processAttrIndex(left, right, *args):
        EdgeType.processCommon(left, right, args)

    @staticmethod
    def processAttrObject(left, right, *args):
        EdgeType.processCommon(left, right, args)

    @staticmethod
    def processAttrSlice(left, right, *args):
        EdgeType.processCommon(left, right, args)

    @staticmethod
    def processCommon(left, right, *args):
        length = len(right.nodeType)
        right.process()
        if len(right.nodeType) > length:
            right.walkEdges()

    @staticmethod
    def processElement(left, right, *args):
        try:
            index = args[0]
        except IndexError:
            index = None

        for obj in right.nodeType:
            if not isinstance(obj, CollectionSema):
                continue
            obj.addElementsAtIndex(index, left.nodeType)

        right.walkEdges()

    @staticmethod
    def processFunc(left, right, *args):
        length = len(right.nodeType)
        right.processCall()
        if len(right.nodeType) > length:
            right.walkEdges()

    @staticmethod
    def processKWArgument(left, right, *args):
        length = len(right.nodeType)
        right.processCall()
        if len(right.nodeType) > length:
            right.walkEdges()

    @staticmethod
    def processListArgument(left, right, *args):
        length = len(right.nodeType)
        right.processCall()
        if len(right.nodeType) > length:
            right.walkEdges()

    @staticmethod
    def isNotReverse(edgeType):
        return not edgeType.startswith('Rev')

    @staticmethod
    def isNotReverseAssign(edgeType):
        return edgeType != EdgeType.REV_ASSIGN

class TGNode(object):

    def __init__(self):
        self.nodeType = set()

    def addEdge(self, edgeType, node, *args):
        self.walkEdge(edgeType, node, *args)

    def walkEdge(self, edgeType, node, *args):
        if EdgeType.isNotReverse(edgeType):
            getattr(EdgeType, 'process' + edgeType)(self, node, *args)

    def walkEdges(self):
        pass

    def getElementsTypes(self, index):
        res = set()
        for singleType in self.nodeType:
            updateSet(res, singleType.getElementsAtIndex(index))
        return res

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash((self.__class__, id(self)))

class ConstTGNode(TGNode):

    def __init__(self, node, getValue = False):
        super(ConstTGNode, self).__init__()
        if isinstance(node, ast.Num):
            value = node.n
        elif isinstance(node, ast.Str):
            value = node.s
        elif (isinstance(node, ast.Name) and node.id == 'None' or
              isinstance(node, (ast.Return, ast.Yield)) and not node.value):
            value = None
        else:
            assert False
        self.value = value
        if getValue:
            self.nodeType = {LiteralValueSema(value)}
        else:
            self.nodeType = {LiteralSema(value.__class__)}

    def getValue(self):
        return self.value

class VariableTGNode(TGNode):

    def __init__(self, name, nodeType = None):
        super(VariableTGNode, self).__init__()
        self.name   = name
        self.number = None

        if nodeType is not None:
            self.nodeType = nodeType
        else:
            self.nodeType = set()

    def setNumber(self, number):
        self.number = number

    def process(self):
        pass

class ListTGNode(TGNode):

    def __init__(self, node):
        super(ListTGNode, self).__init__()
        if isinstance(node, ast.List):
            elems = node.elts
            listSema      = ListSema(len(elems))
            self.nodeType = {listSema}
            index = 0
            for elem in elems:
                link = getLink(elem)
                link.addEdge(EdgeType.ELEMENT, self, index)
                index += 1
        else:
            link = getLink(node.elt)
            listSema = ListSema()
            self.nodeType = {listSema}
            link.addEdge(EdgeType.ELEMENT, self)

class TupleTGNode(TGNode):

    def __init__(self, node):
        super(TupleTGNode, self).__init__()
        if isinstance(node, ast.ClassDef):
            elems = node.bases
        else:
            elems = node.elts
        tupleSema     = TupleSema(len(elems))
        self.nodeType = {tupleSema}
        if (isinstance(node, ast.Tuple) or
            isinstance(node, ast.ClassDef)):
            index = 0
            for elem in elems:
                link = getLink(elem)
                link.addEdge(EdgeType.ELEMENT, self, index)
                index += 1

class DictTGNode(TGNode):

    def __init__(self):
        super(DictTGNode, self).__init__()
        dictSema = DictSema()
        self.nodeType = {dictSema}

class SetTGNode(TGNode):

    def __init__(self, node):
        super(SetTGNode, self).__init__()
        setSema = SetSema()
        self.nodeType = {setSema}
        for elem in node.elts:
            link = getLink(elem)
            link.addEdge(EdgeType.ELEMENT, self)

class AttributeTGNode(TGNode):

    def __init__(self, attr):
        super(AttributeTGNode, self).__init__()
        self.attr = attr

    def processWithFlag(self, createNew):
       objects = self.getObjects()
       rights  = self.getRights()
       self.setValues(objects, self.attr, rights, createNew)
       self.nodeType = self.getValues(objects, self.attr)

    def process(self):
        self.processWithFlag(False)

    @staticmethod
    def setValuesWithAttr(obj, attr, values, createNew):
        from ti.lookup import setTypes
        setTypes(obj, attr, values, createNew)

    @staticmethod
    def setValues(objects, attr, values, createNew):
        for obj in objects:
            if not isinstance(obj, classes):
                continue
            AttributeTGNode.setValuesWithAttr(obj, attr, values, createNew)

    @staticmethod
    def getValuesWithAttr(obj, attr):
        from ti.lookup import lookupTypes
        return lookupTypes(obj, attr)

    @staticmethod
    def getValues(objects, attr):
        res = set()
        for obj in objects:
            if not isinstance(obj, classes):
                continue
            newTypes = AttributeTGNode.getValuesWithAttr(obj, attr)
            updateSet(res, newTypes)
        return res

    def objectsCallback(self, result):
        updateSet(result, self.getObjects())

class SubscriptTGNode(TGNode):

    def __init__(self, hasIndex):
        super(SubscriptTGNode, self).__init__()
        self.hasIndex = hasIndex

    def process(self):
       objects = self.getObjects()
       rights  = self.getRights()
       if self.hasIndex:
           indices = self.getIndices()
       else:
           indices = self.getSlices()
       self.setValues(objects, indices, rights, self.hasIndex)
       self.nodeType = self.getValues(objects, indices, self.hasIndex)

    @staticmethod
    def setValuesWithIndex(obj, slices, values):
        for elem in slices:
            if isinstance(obj, DictSema):
                index = None
            else:
                index = getattr(elem, 'value', None)
            if index is not None:
                obj.addElementsAtIndex(index, values)
            else:
                obj.addElementsAtKey(elem, values)

    @staticmethod
    def setValuesWithoutIndex(obj, values):
        if not isinstance(obj, ListSema):
            return
        for value in values:
            obj.addElements(value.getElements())

    @staticmethod
    def setValues(objects, indices, values, hasIndex):
        for obj in objects:
            if not isinstance(obj, CollectionSema):
                continue
            if hasIndex:
                SubscriptTGNode.setValuesWithIndex(obj, indices, values)
            else:
                SubscriptTGNode.setValuesWithoutIndex(obj, values)

    @staticmethod
    def getValuesWithIndex(obj, slices):
        res = set()
        for elem in slices:
            if isinstance(obj, DictSema):
                index = None
            else:
                index = getattr(elem, 'value', None)
            if index is not None:
                newTypes = obj.getElementsAtIndex(index)
            else:
                newTypes = obj.getElementsAtKey(elem)
            updateSet(res, newTypes)
        return res

    @staticmethod
    def getValuesWithoutIndex(obj):
        if isinstance(obj, ListSema):
            objCopy = ListSema(0)
            objCopy.addElementsAtKey(None, obj.getElements())
            return {objCopy}
        else:
            return set()
            
    @staticmethod
    def getValues(objects, indices, hasIndex):
        res = set()
        for obj in objects:
            if hasIndex:
                if isinstance(obj, CollectionSema):
                    newTypes = SubscriptTGNode.getValuesWithIndex(obj, indices)
                else:
                    newTypes = set()
            else:
                if isinstance(obj, CollectionSema):
                    newTypes = SubscriptTGNode.getValuesWithoutIndex(obj)
                elif (isinstance(obj, LiteralSema) and
                      obj.ltype in (str, unicode)):
                    newTypes = set()
                    for elem in itertools.product(*indices):
                        try:
                            value = obj.value
                            lower = getattr(elem[0], 'value', None)
                            upper = getattr(elem[1], 'value', None)
                            if upper:
                                step = getattr(elem[2], 'value', None)
                                if step:
                                    strSlice = value[lower:upper:step]
                                else:
                                    strSlice = value[lower:upper]
                            else:
                                strSlice = value[lower:]
                            newTypes.add(LiteralValueSema(strSlice))
                        except:
                            pass
                else:
                    newTypes = set()
            updateSet(res, newTypes)
        return res

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

    def getNodeName(self):
        return self.name

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

class ForFunctionDefinitionTGNode(FunctionDefinitionTGNode):

    FUNC_NAME = '#func'
    ITER_NAME = '#iter'

    def __init__(self, node, scope):
        super(ForFunctionDefinitionTGNode, self).__init__(self.FUNC_NAME,
                                                          scope,
                                                          None)

        self.ast    = node.body
        self.target = node.target

        param = VariableTGNode(self.ITER_NAME)
        param.setNumber(1)
        self.params.addVariable(param)

class FunctionCallTGNode(TGNode):

    def __init__(self, node, var = None):
        super(FunctionCallTGNode, self).__init__()
        self.node = node

        self._isLocked = True

        if isinstance(node, ast.BinOp):
            func = var
            args = [node.left, node.right]
        elif isinstance(node, ast.UnaryOp):
            func = var
            args = [node.operand]
        elif isinstance(node, ast.AugAssign):
            func = var
            args = [node.target, node.value]
        else:
            func = getLink(node.func)
            args = node.args

        func.addEdge(EdgeType.FUNC, self)

        index = 0
        for arg in args:
            link = getLink(arg)
            link.addEdge(EdgeType.ARGUMENT, self)
            index += 1
        self.argsNum = index

        if isinstance(node, ast.Call):
            for pair in node.keywords:
                link = getLink(pair.value)
                link.addEdge(EdgeType.KWARGUMENT, self)

            if node.starargs:
                link = getLink(node.starargs)
                link.addEdge(EdgeType.LISTARGUMENT, self)

        self._isLocked = False

        self.processCall()

    def getArgumentNodesNumber(self):
        return self.argsNum

    def isLocked(self):
        return self._isLocked

    def process(self):
        pass
 
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

    def process(self):
        pass

class ClassTGNode(TGNode):

    def __init__(self, name, bases, scope):
        super(ClassTGNode, self).__init__()

        nodeType = ClassSema(self)
        self.nodeType = {nodeType}

        self.name   = name
        self.parent = scope
        self.scope  = nodeType
        self.bases  = bases
        self.body   = ScopeSema()

    def getBases(self):
        return self.bases

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

        self._inherited = inheritedScope is not None
        if self._inherited:
            self.body   = None
            self.scope  = inheritedScope
        else:
            self.body  = ScopeSema()
            self.scope = ModuleSema(self)

            nodeType = {LiteralValueSema(name)}
            nameVar = VariableTGNode('__name__', nodeType)
            self.scope.addVariable(nameVar)

        self.parent   = parent
        self.nodeType = {self.scope}

    def getBody(self):
        return self.body

    def getParent(self):
        return self.parent

    def getScope(self):
        return self.scope

    def isInherited(self):
        return self._inherited

class UsualModuleTGNode(ModuleTGNode):

    def __init__(self, ast, name, parentScope, inheritedScope = None):
        super(UsualModuleTGNode, self).__init__(name,
                                                parentScope,
                                                inheritedScope)
        self.ast = ast

    def getAST(self):
        return self.ast

class ExternalModuleTGNode(ModuleTGNode):

    def __init__(self, name, parentScope, asname = None):
        super(ExternalModuleTGNode, self).__init__(name, parentScope, None)
        self.asname = asname if asname else self.name

    def getAliasName(self):
        return self.asname

    def getNodeName(self):
        return self.getAliasName()

class BooleanOperationTGNode(TGNode):

    def __init__(self, op):
        super(BooleanOperationTGNode, self).__init__()
        self.isAnd = isinstance(op, ast.And)

    def process(self):
        pass
