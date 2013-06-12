'''
Created on 26.05.2013

@author: bronikkk
'''

import ast

from ti.sema import *

class EdgeType(object):

    ARGUMENT       = 'Argument'
    ASSIGN         = 'Assign'
    ASSIGN_ELEMENT = 'AssignElement'
    ASSIGN_OBJECT  = 'AssignObject'
    ASSIGN_SLICE   = 'AssignSlice'
    ATTR_SLICE     = 'AttrSlice'
    ATTR_OBJECT    = 'AttrObject'
    ELEMENT        = 'Element'
    FUNC           = 'Func'
    REV_ARGUMENT   = 'RevArgument'
    REV_FUNC       = 'RevFunc'

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
        right.process()
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
                right.removeEdge(EdgeType.Assign, left)
        except KeyError:
            pass

        right.walkEdges()

    @staticmethod
    def processFunc(left, right, *args):
        length = len(right.nodeType)
        right.process()
        if len(right.nodeType) > length:
            right.walkEdges()

    @staticmethod
    def processRevArgument(left, right, *args):
        pass

    @staticmethod
    def processRevFunc(left, right, *args):
        pass

class TGNode(object):

    def __init__(self):
        self.edges    = {}
        self.nodeType = set()

    def addEdge(self, edgeType, node, *args):
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

    def process(self):
        pass

class ConstTGNode(TGNode):

    def __init__(self, node, getValue = False):
        super(ConstTGNode, self).__init__()
        if isinstance(node, ast.Num):
            value = node.n
        elif isinstance(node, ast.Str):
            value = node.s
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

class SubscriptTGNode(TGNode):

    def __init__(self, hasIndex):
        super(SubscriptTGNode, self).__init__()
        self.hasIndex = hasIndex

    def getSlices(self):
       slices = set()
       for node, args in self.getEdges(EdgeType.ASSIGN_SLICE):
           slices |= node.nodeType
       return slices

    def getObjects(self):
       objects = set()
       for node, args in self.getEdges(EdgeType.ASSIGN_OBJECT):
           objects |= node.nodeType
       return objects

    def process(self):
       objects = self.getObjects()
       slices  = self.getSlices()
       self.setValues(objects, slices, self.nodeType, self.hasIndex)
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

    def __init__(self, name, scope):
        super(FunctionDefinitionTGNode, self).__init__()

        nodeType = FunctionSema(self, scope)

        self.nodeType  = {nodeType}
        self.parent    = scope
        self.templates = {}

        self.params    = ScopeSema()
        self.listParam = None
        self.dictParam = None
        self.defaults  = {}

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
        return [var for var in variables if var.number]

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

class UsualFunctionDefinitionTGNode(FunctionDefinitionTGNode):

    def __init__(self, node, name, scope):
        super(UsualFunctionDefinitionTGNode, self).__init__(name, scope)

        if isinstance(node, ast.Lambda):
            self.ast = [node.body]
        else:
            self.ast = node.body

        if node.args.vararg:
            self.listParam = VariableTGNode(node.args.vararg)

        if node.args.kwarg:
            self.dictParam = VariableTGNode(node.args.kwarg)

class FunctionCallTGNode(TGNode):

    def __init__(self, node):
        super(FunctionCallTGNode, self).__init__()

        self._isLocked = True

        if isinstance(node, ast.Call):
            func = node.func.link
            args = node.args
        else:
            func = None
        func.addEdge(EdgeType.FUNC, self)
        self.addEdge(EdgeType.REV_FUNC, func)

        index = 0
        for arg in node.args:
            link = arg.link
            link.addEdge(EdgeType.ARGUMENT, self)
            self.addEdge(EdgeType.REV_ARGUMENT, link, index)
            index += 1
        self.argsNum = index

        self._isLocked = False

        self.process()

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

    def isLocked(self):
        return self._isLocked
 
    def process(self):
        from ti.function import processCall
        if self._isLocked:
            return
        functionNode  = self.getFunctionNode()
        argumentNodes = []
        for index in range(self.argsNum):
            argumentNodes.append(self.getArgumentNode(index))
        processCall(self, functionNode, argumentNodes)

class FunctionTemplateTGNode(TGNode):

    def __init__(self, params, scope):
        super(FunctionTemplateTGNode, self).__init__()

        self.params = params
        self.parent = scope
        self.scope  = TemplateSema(self)

    def getParams(self):
        return self.params

    def getParent(self):
        return self.parent

    def getScope(self):
        return self.scope

class UnknownTGNode(TGNode):

    def __init__(self, node):
        super(UnknownTGNode, self).__init__()
        self.nodeType = {NoSema()}
