'''
Created on 21.07.2013

@author: bronikkk
'''

import types

from ti.sema import *
from utils   import *

typeNone = LiteralSema(types.NoneType)

def quasiTimeout_Add(params, **kwargs):
    import config
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

    tgNode = kwargs['TGNODE']
    node = tgNode.node
    quasiCall = QuasiCall(func, args, node)
    link = FunctionCallTGNode(quasiCall)
    setLink(quasiCall, link)
    kwargs['CALLS'].append((config.data.currentScope, tgNode, quasiCall))

    return {typeNone}

functions = [
                ['timeout_add', quasiTimeout_Add, 0, None, True, True],
            ]

variables = [
            ]

modules   = [
            ]

classes   = [
            ]

def getAll():
    return (functions, variables, modules, classes)
