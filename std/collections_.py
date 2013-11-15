'''
Created on 10.11.2013

@author: bronikkk
'''

from ti.sema import *

def quasiDefaultDict(params, **kwargs):
    res = DictSema(True)
    return {res}

functions = [
                ['defaultdict', quasiDefaultDict, 1],
            ]

variables = [
            ]

modules   = [
            ]

classes   = [
            ]

def getAll():
    return (functions, variables, modules, classes)
