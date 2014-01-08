'''
Created on 23.12.2013

@author: bronikkk
'''

import utils

from ti.lookup import lookupVariable
from ti.sema   import *

import ti.tgnode

from orak.register import CallbacksRegister

callbacks = CallbacksRegister.get_instance()

def orak_getLink(node):
    try:
        return utils.getLink(node)
    except:
        return None

def orak_getName(sema):
    try:
        origin = sema.getOrigin()
        return origin.getNodeName()
    except:
        return None

def orak_getNodeType(link):
    try:
        return link.nodeType
    except:
        return None

def orak_getOrigin(sema):
    try:
        return sema.getOrigin()
    except:
        return None

def orak_getQualifiedName(sema):
    try:
        parent = sema.getParent()
    except:
        parent = None
    try:
        if parent:
            prefix = orak_getQualifiedName(parent)
        else:
            prefix = ''
    except:
        prefix = ''
    try:
        origin = sema.getOrigin()
    except:
        origin = None
    try:
        name = origin.getNodeName()
    except:
        name = ''
    if prefix != '' and name != '':
        return prefix + '.' + name
    else:
        return name

def orak_hasName(sema, name):
    try:
        var = lookupVariable(sema, name)
        return var is not None
    except:
        return False

def orak_isBasestring(sema):
    try:
        return isBasestring(sema) 
    except:
        return False

def orak_isExternalModule(sema):
    try:
        if not isinstance(sema, ModuleSema):
            return False
        origin = sema.getOrigin()
        return isinstance(origin, ti.tgnode.ExternalModuleTGNode)
    except:
        return False

def orak_isFunction(sema):
    return isinstance(sema, FunctionSema)

def orak_initializeCallbacks():
    callbacks.initialize()

def orak_invokeCallbacks(node):
    callbacks.invokeCallbacks(node)

def orak_registerCallback(kind, callback):
    callbacks.registerCallback(kind, callback)
