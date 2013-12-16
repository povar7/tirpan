'''
Created on 03.08.2013

@author: bronikkk
'''

import ast
import copy

import config
from   ti.sema import *
from   utils   import *

class DefectsHandler(object):

    def __init__(self):
        self._defects = set()

    def addDefect(self, defect):
        self._defects.add(defect)

    def getDefects(self):
        return self._defects

    def printDefects(self):
        first = True
        for defect in self._defects:
            if first:
                first = False
            else:
                print
            print defect

class Defect(object):

    def __init__(self, node):
        self._node  = node
        self._msg   = None
        self._kind  = None
        self._descr = None

    def __repr__(self):
        return self._msg + self._kind + ': ' + self._descr

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.instance_hash() == other.instance_hash())
       
    def __hash__(self):
        return hash((self.__class__, self.instance_hash()))

    def instance_hash(self):
        return hash(self._descr)

class FuncArgWrongDefect(Defect):

    def __init__(self, node, arg):
        super(FuncArgWrongDefect, self).__init__(node)
        self._kind  = 'FUNC.ARG.WRONG'
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

def checkBasenameCall(node):
    def funcCondition(x):
        from ti.tgnode import ExternalFunctionDefinitionTGNode
        if not isinstance(x, FunctionSema):
            return False
        origin = x.origin
        if not isinstance(origin, ExternalFunctionDefinitionTGNode):
            return False
        return origin.name == 'basename'

    try:
        funcLink = getLink(node.func)
    except:
        return

    function = None
    for elem in funcLink.nodeType:
        if funcCondition(elem):
            function = elem
            break

    if not function:
        return

    try:
        argLink = getLink(node.args[0])
    except:
        return

    def argCondition(x):
        if isinstance(x, LiteralSema) and x.ltype in (str, unicode):
            return False
        return True

    btrace  = config.data.backTrace
    handler = config.data.defectsHandler
    scope   = config.data.currentScope

    for arg in argLink.nodeType:
        if argCondition(arg):
            args = (arg,)
            btrace.addFrame(node, scope, function, args) 
            handler.addDefect(FuncArgWrongDefect(node, arg))
            btrace.deleteFrame()
