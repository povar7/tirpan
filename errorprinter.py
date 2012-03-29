'''
Created on 05.02.2012

@author: bronikkk
'''

import __main__

from ast   import BinOp, UnaryOp, Call
from init  import get_operator_name
from utils import getLine, getCol, getFile

class ErrorPrinter(object):
    def printError(self, error):
        if __main__.verbose:
            print error

class TirpanError(object):
    def __init__(self):
        self.prefix = 'Tirpan error: '

class CallNotResolvedError(TirpanError):
    def __init__(self, node):
        super(CallNotResolvedError, self).__init__()
        if isinstance(node, Call):
            self.func = node.func.id
        elif isinstance(node, (BinOp, UnaryOp)):
            self.func = get_operator_name(node.op.__class__)
        self._str = self.prefix + \
                    ('call to "%s" in "%s" at (%d, %d) was not resolved' % \
                    (str(self.func), getFile(node), getLine(node), getCol(node)))

    def __str__(self):
        return self._str 
