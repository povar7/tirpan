'''
Created on 03.01.2012

@author: ramil
'''

class Scope(object):
    def __init__(self, parent = None):
        self.parent = parent
        self.variables = {}

    def add(self, name, varNode):
        varNode.parent       = self
        self.variables[name] = varNode

    def find(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.find(name)
        return None

    def findOrAdd(self, name):
        res = self.find(name)
        if not res:
            from typegraph import VarTypeGraphNode
            res = VarTypeGraphNode(name)
            self.add(name, res)
        return res
 
    def getParent(self):
        return self.parent

    def printVariables(self):
        for var in self.variables.iteritems():
            print var[0], ':', var[1].nodeType
