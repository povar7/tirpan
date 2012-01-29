'''
Created on 11.12.2011

@author: ramil
'''

from scope import Scope

class TypeGraphNode(object):
    def __init__(self):
        self.deps = []
        nodeValue = None

    def addDependency(self, dep):
        if dep and dep not in self.deps:
            self.deps.append(dep)
            dep.appendTypes(self.nodeType)
            
    def appendTypes(self, typeSet):
        tmp = self.nodeType
        self.childTypes(typeSet)
        #XXX Start of a temporarily disabled code
        #if len(self.nodeType - tmp) != 0:
        #    for dep in self.deps:
        #        dep.appendTypes(self.nodeType)
        #XXX End of a temporarily disabled code
    def childTypes(self, typeSet):
        pass
        #XXX Start of a temporarily disabled code
        #self.nodeType = self.nodeType.union(typeSet)
        #XXX End of a temporarily disabled code
        
class ConstTypeGraphNode(TypeGraphNode):
    def __init__(self, value):
        super(ConstTypeGraphNode, self).__init__()
        self.nodeType  = set([value.__class__])
        self.nodeValue = value
            
class VarTypeGraphNode(TypeGraphNode):
    def __init__(self, name):
        super(VarTypeGraphNode, self).__init__()
        self.nodeType  = set()
        self.nodeValue = set()
        self.name = name
    def add_value(self, value):
        self.nodeValue = self.nodeValue.union(set([value]))

class ListTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(ListTypeGraphNode, self).__init__()
        self.nodeType  = set()
        self.nodeValue = []
        for elt in node.elts:
            link = elt.link
            link.addDependency(self)
            self.nodeValue.append(link)

class TupleTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(TupleTypeGraphNode, self).__init__()
        self.nodeType  = set()
        tempValue      = []
        for elt in node.elts:
            link = elt.link
            link.addDependency(self)
            tempValue.append(link)
        self.nodeValue = tuple(tempValue)

class DictTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(DictTypeGraphNode, self).__init__()
        self.nodeType  = (set(), set())
        self.nodeValue = {}
        for i in range(len(node.keys)):
            keyLink   = node.keys[i].link
            valueLink = node.values[i].link
            keyLink.addDependency(self)
            valueLink.addDependency(self)
            self.nodeValue[keyLink] = valueLink

class AssignTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(AssignTypeGraphNode, self).__init__()
        self.nodeType  = node.value.link.nodeType
        self.nodeValue = node.value.link.nodeValue
        for target in node.targets:
            self.addDependency(target.link) 

class ModuleTypeGraphNode(TypeGraphNode):
    def __init__(self, ast, name, parent_scope):
        super(ModuleTypeGraphNode, self).__init__()
        self.nodeType = None
        self.ast      = ast
        self.name     = name
        self.scope    = Scope(parent_scope)
    def get_scope(self):
        return self.scope 
