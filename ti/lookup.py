'''
Created on 15.06.2013

@author: bronikkk
'''

import copy
import sys

import ti.sema
import ti.tgnode

classes = (ti.sema.CollectionSema, ti.sema.LiteralSema, ti.sema.InstanceSema)
NOATTR_MSG = 'AttributeError: %s has no attribute \'%s\''

def getFunctions(functionNode):
    for elem in functionNode.nodeType:
        if isinstance(elem, ti.sema.FunctionSema):
            yield elem, False
        elif isinstance(elem, ti.sema.ClassSema):
            lookupScope = elem.getBody()
            var = lookupScope.findNameHere('__init__')
            if var:
                for atom in var.nodeType:
                    if isinstance(atom, ti.sema.FunctionSema):
                        yield atom, True
            else:
                yield elem, True

def getTypes(objects, attr):
    types = set()
    for obj in objects:
        types |= getTypesForObject(obj, attr)
    return types

def getTypesForObject(obj, attr):
    types = set()
    var = getVariableForObject(obj, attr)
    if not var:
        print >> sys.stderr, NOATTR_MSG % (obj.getString(), attr)
        return types
    if isinstance(obj, classes):
        for elem in var.nodeType:
            if isinstance(elem, ti.sema.FunctionSema):
                elemCopy = copy.copy(elem)
                if not isinstance(elemCopy.parent, ti.sema.InstanceSema):
                    elemCopy.parent = obj
                types.add(elemCopy)
            else:
                types.add(elem)
    else:
        types |= var.nodeType
    return types

def getVariableForObject(obj, attr):
    if isinstance(obj, ti.sema.InstanceSema):
        lookupScope = obj.getBody()
        var = lookupScope.findNameHere(attr)
        if var:
            return var
        else:
            return getVariableForObject(obj.getStub(), attr)
    elif isinstance(obj, ti.sema.ClassSema):
        lookupScope = obj.getBody()
        var = lookupScope.findNameHere(attr)
        return var

def setTypes(objects, attr, types):
    for obj in objects:
        setTypesForObject(obj, attr, types)

def setTypesForObject(obj, attr, types):
    if isinstance(obj, ti.sema.InstanceSema):
        lookupScope = obj.getBody()
        var = lookupScope.findNameHere(attr)
        if not var:
            var = ti.tgnode.VariableTGNode(attr)
            lookupScope.addVariable(var)
        ti.tgnode.replaceSet(var.nodeType, types)
