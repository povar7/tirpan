'''
Created on 11.12.2011

@author: ramil
'''
from sets import Set

class Node(object):
    value = None
    type = Set()
    inheritance_graph = None
    depending_on = None
    def __init__(self, graph):
        self.inheritance_graph = graph
        self.depending_on = []
    def addDependency(self, node):
        self.depending_on.append(node)
        self.recalcType()
    def recalcType(self):
        for child in self.depending_on:
            child.type = child.type.union(self.type)
            child.recalcType()
        
class Constant(Node):
    def set_value(self, value):
        self.value = value
        self.handle_type()
    def handle_type(self):
        if hasattr(self.value, '__class__'):
            type_name = self.value.__class__.__name__
            types = self.inheritance_graph.find(type_name)
            if len(types) == 0:
                node = self.inheritance_graph.append(TypeNode({'name': self.value.__class__.__name__}))
                self.type = Set([node])
            elif len(types) == 1:
                self.type = Set(types)
            else:
                pass;
            
            
            
class Variable(Node):
    pass;
            
class InheritanceGraph(object):
    nodes = []
    def find(self, type_name):
        return [node for node in self.nodes if node.name == type_name] 
    def append(self, node):
        self.nodes.append(node)
        return node

class TypeNode(object):
    name = None
    parents = None
    def __init__(self, params):
        self.name = params['name'] 
    