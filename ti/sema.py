'''
Created on 26.05.2013

@author: bronikkk
'''

import copy

class ScopeWrap(object):

    def __init__(self, scope):
        self.scope = scope

class Sema(object):

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.isInstanceEqualTo(other))

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.__class__, self.getInstanceHash()))

    def freeze(self):
        pass

class LiteralSema(Sema):

    def __init__(self, ltype):
        self.ltype = ltype

    def isInstanceEqualTo(self, other):
        return self.ltype == other.ltype

    def getInstanceHash(self):
        return hash(self.ltype)

class ListSema(Sema):

    def __init__(self):
        self.elems  = set()
        self.frozen = False

    def addElement(self, elem):
        assert(not self.frozen)
        if isinstance(self.elems, list):
            self.elems = set(self.elems)
        self.elems.add(elem)

    def getElementAtIndex(self, index):
        try:
            return self.elems[index]
        except TypeError:
            return None

    def setElementAtIndex(self, index, elem):
        assert(not self.frozen)
        self.elems[index] = elem

    def getElements(self):
        return self.elems

    def isInstanceEqualTo(self, other):
        assert(self.frozen == other.frozen)
        if self.frozen:
            return self.elems == other.elems
        else:
            return self is other

    def getInstanceHash(self):
        if self.frozen:
            return hash(frozenset(self.elems))
        else:
            return id(self)

    def freeze(self):
        self.elems = freeze(self.elems)
        self.frozen = True

class ScopeSema(Sema):

    def __init__(self, parent = None, hasGlobals = None):
        self.parent      = parent
        self.variables   = {}
        self.hasGlobals  = hasGlobals
        self.globalNames = set()

    def addVariable(self, var):
        var.setParent(self)
        self.variables[var.name] = var

    def findName(self, name, considerGlobals = False, scopeWrap = None):
        if name in self.variables:
            return self.variables[name]
        if (considerGlobals and
            self.hasGlobals and name not in self.globalNames):
            if scopeWrap:
                scopeWrap.scope = None
            return None
        if self.parent:
            return self.parent.findName(name, considerGlobals, scopeWrap)
        return None

    def findOrAddName(self, name, considerGlobals = False, fileScope = None):
        scopeWrap = ScopeWrap(fileScope)
        res = self.findName(name, considerGlobals, scopeWrap)
        fileScope = scopeWrap.scope
        if not res:
            from ti.tgnode import VariableTGNode
            res = VariableTGNode(name)
            if considerGlobals and fileScope:
                fileScope.addVariable(res)
            else:
                self.addVariable(res)
        return res
 
    def getParent(self):
        return self.parent

class UnknownSema(Sema):

    def __init__(self):
        pass

    def isInstanceEqualTo(self, other):
        return True

    def getInstanceHash(self):
        return hash(self.__class__)

unknownSema = UnknownSema()

def NoSema():
    return unknownSema

def freeze(elems):
    res = set()
    for elem in elems:
        elementCopy = copy.copy(elem)
        elementCopy.freeze()
        res.add(elementCopy)
    return res
