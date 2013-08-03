'''
Created on 03.08.2013

@author: bronikkk
'''

import ast
import copy

from ti.sema import *
from utils   import *

unknownSema = NoSema()

class DefectsHandler(object):

    def __init__(self):
        self._defects = set()

    def addDefect(self, defect):
        self._defects.add(defect)

    def getDefects(self):
        return self._defects

    def printDefects(self):
        for defect in self._defects:
            print defect

class Defect(object):

    def __init__(self, node):
        self._node  = node
        self._kind  = None
        self._descr = None

    def __repr__(self):
        return '%s: %s' % (self._kind, self._descr)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.instance_hash() == other.instance_hash())
       
    def __hash__(self):
        return hash((self.__class__, self.instance_hash()))

    def instance_hash(self):
        return hash(self._descr)

class FuncArgDefect(Defect):

    def __init__(self, node, arg):
        super(FuncArgDefect, self).__init__(node)
        self._kind  = 'FUNC.ARG'
        self._descr = '\'os.path.basename\' expects ' + \
                      '<basestring object>, not %s.' % arg

        self._arg = arg.copy()
        self._arg.freeze()

    def instance_hash(self):
        line = getLine      (self._node)
        col  = getColumn    (self._node)
        fno  = getFileNumber(self._node)
        pos  = (line, col, fno)
        return hash((pos, self._arg))

def checkBasenameCall(node):
    import config

    if not isinstance(node, ast.Call):
        return
    
    funcType = node.func.link.nodeType

    def funcCondition(x):
        from ti.tgnode import ExternalFunctionDefinitionTGNode
        if not isinstance(x, FunctionSema):
            return False
        origin = x.origin
        if not isinstance(origin, ExternalFunctionDefinitionTGNode):
            return False
        return origin.name == 'basename'

    if not any(funcCondition(elem) for elem in funcType):
        return

    try:
        argType = node.args[0].link.nodeType
    except:
        return

    def argCondition(x):
        if x == unknownSema:
            return False
        if isinstance(x, LiteralSema) and x.ltype in (str, unicode):
            return False
        return True

    for elem in argType:
        if argCondition(elem):
            defectsHandler = config.data.defectsHandler
            defectsHandler.addDefect(FuncArgDefect(node, elem)) 
