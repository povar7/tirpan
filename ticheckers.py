'''
Created on 07.01.2013

@author: bronikkk
'''

import ast

from tibacktrace import get_backtrace
from typenodes   import *
from configure import config

class TirpanDefect(object):
    def __repr__(self):
        return '%s: %s' % (self._kind, self._descr)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.instance_hash() == other.instance_hash()
       
    def __hash__(self):
        return hash((self.__class__, self.instance_hash()))

    def instance_hash(self):
        return hash(self._descr)

class TirpanWrongFuncArgDefect(TirpanDefect):
    def __init__(self, elem):
        bt = get_backtrace() 
        header_str  = '\'os.path.basename\' expects <basestring object>, not %s. Backtrace:' % elem
        self._kind  = 'FUNC.ARG.WRONG'
        self._descr = header_str + '\n' + bt.get()

def check_basename_call(visitor, test):
    from typegraph import ExternFuncDefTypeGraphNode
    if isinstance(test, ast.Call):
        visitor.visit(test.func)
        nodeType = test.func.link.nodeType 
        external_funcs = [elem for elem in nodeType if isinstance(elem, ExternFuncDefTypeGraphNode)]
        if len(external_funcs) == 1:
            basename_func = list(external_funcs)[0]
            if basename_func.name == 'basename' and len(test.args) == 1:
                visitor.visit(test.args[0])
                nodeType = test.args[0].link.nodeType
                for elem in nodeType:
                    if not isinstance(elem, (TypeBaseString, TypeUnknown)):
                        try:
                            pass #Bug Found
                        except AttributeError:
                            pass
