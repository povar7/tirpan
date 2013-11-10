'''
Created on 10.11.2013

@author: bronikkk
'''

import platform

from ti.sema import *

def quasiSystem(params, **kwargs):
    res = LiteralValueSema(platform.system())
    return {res}

functions = [
                ['system', quasiSystem, 0],
            ]

variables = [
            ]

modules   = [
            ]

classes   = [
            ]

def getAll():
    return (functions, variables, modules, classes)
