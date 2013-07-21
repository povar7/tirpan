'''
Created on 21.07.2013

@author: bronikkk
'''

import types

from ti.sema import *

typeNone = LiteralSema(types.NoneType)

class QuasiNode(object):

    def __init__(self, link):
        self.link = link

class QuasiCall(object):

    def __init__(self, func, args):
        self.func = func
        self.args = args

def quasiTimeout_Add(params, **kwargs):
    from ti.tgnode import FunctionCallTGNode, VariableTGNode

    vaarg = params[0]
    if not isinstance(vaarg, TupleSema):
        return {typeNone}

    size = vaarg.getNumberOfElements()
    if size < 2:
        return {typeNone}

    funcTypes = vaarg.getElementsAtIndex(1)
    func = QuasiNode(VariableTGNode('func', funcTypes.copy()))

    args = []
    for index in range(2, size):
        argTypes = vaarg.getElementsAtIndex(index)
        arg = VariableTGNode('arg' + str(index), argTypes.copy())
        args.append(QuasiNode(arg))

    quasiCall = QuasiCall(func, args)
    FunctionCallTGNode(quasiCall)

    return {typeNone}

functions = [
                ['timeout_add', quasiTimeout_Add, 0, None, True, True],
            ]

variables = [
            ]

modules   = [
            ]

objects   = [
            ]

def getAll():
    return (functions, variables, modules, objects)
