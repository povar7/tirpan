'''
Created on 26.05.2013

@author: bronikkk
'''

import ast

from ti.sema    import *

class EdgeType(object):

    ARGUMENT       = 'Argument'
    ASSIGN         = 'Assign'
    ASSIGN_ELEMENT = 'AssignElement'
    ASSIGN_OBJECT  = 'AssignObject'
    ASSIGN_SLICE   = 'AssignSlice'
    ATTR_SLICE     = 'AttrSlice'
    ATTR_OBJECT    = 'AttrObject'
    ELEMENT        = 'Element'

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
        pass

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
        # Trying to retrieve constants
        if isinstance(left, ConstTGNode) and len(left.nodeType) == 1:
            left.nodeType.add(LiteralValueSema(left.getValue()))
            left.walkEdges()
            return

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
            for leftType in left.nodeType:
                obj.setElementAtIndex(index, leftType)

        # Remove simple loops in type variables graph
        try:
            if (left, ()) in right.edges[EdgeType.ASSIGN]:
                right.removeEdge(EdgeType.Assign, left)
        except KeyError:
            pass

        right.walkEdges()

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

    def __init__(self, node):
        super(ConstTGNode, self).__init__()
        if isinstance(node, ast.Num):
            value = node.n
        elif isinstance(node, ast.Str):
            value = node.s
        else:
            assert(False)
        self.value = value
        self.nodeType = {LiteralSema(value.__class__)}

    def getValue(self):
        return self.value

class VariableTGNode(TGNode):

    def __init__(self, name, nodeType = None):
        super(VariableTGNode, self).__init__()
        self.name     = name
        if nodeType is not None:
            self.nodeType = nodeType
        else:
            self.nodeType = set()
        self.parent   = None

    def setParent(self, parent):
        self.parent = parent

class ListTGNode(TGNode):

    def __init__(self, node):
        super(ListTGNode, self).__init__()
        listSema      = ListSema()
        self.nodeType = {listSema}
        if isinstance(node, ast.List):
            elems = node.elts
            listSema.elems = [NoSema(),] * len(elems)
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
        tupleSema     = TupleSema()
        self.nodeType = {tupleSema}
        if isinstance(node, ast.Tuple):
            elems = node.elts
            tupleSema.elems = [NoSema(),] * len(elems)
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
                obj.setElementsAtIndex(index, values)
            else:
                obj.setElementsAtKey(elem, values)

    @staticmethod
    def setValuesWithoutIndex(obj, values):
        if not isinstance(obj, ListSema):
            return
        for value in values:
            for elem in value.getElements():
                obj.addElement(elem)

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
            objCopy = ListSema()
            for elem in obj.getElements():
                objCopy.addElement(elem)
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
    
class UnknownTGNode(TGNode):

    def __init__(self, node):
        super(UnknownTGNode, self).__init__()
        self.nodeType = {NoSema()}
