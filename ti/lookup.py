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
    if isinstance(obj, CollectionSema):
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

def lookupVariable(obj, attr):
    if isinstance(obj, CollectionSema):
        lookupScope = replaceStandardCollections(obj)
        return lookupScope.findNameHere(attr)
    return None
