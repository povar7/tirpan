'''
Created on 11.12.2011

@author: ramil
'''

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
        if len(self.nodeType - tmp) != 0:
            for dep in self.deps:
                dep.appendTypes(self.nodeType)
    def childTypes(self, typeSet):
        self.nodeType = self.nodeType.union(typeSet)
        
class ConstTypeGraphNode(TypeGraphNode):
    def __init__(self, value):
        super(ConstTypeGraphNode, self).__init__()
        self.nodeType  = set([value.__class__])
        self.nodeValue = value
            
class VarTypeGraphNode(TypeGraphNode):
    def __init__(self, name):
        super(VarTypeGraphNode, self).__init__()
        self.nodeType = set()
        self.name = name

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

