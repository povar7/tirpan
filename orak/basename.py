'''
Created on 03.08.2013

@author: bronikkk
'''

import config

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
            handler.addDefect(BasenameDefect(node, arg))
            btrace.deleteFrame()
