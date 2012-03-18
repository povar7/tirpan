'''
Created on 18.03.2012

@author: bronikkk
'''

from copy import deepcopy as stdcopy

from scope     import Scope

def copy_params(params):
    save   = params.parent
    params.parent = None
    result = stdcopy(params)
    params.parent = save
    result.parent = save
    return result

def copy_func_def(func_def):
    return func_def

def deepcopy(x):
    from typegraph import FuncDefTypeGraphNode
    if isinstance(x, Scope) and x.params_scope:
        return copy_params(x)
    if isinstance(x, FuncDefTypeGraphNode):
        return copy_func_def(x)
    return stdcopy(x)
