'''
Created on 26.05.2013

@author: bronikkk
'''

import ast

from ti.sema import LiteralSema, ListSema, NoSema

class EdgeType(object):
    ARGUMENT       = 'Argument'
    ASSIGN         = 'Assign'
    ASSIGN_ELEMENT = 'AssignElement'
    ELEMENT        = 'Element'

    @staticmethod
    def updateRight(right, types):
        if len(types - right.nodeType) > 0:
            length = len(right.nodeType)
            right.nodeType |= types
            if len(right.nodeType) > length:
                right.walkEdges()

    @staticmethod
    def processArgument(left, right):
        pass

    @staticmethod
    def processAssign(left, right):
        # Remove simple loops in type variables graph
        try:
            if (left, ()) in right.edges[EdgeType.ARGUMENT]:
                right.removeEdge(EdgeType.ARGUMENT, left)
        except KeyError:
            pass

        if isinstance(right, VariableTGNode):
            EdgeType.updateRight(right, left.nodeType)

    @staticmethod
    def processAssignElement(left, right, *args):
        index = args[0]
        types = left.getElements(index)
        EdgeType.updateRight(right, types)

    @staticmethod
    def processElement(left, right, *args):
        try:
            index = args[0]
        except IndexError:
            index = None

        for collection in right.nodeType:
            for leftType in left.nodeType:
                if index is not None:
                    elem = collection.getElementAtIndex(index)
                    if elem == NoSema():
                        collection.setElementAtIndex(index, leftType)
                        continue
                collection.addElement(leftType)

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

class ConstTGNode(TGNode):
    def __init__(self, node):
        super(ConstTGNode, self).__init__()
        self.node = node
        if isinstance(node, ast.Num):
            value = node.n
        elif isinstance(node, ast.Str):
            value = node.s
        else:
            value = None
        self.nodeType = {LiteralSema(value.__class__)}

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
    
class UnknownTGNode(TGNode):
    def __init__(self, node):
        super(UnknownTGNode, self).__init__()
        self.nodeType = {NoSema()}
