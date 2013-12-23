'''
Created on 18.08.2013

@author: bronikkk
'''

from ti.sema import *
from utils   import *

def stringFrom(element):
    try:
        return element.getString()
    except AttributeError:
        return None.__repr__()

class BackTrace(object):

    def __init__(self):
        self._backtrace = []

    def addFrame(self, node, scope, function, args):
        frame = (node, scope, function, args)
        self._backtrace.append(frame)

    def deleteFrame(self):
        self._backtrace.pop()

    def get(self):
        res = ''

        for frame in self._backtrace:
            node, scope, func, args = frame

            res += ' ' * 2

            filename = getFileName(node)
            if not filename:
                filename = '?'

            line = getLine(node)
            if not line:
                line = '?'

            scopeName = stringFrom(scope)
          
            res += 'File "%s", line %s, in %s:\n' % (filename, line, scopeName)

            res += ' ' * 4

            parent = func.parent
            if isinstance(parent, InstanceSema):
                res += '%s.' % stringFrom(parent)
                printedArgs = args[1:]
            else:
                printedArgs = args

            if isinstance(parent, ModuleSema):
                from ti.tgnode import ExternalModuleTGNode
                origin = parent.getOrigin()
                if isinstance(origin, ExternalModuleTGNode):
                    res += '%s.' % origin.getAliasName()

            res += stringFrom(func)

            res += '('
            firstArg = True

            for arg in printedArgs:
                if not firstArg:
                    res += ', '
                else:
                    firstArg = False
                res += stringFrom(arg)

            res += ')'
            res += '\n'

        return res 
