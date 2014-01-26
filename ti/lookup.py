'''
Created on 15.06.2013

@author: bronikkk
'''

import copy
import sys

import ti.sema
import ti.tgnode
import utils

classes = (ti.sema.CollectionSema, ti.sema.LiteralSema, ti.sema.InstanceSema)
NOATTR_MSG = 'AttributeError: %s has no attribute \'%s\''

class QuasiVar(object):

    def __init__(self):
        self.nodeType = set()

def addNewType(var, elem, cond):
    types = var.nodeType
    if cond:
        if isinstance(types, set):
            types = {}
        types[elem] = cond
    else:
        types.add(elem)
    var.nodeType = types

def getCondition(conj):
    res = ''
    first = True
    value = sorted(conj, sortIfs)
    for if_node, flag in conj:
        filename = utils.getFileName(if_node.node)
        lineno   = utils.getLine    (if_node.node)
        if first:
            first = False
            prefix = ''
        else:
            prefix = ' and '
        added = '%s:%d == %s' % (filename, lineno, flag)
        res += prefix + added
    return res

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

def getTypes(objects, attr, stack):
    res_var = QuasiVar()
    types = set()
    for obj in objects:
        try:
            cond = objects[obj]
        except TypeError:
            cond = set()
        new_types = getTypesForObject(obj, attr, cond, stack)
        for elem in new_types:
            try:
                cond = new_types[elem]
            except TypeError:
                cond = set()
            addNewType(res_var, elem, cond)
    return res_var.nodeType

def getTypesForObject(obj, attr, cond, stack):
    var = getVariableForObject(obj, attr)
    if not var:
        print >> sys.stderr, NOATTR_MSG % (obj.getString(), attr)
        if not cond:
            print >> sys.stderr, '\tCondition: always'
        else:
            printCondition(cond)
            obj = ti.tgnode.findDefault(cond)
            if obj:
                printCondition(obj.data)
        return set()
    res_var = QuasiVar() 
    for elem in var.nodeType:
        try:
            cond = var.nodeType[elem]
        except TypeError:
            cond = set()
        if isinstance(obj, classes) and isinstance(elem, ti.sema.FunctionSema):
            elemCopy = copy.copy(elem)
            if not isinstance(elemCopy.parent, ti.sema.InstanceSema):
                elemCopy.parent = obj
            addNewType(res_var, elemCopy, cond)
        else:
            addNewType(res_var, elem    , cond)
    return res_var.nodeType

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

def printCondition(cond):
    for elem in cond:
        if not isinstance(elem, ti.tgnode.Default):
            print >> sys.stderr, '\tCondition: ' + getCondition(elem)

def setTypes(objects, attr, types, stack):
    for obj in objects:
        setTypesForObject(obj, attr, types, stack)

def setTypesForObject(obj, attr, types, stack):
    if isinstance(obj, ti.sema.InstanceSema):
        lookupScope = obj.getBody()
        var = lookupScope.findNameHere(attr)
        if not var:
            var = ti.tgnode.VariableTGNode(attr)
            lookupScope.addVariable(var)
        ti.tgnode.replaceTypes(var, types, stack)

def sortIfs(x, y):
    return utils.getLine(x[0].node) < utils.getLine(y[0].node)
