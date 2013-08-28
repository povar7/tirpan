'''
Created on 28.08.2013

@author: bronikkk
'''

import glob

from ti.sema import *

def quasiGlob(params, **kwargs):
    res = ListSema()
    res.elems = [set()]
    try:
        for elem in glob.glob(params[0].value):
            res.elems.append({LiteralValueSema(elem)})
    except AttributeError:
        pass
    return {res}

functions = [
                ['glob', quasiGlob, 1],
            ]

variables = [
            ]

modules   = [
            ]

classes   = [
            ]

def getAll():
    return (functions, variables, modules, classes)
