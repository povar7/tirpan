'''
Created on 08.09.2013

@author: bronikkk
'''

import urllib

from ti.sema import *

def quasiUrlopen(params, **kwargs):
    return set()

def quasiUrl2pathname(params, **kwargs):
    return set()

functions = [
                ['urlopen'     , quasiUrlopen     , 1],
                ['url2pathname', quasiUrl2pathname, 1]
            ]

variables = [
            ]

modules   = [
            ]

classes   = [
            ]

def getAll():
    return (functions, variables, modules, classes)
