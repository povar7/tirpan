'''
Created on 15.06.2013

@author: bronikkk
'''

import ast
import copy

from ti.builtin import getBaseStringClass, getDictClass, getListClass
from ti.sema    import *
from utils      import *

def replaceStandardCollections(obj):
    if isinstance(obj, ListSema):
        return getListClass()
    elif isinstance(obj, DictSema):
        return getDictClass()
    elif (isinstance(obj, LiteralSema) and
          obj.ltype in (str, unicode)):
        return getBaseStringClass()
    else:
        return None

def lookupTypes(obj, attr):
    res = set()
    var = lookupVariable(obj, attr)
    if var is None:
        return set()
    if isinstance(obj, (CollectionSema, LiteralSema, InstanceSema)):
        for elem in var.nodeType:
            if isinstance(elem, FunctionSema):
                elemCopy = copy.copy(elem)
                if not isinstance(elemCopy.parent, InstanceSema):
                    elemCopy.parent = obj
                res.add(elemCopy)
            else:
                res.add(elem)
    else:
        res |= var.nodeType
    return res

def setTypes(obj, attr, values):
    from ti.tgnode import EdgeType
    var = lookupVariable(obj, attr, True, len(values) > 0)
    if var is not None:
        EdgeType.updateRight(var, values)

def lookupVariable(obj, attr, setValue = False, createNew = False, aux = None):
    from ti.tgnode import FunctionCallTGNode, VariableTGNode
    var = None
    if (isinstance(obj, CollectionSema) or
        isinstance(obj, LiteralSema)):
        lookupScope = replaceStandardCollections(obj)
        if lookupScope:
            var = lookupScope.findNameHere(attr)
    elif isinstance(obj, ClassSema):
        lookupScope = obj.getBody()
        var = lookupScope.findNameHere(attr)
        if var:
            return var
        if (aux is not None and attr != '__getattr__' and
            not setValue and not createNew):
            attrTypes = lookupTypes(aux, '__getattr__')
        else:
            attrTypes = set()
        if len(attrTypes) > 0:
            attrVar  = VariableTGNode(None, {LiteralValueSema(attr)})
            args     = [QuasiNode(attrVar)]
            attrFunc = VariableTGNode(None, attrTypes)
            func     = QuasiNode(attrFunc)
            quasiCall = QuasiCall(func, args)
            return FunctionCallTGNode(quasiCall)
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
            var = lookupVariable(obj.getStub(), attr, False, False, obj)
    elif isinstance(obj, ModuleSema):
        lookupScope = obj.getBody()
        var = lookupScope.findNameHere(attr)
    return var

operatorNames = {
                    ast.Add      : '+' ,
                    ast.BitAnd   : '&' ,
                    ast.BitOr    : '|' ,
                    ast.Div      : '/' ,
                    ast.FloorDiv : '//',
                    ast.LShift   : '<<',
                    ast.Mult     : '*' ,
                    ast.Mod      : '%' ,
                    ast.RShift   : '>>',
                    ast.Sub      : '-' ,
                    ast.Pow      : '**',
                    ast.UAdd     : '+' ,
                    ast.USub     : '-' ,
                    ast.Invert   : '~' ,
                    ast.Not      : '!' ,
                }

def getOperatorName(node):
    return operatorNames[node.__class__]
