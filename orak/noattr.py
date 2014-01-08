'''
Created on 03.01.2014

@author: bronikkk
'''

import ast

import config

from orak.api     import *
from orak.defects import *
from ti.sema      import *
from utils        import *

class NoAttributeDefect(Defect):

    def __init__(self, node, obj, name):
        super(NoAttributeDefect, self).__init__(node)
        self._kind  = 'NOATTR'
        self._descr = '%s has no attribute \'%s\'.' % (obj.getString(), name)
        self._msg   = 'Tirpan traceback (most recent call last):\n' + \
                      config.data.backTrace.get()

        self._obj = obj.copy()
        self._obj.freeze()

    def instance_hash(self):
        line = getLine      (self._node)
        col  = getColumn    (self._node)
        fno  = getFileNumber(self._node)
        pos  = (line, col, fno)
        return hash((pos, self._obj))

def objCondition(sema, name):
    if orak_isExternalModule(sema) or orak_isFunction(sema):
        return False
    return (not orak_hasName(sema, name) and
            not orak_hasName(sema, '__metaclass__'))

def checkNoAttribute(node):
    objLink = orak_getLink(node.value)
    if not objLink:
        return

    btrace  = config.data.backTrace
    handler = config.data.defectsHandler
    scope   = config.data.currentScope

    first_time = True
    name = node.attr

    for obj in orak_getNodeType(objLink):
        if objCondition(obj, name):
            if first_time:
                first_time = False
                function = QuasiFunction('<.%s>' % name)
            args = (obj,)
            btrace.addFrame(node, scope, function, args) 
            handler.addDefect(NoAttributeDefect(node, obj, name))
            btrace.deleteFrame()

def noattrChecker():
    orak_registerCallback(ast.Attribute, checkNoAttribute)