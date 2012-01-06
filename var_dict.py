'''
Created on 03.01.2012

@author: ramil
'''

class VarDict(object):
    variables = None
    parent = None
    def __init__(self, parent = None):
        self.parent = None
        self.variables = {}
    def append(self, name, graph_node):
        self.variables[name] = graph_node
    def find(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.find(name)
        return None
        