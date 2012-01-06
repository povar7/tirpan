'''
Created on 11.12.2011

@author: ramil
'''
from types_hierarchy import *
            
            
class Graph(object):
    nodes = []
    def append(self, node):
        self.nodes.append(node)
        return node

class GraphNode(object):
    def __init__(self):
        self.dpnd = []
        type = set()
        value = None

    def addDependency(self, node):
        self.dpnd.append(node)
        
class TConst(GraphNode):
    def __init__(self, hierarhyGraph, value):
        super(TConst, self).__init__()
        self.value = value
        if hasattr(self.value, '__class__'):
            type_name = self.value.__class__.__name__
            types = hierarhyGraph.find(type_name)
            if len(types) == 0:
                node = hierarhyGraph.append(SimpleNode(self.value.__class__.__name__))
                self.type = set([node])
            elif len(types) == 1:
                self.type = set(types)
            else:
                pass;
            
class TVar(GraphNode):
    name = None
    def __init__(self, name):
        super(TVar, self).__init__()
        self.name = name

class TList(GraphNode):
    def __init__(self, hierarhyGraph, node):
        super(TList, self).__init__()
        self.value = []
        for el in node.elts:
            self.value.append(el.link)
        self.type = set([hierarhyGraph.append(ListNode(self.value))])
        self.elem = TElem(self, self.value)
        self.addDependency(self.elem)

class TTuple(GraphNode):
    def __init__(self, hierarhyGraph, node):
        super(TTuple, self).__init__()
        self.value = []
        for el in node.elts:
            self.value.append(el.link)
        self.type = set([hierarhyGraph.append(TupleNode(self.value))])
        self.elem = TElem(self, self.value)
        self.addDependency(self.elem)
        
class TElem(GraphNode):
    def __init__(self, parent, values):
        super(TElem, self).__init__()
        self.value = None
        self.type = set()
        for val in values:
            self.type = self.type.union(val.type)
            val.addDependency(self)
        self.parent = parent
        self.addDependency(parent)

class TDict(GraphNode):
    def __init__(self, hierarhyGraph, node):
        super(TDict, self).__init__()
        self.value = []
        self.keys = []
        for vv in node.values:
            self.value.append(vv.link)
        for key in node.keys:
            self.keys.append(key.link)
        self.type = set([hierarhyGraph.append(DictNode(self))])
        self.elem = TElem(self, self.value)
        self.addDependency(self.elem)
        self.key = TElem(self, self.keys)
        self.addDependency(self.key)