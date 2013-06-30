'''
Created on 15.06.2013

@author: bronikkk
'''

import copy

from ti.builtin import getListClass
from ti.sema    import *

def replaceStandardCollections(obj):
    if isinstance(obj, ListSema):
        return getListClass()
    else:
        return obj

def lookupTypes(obj, attr):
    res = set()
    var = lookupVariable(obj, attr)
    if var is None:
        return set()
    if isinstance(obj, (CollectionSema, InstanceSema)):
        for elem in var.nodeType:
            if isinstance(elem, FunctionSema):
                elemCopy = copy.copy(elem)
                elemCopy.parent = obj
                res.add(elemCopy)
            else:
                res.add(elem)
    else:
        res |= var.nodeType
    return res

def lookupVariable(obj, attr, setValue = False, createNew = False):
    from ti.tgnode import VariableTGNode
    var = None
    if isinstance(obj, CollectionSema):
        lookupScope = replaceStandardCollections(obj)
        var = lookupScope.findNameHere(attr)
    elif isinstance(obj, ClassSema):
        lookupScope = obj.getBody()
        var = lookupScope.findNameHere(attr)
        if var:
            return var
        for base in obj.origin.getBases():
            for elem in base.link.nodeType:
                if not isinstance(elem, ClassSema):
                    continue
                var = lookupVariable(elem, attr)
                if var:
                    return var
    elif isinstance(obj, InstanceSema):
        lookupScope = obj.getBody()
        var = lookupScope.findNameHere(attr)
        if var:
            return var
        if createNew:
            var = VariableTGNode(attr)
            lookupScope.addVariable(var)
            return var
        if not setValue:
            var = lookupVariable(obj.getStub(), attr)
    elif isinstance(obj, (ModuleSema, PackageSema)):
        lookupScope = obj.getBody()
        var = lookupScope.findNameHere(attr)
    return var 
