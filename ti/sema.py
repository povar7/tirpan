'''
Created on 26.05.2013

@author: bronikkk
'''

import copy
import types

import utils

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

class LiteralSema(Sema):

    def __init__(self, ltype):
        super(LiteralSema, self).__init__()
        assert(ltype not in (str, unicode))
        self.ltype = ltype

    def isInstanceEqualTo(self, other):
        return self.ltype == other.ltype

    def getInstanceHash(self):
        return hash(self.ltype)

class LiteralValueSema(LiteralSema):

    def __init__(self, value):
        if isinstance(value, basestring):
            lclass = basestring
        else:
            lclass = value.__class__
        super(LiteralValueSema, self).__init__(lclass)
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
        for index in range(size + 1 if size != None else 0):
            self.elems.append(set())

    def isInstanceEqualTo(self, other):
        assert self.frozen == other.frozen
        if self.frozen:
            return self.elems == other.elems
        else:
            return self is other

    def getInstanceHash(self):
        if self.frozen:
            return hash(frozenset(self.elems))
        else:
            return id(self)

    def copy(self):
        res = copy.copy(self)
        res.elems = [elem.copy() for elem in self.elems]
        return res

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
    
    def __init__(self, default = False):
        super(DictSema, self).__init__()
        self.elems   = dict()
        self.default = default

    def isInstanceEqualTo(self, other):
        assert self.frozen == other.frozen
        if self.frozen:
            return self.elems == other.elems
        else:
            return self is other

    def getInstanceHash(self):
        if self.frozen:
            return hash(frozenset(self.elems.items()))
        else:
            return id(self)

    def copy(self):
        res = DictSema()
        for key, val in self.elems.items():
            res.elems[key] = val.copy()
        return res

    def freeze(self):
        self.elems = freezeDict(self.elems)
        self.frozen = True

class SetSema(CollectionSema):
    
    def __init__(self):
        super(SetSema, self).__init__()
        self.elems = set()

    def isInstanceEqualTo(self, other):
        assert self.frozen == other.frozen
        if self.frozen:
            return self.elems == other.elems
        else:
            return self is other

    def getInstanceHash(self):
        if self.frozen:
            return hash(frozenset(self.elems.items()))
        else:
            return id(self)

    def copy(self):
        res = SetSema()
        res.elems = self.elems.copy()
        return res

    def freeze(self):
        self.elems = freezeSet(self.elems)
        self.frozen = True

class FunctionSema(Sema):

    def __init__(self, origin, parent):
        super(FunctionSema, self).__init__()
        self.origin = origin
        self.parent = parent

    def isInstanceEqualTo(self, other):
        return self is other

    def getInstanceHash(self):
        return id(self)

    def getOrigin(self):
        return self.origin

    def getParent(self):
        return self.parent

class ScopeInterface(object):

    def addVariable(self, var):
        variables = self.getVariables()
        variables[var.name] = var

    def findName(self, name,
                 considerGlobals = False, scopeWrap = None):
        variables = self.getVariables()
        if name in variables:
            return variables[name]
        if (considerGlobals and
            self.hasGlobals() and name not in self.getGlobalNames()):
            if scopeWrap:
                scopeWrap.scope = None
            return None
        parent = self.getParent()
        if parent:
            if considerGlobals and isinstance(self, ModuleSema):
                return None
            return parent.findName(name, considerGlobals, scopeWrap)

    def findOrAddName(self, name,
                      considerGlobals = False, fileScope = None):
        scopeWrap = ScopeWrap(fileScope)
        res = self.findName(name, considerGlobals, scopeWrap)
        fileScope = scopeWrap.scope
        if not res:
            from ti.tgnode import VariableTGNode
            res = VariableTGNode(name)
            if considerGlobals and fileScope:
                fileScope.addVariable(res)
            else:
                scope = self.getScopeForAdding()
                scope.addVariable(res)
        return res

    def findNameHere(self, name):
        variables = self.getVariables()
        if name in variables:
            return variables[name]
        return None

    def getScopeForAdding(self):
        return self

class ScopeSema(Sema, ScopeInterface):

    def __init__(self, parent = None, add = True):
        super(ScopeSema, self).__init__()
        self.add       = add
        self.parent    = parent
        self.variables = dict()

    def hasGlobals(self):
        return False

    def getParent(self):
        return self.parent

    def getScopeForAdding(self):
        if self.add:
            return self
        parent = self.getParent()
        if parent:
            return parent.getScopeForAdding()
        else:
            return None

    def getVariables(self):
        return self.variables

    def addGlobalNames(self, names):
        parent = self.getParent()
        if parent:
            parent.addGlobalNames(names)

class ClassSema(Sema, ScopeInterface):
   
    def __init__(self, origin):
        super(ClassSema, self).__init__()
        self.origin = origin

    def getBody(self):
        origin = self.getOrigin()
        return origin.getBody()

    def getClassInstance(self):
        from ti.tgnode import VariableTGNode
        inst = InstanceSema(self)
        origin = self.getOrigin()
        var = VariableTGNode('__class__', {self})
        inst.getBody().addVariable(var)
        return inst

    def getGlobalNames(self):
        return set()

    def getOrigin(self):
        return self.origin

    def getParent(self):
        origin = self.getOrigin()
        return origin.getParent()

    def getVariables(self):
        scope = self.getBody()
        return scope.variables

    def hasGlobals(self):
        return True

    def isInstanceEqualTo(self, other):
        return self is other

    def getInstanceHash(self):
        return id(self)

class InstanceSema(Sema, ScopeInterface):

    def __init__(self, stub):
        super(InstanceSema, self).__init__()

        self.body = ScopeSema()
        self.stub = stub

    def getBody(self):
        return self.body

    def getStub(self):
        return self.stub

    def isInstanceEqualTo(self, other):
        return self is other

    def getInstanceHash(self):
        return id(self)

class TemplateSema(Sema, ScopeInterface):

    def __init__(self, origin):
        super(TemplateSema, self).__init__()
        self.origin = origin

    def addGlobalNames(self, names):
        globalNames  = self.getGlobalNames()
        globalNames |= set(names)

    def getGlobalNames(self):
        origin = self.getOrigin()
        return origin.function.globalNames

    def getParent(self):
        origin = self.getOrigin()
        return origin.getParent()

    def getVariables(self):
        origin = self.getOrigin()
        scope  = origin.getParams()
        return scope.getVariables()

    def hasGlobals(self):
        origin = self.getOrigin()
        return True

    def getOrigin(self):
        return self.origin

class ModuleSema(Sema, ScopeInterface):

    def __init__(self, origin):
        super(ModuleSema, self).__init__()
        self.origin = origin

    def isInstanceEqualTo(self, other):
        return self is other

    def getInstanceHash(self):
        return id(self)

    def getBody(self):
        origin = self.getOrigin()
        return origin.getBody()

    def getParent(self):
        origin = self.getOrigin()
        return origin.getParent()

    def getVariables(self):
        scope = self.getBody()
        return scope.variables

    def hasGlobals(self):
        return False

    def getOrigin(self):
        return self.origin

def freezeSet(elems):
    res = set()
    for elem in elems:
        elementCopy = copy.copy(elem)
        elementCopy.freeze()
        res.add(elementCopy)
    return res

def freezeDict(elems):
    res = dict()
    for key, val in elems.items():
        keyCopy = copy.copy(key)
        keyCopy.freeze()
        valCopy = frozenset(freezeSet(val))
        res[keyCopy] = valCopy
    return res

def isString(sema):
    try:
        return sema.ltype == basestring
    except AttributeError:
        return False

boolSema = LiteralSema(bool)

def getBoolSema():
    return boolSema

noneSema = LiteralSema(types.NoneType)

def getNoneSema():
    return noneSema
