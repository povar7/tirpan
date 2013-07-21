'''
Created on 26.05.2013

@author: bronikkk
'''

import ast
import os
import types

from ti.sema import *

classes = (CollectionSema, LiteralSema, ClassSema, InstanceSema, ModuleSema)

class EdgeType(object):

    ARGUMENT         = 'Argument'
    ASSIGN           = 'Assign'
    ASSIGN_ELEMENT   = 'AssignElement'
    ASSIGN_OBJECT    = 'AssignObject'
    ASSIGN_SLICE     = 'AssignSlice'
    ASSIGN_YIELD     = 'AssignYield'
    ATTR_SLICE       = 'AttrSlice'
    ATTR_OBJECT      = 'AttrObject'
    ELEMENT          = 'Element'
    FUNC             = 'Func'
    KWARGUMENT       = 'KWArgument'
    LISTARGUMENT     = 'ListArgument'
    REV_ARGUMENT     = 'RevArgument'
    REV_ASSIGN       = 'RevAssign'
    REV_FUNC         = 'RevFunc'
    REV_KWARGUMENT   = 'RevKWArgument'
    REV_LISTARGUMENT = 'RevListArgument'

    @staticmethod
    def updateRight(right, types):
        if len(types - right.nodeType) > 0:
            length = len(right.nodeType)
            right.nodeType |= types
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
        # Remove simple loops in type variables graph
        try:
            if (left, ()) in right.edges[EdgeType.ARGUMENT]:
                right.removeEdge(EdgeType.ARGUMENT, left)
        except KeyError:
            pass

        EdgeType.updateRight(right, left.nodeType)

    @staticmethod
    def processAssignElement(left, right, *args):
        index = args[0]
        types = left.getElementsTypes(index)
        EdgeType.updateRight(right, types)

    @staticmethod
    def processAssignObject(left, right, *args):
        pass

    @staticmethod
    def processAssignSlice(left, right, *args):
        pass

    @staticmethod
    def processAssignYield(left, right, *args):
        listType = ListSema(0)
        listType.elems[0] |= left.nodeType
        types = {listType}
        EdgeType.updateRight(right, types)

    @staticmethod
    def processAttrSlice(left, right, *args):
        right.process()

    @staticmethod
    def processAttrObject(left, right, *args):
        right.process()

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

        # Remove simple loops in type variables graph
        try:
            if (left, ()) in right.edges[EdgeType.ASSIGN]:
                right.removeEdge(EdgeType.ASSIGN, left)
        except KeyError:
            pass

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
    def processRevArgument(left, right, *args):
        pass

    @staticmethod
    def processRevAssign(left, right, *args):
        pass

    @staticmethod
    def processRevFunc(left, right, *args):
        pass

    @staticmethod
    def processRevKWArgument(left, right, *args):
        pass

    @staticmethod
    def processRevListArgument(left, right, *args):
        pass

class TGNode(object):

    def __init__(self):
        self.edges    = {}
        self.nodeType = set()

    def addEdge(self, edgeType, node, *args):
        if edgeType == EdgeType.ASSIGN:
            node.addEdge(EdgeType.REV_ASSIGN, self)
        if not edgeType in self.edges:
            self.edges[edgeType] = set()
        self.edges[edgeType].add((node, args))
        self.walkEdge(edgeType, node, *args)

    def removeEdge(self, edgeType, node):
        self.edges[edgeType].discard((node, ()))
    
    def walkEdge(self, edgeType, node, *args):
        getattr(EdgeType, 'process' + edgeType)(self, node, *args)

    def walkEdges(self):
        for edgeType in self.edges:
            for node, args in self.edges[edgeType]:
                self.walkEdge(edgeType, node, *args)

    def getEdges(self, edgeType):
        try:
            return self.edges[edgeType]
        except KeyError:
            return set()

    def getElementsTypes(self, index):
        res = set()
        for singleType in self.nodeType:
            res |= singleType.getElementsAtIndex(index)
        return res

class ConstTGNode(TGNode):

    def __init__(self, node, getValue = False):
        super(ConstTGNode, self).__init__()
        if isinstance(node, ast.Num):
            value = node.n
        elif isinstance(node, ast.Str):
            value = node.s
        elif (isinstance(node, ast.Name)   and node.id == 'None' or
              isinstance(node, (ast.Return, ast.Yield)) and not node.value):
            value = None
        else:
            assert(False)
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
        # self.parent = None

        if nodeType is not None:
            self.nodeType = nodeType
        else:
            self.nodeType = set()

    def setNumber(self, number):
        self.number = number

    def setParent(self, parent):
        # self.parent = parent
        pass

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
                link = elem.link
                link.addEdge(EdgeType.ELEMENT, self, index)
                index += 1
        else:
            node.elt.addEdge(EdgeType.ELEMENT, self)

class TupleTGNode(TGNode):

    def __init__(self, node):
        super(TupleTGNode, self).__init__()
        elems = node.elts
        tupleSema     = TupleSema(len(elems))
        self.nodeType = {tupleSema}
        if isinstance(node, ast.Tuple):
            index = 0
            for elem in elems:
                link = elem.link
                link.addEdge(EdgeType.ELEMENT, self, index)
                index += 1

class DictTGNode(TGNode):

    def __init__(self):
        super(DictTGNode, self).__init__()
        dictSema = DictSema()
        self.nodeType = {dictSema}

class AttributeTGNode(TGNode):

    def __init__(self, attr):
        super(AttributeTGNode, self).__init__()
        self.attr = attr

    def getObjects(self):
       objects = set()
       for node, args in self.getEdges(EdgeType.ASSIGN_OBJECT):
           objects |= node.nodeType
       return objects

    def getRights(self):
       rights = set()
       for node, args in self.getEdges(EdgeType.REV_ASSIGN):
           rights |= node.nodeType
       return rights

    def process(self):
       objects = self.getObjects()
       rights  = self.getRights()
       self.setValues(objects, self.attr, rights)
       self.nodeType = self.getValues(objects, self.attr)

    @staticmethod
    def setValuesWithAttr(obj, attr, values):
        from ti.lookup import lookupVariable
        var = lookupVariable(obj, attr, True, len(values) > 0)
        if var is not None:
            EdgeType.updateRight(var, values)

    @staticmethod
    def setValues(objects, attr, values):
        for obj in objects:
            if not isinstance(obj, classes):
                continue
            AttributeTGNode.setValuesWithAttr(obj, attr, values)

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
            res |= newTypes
        return res

class SubscriptTGNode(TGNode):

    def __init__(self, hasIndex):
        super(SubscriptTGNode, self).__init__()
        self.hasIndex = hasIndex

    def getSlices(self):
       slices = set()
       for node, args in self.getEdges(EdgeType.ASSIGN_SLICE):
           slices |= node.nodeType
       return slices

    def getRights(self):
       rights = set()
       for node, args in self.getEdges(EdgeType.REV_ASSIGN):
           rights |= node.nodeType
       return rights

    def getObjects(self):
       objects = set()
       for node, args in self.getEdges(EdgeType.ASSIGN_OBJECT):
           objects |= node.nodeType
       return objects

    def process(self):
       objects = self.getObjects()
       rights  = self.getRights()
       slices  = self.getSlices()
       self.setValues(objects, slices, rights, self.hasIndex)
       self.nodeType = self.getValues(objects, slices, self.hasIndex)

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
    def setValues(objects, slices, values, hasIndex):
        for obj in objects:
            if not isinstance(obj, CollectionSema):
                continue
            if hasIndex:
                SubscriptTGNode.setValuesWithIndex(obj, slices, values)
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
            res |= newTypes
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
    def getValues(objects, slices, hasIndex):
        res = set()
        for obj in objects:
            if not isinstance(obj, CollectionSema):
                continue
            if hasIndex:
                newTypes = SubscriptTGNode.getValuesWithIndex(obj, slices)
            else:
                newTypes = SubscriptTGNode.getValuesWithoutIndex(obj)
            res |= newTypes
        return res

class FunctionDefinitionTGNode(TGNode):

    def __init__(self, name, scope, defaults):
        super(FunctionDefinitionTGNode, self).__init__()

        nodeType = FunctionSema(self, scope)
        self.nodeType  = {nodeType}

        self.name      = name
        self.parent    = scope
        self.templates = {}

        self.params    = ScopeSema()
        self.listParam = None
        self.dictParam = None

        self.defaults  = defaults if defaults else {}

        self.globalNames = set()

    def isListParam(self, param):
        return param and param is self.listParam

    def isDictParam(self, param):
        return param and param is self.dictParam

    @staticmethod
    def sortParams(x, y):
        return cmp(x.number, y.number)

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
        return sorted(unsorted, self.sortParams)

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

    def __init__(self, node, name, scope):
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

    def __init__(self, num, quasi, name, scope, defaults):
        super(ExternalFunctionDefinitionTGNode, self).__init__(name,
                                                               scope,
                                                               defaults)

        self.quasi = quasi

        for index in range(num):
            number = index + 1
            param = VariableTGNode(str(number))
            param.setNumber(number)
            self.params.addVariable(param)

class FunctionCallTGNode(TGNode):

    def __init__(self, node, var = None):
        super(FunctionCallTGNode, self).__init__()
        self.node = node

        self._isLocked = True

        if isinstance(node, ast.Call):
            func = node.func.link
            args = node.args
        elif isinstance(node, ast.BinOp):
            func = var
            args = [node.left, node.right]
        elif isinstance(node, ast.UnaryOp):
            func = var
            args = [node.operand]
        elif isinstance(node, ast.AugAssign):
            func = var
            args = [node.value]

        func.addEdge(EdgeType.FUNC, self)
        self.addEdge(EdgeType.REV_FUNC, func)

        index = 0
        for arg in args:
            link = arg.link
            link.addEdge(EdgeType.ARGUMENT, self)
            self.addEdge(EdgeType.REV_ARGUMENT, link, index)
            index += 1
        self.argsNum = index

        if isinstance(node, ast.Call):
            for pair in node.keywords:
                link = pair.value.link
                link.addEdge(EdgeType.KWARGUMENT, self)
                self.addEdge(EdgeType.REV_KWARGUMENT, link, pair.arg)

            if node.starargs:
                link = node.starargs.link
                link.addEdge(EdgeType.LISTARGUMENT, self)
                self.addEdge(EdgeType.REV_LISTARGUMENT, link)

        self._isLocked = False

        self.processCall()

    def getArgumentNode(self, index):
        for node, args in self.getEdges(EdgeType.REV_ARGUMENT):
            try:
                if args[0] == index:
                    return node
            except IndexError:
                pass
        return None

    def getFunctionNode(self):
        edges = self.getEdges(EdgeType.REV_FUNC)
        assert(len(edges) == 1)
        for node, args in edges:
            return node
        return None

    def getKWArgumentNodes(self):
        res = {}
        for node, args in self.getEdges(EdgeType.REV_KWARGUMENT):
            key = args[0]
            res[key] = node
        return res

    def getListArgumentNode(self):
        edges = self.getEdges(EdgeType.REV_LISTARGUMENT)
        assert(len(edges) <= 1)
        for node, args in edges:
            return node
        return None

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
        for index in range(self.argsNum):
            oldArgumentNodes.append(self.getArgumentNode(index))
        for listArgumentType in listArgumentTypes:
            argumentNodes = oldArgumentNodes[:]
            for elem in listArgumentType:
                argumentNodes.append(None)
            processFunc(self, functionNode,
                        argumentNodes, KWArgumentNodes, listArgumentType)

class FunctionTemplateTGNode(TGNode):

    def __init__(self, params, function, inst):
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

        self.params = params

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

        self.templates = {}

    def getBases(self):
        return self.bases

    def getBody(self):
        return self.body

    def getParent(self):
        return self.parent

    def getScope(self):
        return self.scope

    def getTemplates(self):
        return self.templates

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

    def __init__(self, name, parentScope):
        super(ExternalModuleTGNode, self).__init__(name, parentScope, None)

class BooleanOperationTGNode(TGNode):

    def __init__(self, op):
        super(BooleanOperationTGNode, self).__init__()
        self.isAnd = isinstance(op, ast.And)

    def process(self):
        pass

class UnknownTGNode(TGNode):

    def __init__(self, node):
        super(UnknownTGNode, self).__init__()
        self.nodeType = {NoSema()}
