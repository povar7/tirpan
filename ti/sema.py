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

class ListOrTupleSema(CollectionSema):
    
    def __init__(self, size = None):
        super(ListOrTupleSema, self).__init__()
        self.elems = []
        for index in range(size + 1 if size is not None else 0):
            self.elems.append(set())

    def getElements(self):
        res = set()
        for elem in self.elems:
            res |= elem
        return res

    def getElementsAtIndex(self, index):
        try:
            return self.elems[index + 1]
        except:
            return self.getElements()

    def addElements(self, values):
        for elem in self.elems:
            elem |= values

    def addElementsAtIndex(self, index, values):
        assert(not self.frozen)
        try:
            self.elems[index + 1] |= values
        except:
            self.addElementsAtKey(index, values)

    def addElementsAtKey(self, key, values):
        self.elems[0] |= values

    def getElementsAtKey(self, key):
        return self.getElements()

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
        res = []
        for atom in self.elems:
            atomCopy = frozenset(freezeSet(atom))
            res.append(atomCopy)
        self.elems  = res
        self.frozen = True

class ListSema(ListOrTupleSema):

    def __init__(self, size = 0):
        super(ListSema, self).__init__(size)

class TupleSema(ListOrTupleSema):

    def __init__(self, size = 0):
        super(TupleSema, self).__init__(size)

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

    def getElementsAtIndex(self, index):
        return set(self.elems.keys())

    def getElementsAtKey(self, key):
        try:
            return self.elems[key]
        except:
            return set()

    def addElementsAtKey(self, key, values):
        try:
            oldValue = self.elems[key]
        except:
            oldValue = self.elems[key] = set()
        oldValue |= values

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
