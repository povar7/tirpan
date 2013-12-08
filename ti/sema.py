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

    def copy(self):
        return self

    def freeze(self):
        pass

    def getElementsAtIndex(self, index):
        return set()

    def getLink(self, node):
        parent = self.getParent()
        if parent:
            return parent.getLink(node)
        else:
            return node.link

    def getNumberOfElements(self):
        return 0

    def getString(self):
        return '?'

    def setLink(self, node, value):
        parent = self.getParent()
        if parent:
            parent.setLink(node, value)
        else:
            node.link = value

class LiteralSema(Sema):

    def __init__(self, ltype):
        super(LiteralSema, self).__init__()
        self.ltype = ltype

    def isInstanceEqualTo(self, other):
        return self.ltype == other.ltype

    def getInstanceHash(self):
        return hash(self.ltype)

    def getString(self):
        if self.ltype == types.NoneType:
            return None.__repr__()
        else:
            return '<%s value>' % str(self.ltype)

class LiteralValueSema(LiteralSema):

    def __init__(self, value):
        super(LiteralValueSema, self).__init__(value.__class__)
        self.value = value

    def isInstanceEqualTo(self, other):
        return (self.ltype == other.ltype and
                self.value == other.value)

    def getInstanceHash(self):
        return hash((self.ltype, self.value))

    def getString(self):
        return self.value.__repr__()

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
            if index is None or isinstance(index, (int, long)):
                return self.getElements()
            else:
                return set()

    def getNumberOfElements(self):
        return max(0, len(self.elems) - 1)

    def addElements(self, values):
        for elem in self.elems:
            elem |= values

    def addElementsAtIndex(self, index, values):
        assert not self.frozen
        try:
            self.elems[index + 1] |= values
        except:
            self.addElementsAtKey(index, values)

    def addElementsAtKey(self, key, values):
        self.elems[0] |= values

    def getElementsAtKey(self, key):
        return self.getElements()

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

    def getString(self):
        res = ''
        if isinstance(self, TupleSema):
            res += '('
        else:
            res += '['
        first = True
        for elem in self.getElements():
            if not first:
                res += ', '
            else:
                first = False
            res += elem.getString()
        if isinstance(self, TupleSema):
            res += ')'
        else:
            res += ']'
        return res

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

    def getElementsAtIndex(self, index):
        return set(self.elems.keys())

    def getElementsAtKey(self, key):
        try:
            return self.elems[key]
        except:
            res = set()
            if self.default:
                res.add(ListSema())
            return res

    def getElements(self):
        return self.getElementsAtIndex(None)

    def addElementsAtKey(self, key, values):
        try:
            oldValue = self.elems[key]
        except:
            res = set()
            if self.default:
                res.add(ListSema())
            oldValue = self.elems[key] = res
        oldValue |= values

    def copy(self):
        res = DictSema()
        for key, val in self.elems.items():
            res.elems[key] = val.copy()
        return res

    def freeze(self):
        self.elems = freezeDict(self.elems)
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

    def getString(self):
        if self.origin.name:
            return self.origin.name
        else:
            return '<lambda>'

class ScopeInterface(object):

    def addVariable(self, var):
        var.setParent(self)
        variables = self.getVariables()
        variables[var.name] = var

    def findName(self, name,
                 considerGlobals = False,
                 scopeWrap       = None ,
                 loseName        = False):
        variables = self.getVariables()
        if name in variables:
            if loseName:
                del variables[name]
                return None
            else:
                return variables[name]
        if (considerGlobals and
            self.hasGlobals() and name not in self.getGlobalNames()):
            if scopeWrap:
                scopeWrap.scope = None
            return None
        parent = self.getParent()
        if parent:
            return parent.findName(name, considerGlobals, scopeWrap, loseName)
        return None

    def findOrAddName(self, name,
                      considerGlobals = False,
                      fileScope       = None ,
                      loseName        = False):
        scopeWrap = ScopeWrap(fileScope)
        res = self.findName(name, considerGlobals, scopeWrap, loseName)
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
        self.variables = {}

    def hasGlobals(self):
        return False
 
    def getParent(self):
        return self.parent

    def getVariables(self):
        return self.variables

    def connectReturn(self, node):
        parent = self.getParent()
        if parent:
            parent.connectReturn(node)

    def connectYield(self, node):
        parent = self.getParent()
        if parent:
            parent.connectYield(node)

    def addGlobalNames(self, names):
        parent = self.getParent()
        if parent:
            parent.addGlobalNames(names)

    def setGlobalDestructive(self):
        parent = self.getParent()
        if parent:
            parent.setGlobalDestructive()

    def getScopeForAdding(self):
        if self.add:
            return self
        parent = self.getParent()
        if parent:
            return parent.getScopeForAdding()
        else:
            return None

    def getString(self):
        parent = self.getParent()
        if parent:
            return parent.getString()
        else:
            return '?'

class ClassSema(Sema, ScopeInterface):
   
    def __init__(self, origin):
        super(ClassSema, self).__init__()
        self.origin = origin

    def getBody(self):
        return self.origin.getBody()

    def getClassInstance(self):
        from ti.tgnode import VariableTGNode
        inst = InstanceSema(self)
        self.origin.addInstance(inst)
        var = VariableTGNode('__class__', {self})
        inst.getBody().addVariable(var)
        return inst

    def getInstancesNumber(self):
        return self.origin.getInstancesNumber()

    def getGlobalNames(self):
        return set() 

    def getParent(self):
        return self.origin.getParent()

    def getVariables(self):
        scope = self.getBody()
        return scope.variables

    def hasGlobals(self):
        return True

    def isInstanceEqualTo(self, other):
        return self is other

    def getInstanceHash(self):
        return id(self)

    def getString(self):
        return '<class %s>' % self.origin.name

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

    def getString(self):
        return '<%s object>' % self.stub.origin.name

    def isSingleton(self):
        stub = self.getStub()
        return stub.getInstancesNumber() == 1

class TemplateSema(Sema, ScopeInterface):

    def __init__(self, origin):
        super(TemplateSema, self).__init__()
        self.origin = origin

    def addGlobalNames(self, names):
        globalNames  = self.getGlobalNames()
        globalNames |= set(names)

    def getGlobalNames(self):
        return self.origin.function.globalNames

    def getParent(self):
        return self.origin.getParent()

    def getVariables(self):
        scope = self.origin.getParams()
        return scope.getVariables()

    def hasGlobals(self):
        from ti.tgnode import ForFunctionDefinitionTGNode
        if isinstance(self.origin.function, ForFunctionDefinitionTGNode):
            return False
        return True

    def connectReturn(self, node):
        from ti.tgnode import EdgeType, ForFunctionDefinitionTGNode
        origin = self.origin
        if isinstance(origin.function, ForFunctionDefinitionTGNode):
            origin.parent.connectReturn(node)
        else:
            utils.getLink(node).addEdge(EdgeType.ASSIGN, origin)

    def connectYield(self, node):
        from ti.tgnode import EdgeType, ForFunctionDefinitionTGNode
        origin = self.origin
        if isinstance(origin.function, ForFunctionDefinitionTGNode):
            origin.parent.connectYield(node)
        else:
            utils.getLink(node).addEdge(EdgeType.ASSIGN_YIELD, origin)

    def setGlobalDestructive(self):
        function = self.origin.function
        function.setGlobalDestructive()

    def getLink(self, node):
        try:
            return self.origin.mapping[node]
        except KeyError:
            return self.getParent().getLink(node)

    def getString(self):
        function = self.origin.function
        if function.name:
            return function.name
        else:
            return '<lambda>'

    def setLink(self, node, value):
        self.origin.mapping[node] = value

class ModuleSema(Sema, ScopeInterface):

    def __init__(self, origin):
        super(ModuleSema, self).__init__()
        self.origin = origin

    def isInstanceEqualTo(self, other):
        return self is other

    def getInstanceHash(self):
        return id(self)

    def getBody(self):
        return self.origin.getBody()

    def getParent(self):
        return self.origin.getParent()

    def getVariables(self):
        scope = self.getBody()
        return scope.variables

    def hasGlobals(self):
        return False

    def setGlobalDestructive(self):
        pass

    def getString(self):
        return '<module>'

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
