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
        super(LiteralSema, self).__init__()
        self.ltype = ltype

    def isInstanceEqualTo(self, other):
        return self.ltype == other.ltype

    def getInstanceHash(self):
        return hash(self.ltype)

class LiteralValueSema(LiteralSema):

    def __init__(self, value):
        super(LiteralValueSema, self).__init__(value.__class__)
        self.value = value

    def isInstanceEqualTo(self, other):
        return (self.ltype == other.ltype and
                self.value == other.value)

    def getInstanceHash(self):
        return hash((self.ltype, self.value))

class CollectionSema(Sema):

    def __init__(self):
        super(CollectionSema, self).__init__()
        self.frozen = False

    def setElementsAtIndex(self, index, values):
        for value in values:
            self.setElementAtIndex(index, value)

    def setElementsAtKey(self, key, values):
        for value in values:
            self.setElementAtKey(key, value)

class ListOrTupleSema(CollectionSema):
    
    def __init__(self):
        super(ListOrTupleSema, self).__init__()
        self.elems  = set()

    def addElement(self, elem):
        assert(not self.frozen)
        if isinstance(self.elems, list):
            self.elems = set(self.elems)
        self.elems.add(elem)

    def getElements(self):
        return self.elems

    def getElementsSet(self):
        if isinstance(self.elems, set):
            return self.elems
        else:
            return set(self.elems)

    def getElementsAtIndex(self, index):
        try:
            return {self.elems[index]}
        except:
            return self.getElementsSet()

    def getElementAtIndex(self, index):
        try:
            return self.elems[index]
        except:
            return None

    def setElementAtIndex(self, index, elem):
        assert(not self.frozen)
        try:
            if self.elems[index] == NoSema():
                self.elems[index] = elem
                return
        except KeyError:
            pass
        except TypeError:
            pass
        self.setElementAtKey(index, elem)

    def setElementAtKey(self, key, elem):
        self.addElement(elem)

    def getElementsAtKey(self, key):
        return self.getElementsSet()

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
        self.elems = freezeSet(self.elems)
        self.frozen = True

class ListSema(ListOrTupleSema):

    def __init__(self):
        super(ListSema, self).__init__()

class TupleSema(ListOrTupleSema):

    def __init__(self):
        super(TupleSema, self).__init__()

class DictSema(CollectionSema):
    
    def __init__(self):
        super(DictSema, self).__init__()
        self.elems = dict()

    def isInstanceEqualTo(self, other):
        assert(self.frozen == other.frozen)
        if self.frozen:
            return self.elems == other.elems
        else:
            return self is other

    def getInstanceHash(self):
        if self.frozen:
            return hash(frozenset(self.elems.items()))
        else:
            return id(self)

    def getElementsAtKey(self, key):
        try:
            return self.elems[key]
        except:
            return set()

    def setElementAtKey(self, key, elem):
        try:
            value = self.elems[key]
            value.add(elem)
        except KeyError:
            self.elems[key] = {elem}

    def freeze(self):
        self.elems = freezeDict(self.elems)
        self.frozen = True

class ScopeSema(Sema):

    def __init__(self, parent = None, hasGlobals = None):
        super(ScopeSema, self).__init__
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
        super(UnknownSema, self).__init__()

    def isInstanceEqualTo(self, other):
        return True

    def getInstanceHash(self):
        return hash(self.__class__)

unknownSema = UnknownSema()

def NoSema():
    return unknownSema

def freezeSet(elems):
    res = set()
    for elem in elems:
        elementCopy = copy.copy(elem)
        elementCopy.freeze()
        res.add(elementCopy)
    return res

def freezeDict(elems):
    res = {}
    for key, val in elems.items():
        keyCopy = copy.copy(key)
        keyCopy.freeze()
        valCopy = frozenset(freezeSet(val))
        res[keyCopy] = valCopy
    return res
