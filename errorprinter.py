'''
Created on 05.02.2012

@author: bronikkk
'''

import __main__

from utils import getLine, getCol, getFile

class ErrorPrinter(object):
    def printError(self, error):
        if __main__.verbose:
            print error

class TirpanError(object):
    def __init__(self):
        self.prefix = 'Tirpan error: '

class CallNotResolvedError(TirpanError):
    def __init__(self, node, func):
        super(CallNotResolvedError, self).__init__()
        self.func = func
        self._str = self.prefix + \
                    ('call to "%s" in "%s" at (%d, %d) was not resolved' % \
                    (self.func, getFile(node), getLine(node), getCol(node)))
    def __str__(self):
        return self._str 
