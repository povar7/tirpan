'''
Created on 03.08.2013

@author: bronikkk
'''

import ast

import config

from orak.api     import *
from orak.defects import *
from ti.sema      import *
from utils        import *

class BasenameDefect(Defect):

    def __init__(self, node, arg):
        super(BasenameDefect, self).__init__(node)
        self._kind  = 'BASENAME'
        self._descr = '\'os.path.basename\' expects ' + \
                      '<basestring object>, not %s.' % arg.getString()
        self._msg   = 'Tirpan traceback (most recent call last):\n' + \
                      config.data.backTrace.get()

        self._arg = arg.copy()
        self._arg.freeze()

    def instance_hash(self):
        line = getLine      (self._node)
        col  = getColumn    (self._node)
        fno  = getFileNumber(self._node)
        pos  = (line, col, fno)
        return hash((pos, self._arg))

def funcCondition(sema):
    return (orak_isFunction(sema) and
            orak_getQualifiedName(sema) == 'os.path.basename')

def argCondition(sema):
    return not orak_isBasestring(sema)

def checkBasenameCall(node):
    funcLink = orak_getLink(node.func)
    if not funcLink:
        return

    function = None
    for elem in orak_getNodeType(funcLink):
        if funcCondition(elem):
            function = elem
            break

    if not function:
        return

    argLink = orak_getLink(node.args[0])
    if not argLink:
        return

    btrace  = config.data.backTrace
    handler = config.data.defectsHandler
    scope   = config.data.currentScope

    for arg in orak_getNodeType(argLink):
        if argCondition(arg):
            args = (arg,)
            btrace.addFrame(node, scope, function, args) 
            handler.addDefect(BasenameDefect(node, arg))
            btrace.deleteFrame()

def basenameChecker():
    orak_registerCallback(ast.Call, checkBasenameCall)
