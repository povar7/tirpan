'''
Created on 14.07.2013

@author: bronikkk
'''

import os

from ti.sema import *

typeStr = LiteralSema(basestring)

def quasiAbspath(params, **kwargs):
    try:
        res = LiteralValueSema(os.path.abspath(params[0].value))
        return {res}
    except:
        return {typeStr}

def quasiBasename(params, **kwargs):
    try:
        res = LiteralValueSema(os.path.basename(params[0].value))
        return {res}
    except:
        return {typeStr}

def quasiDirname(params, **kwargs):
    try:
        res = LiteralValueSema(os.path.dirname(params[0].value))
        return {res}
    except:
        return {typeStr}

def quasiJoin(params, **kwargs):
    try:
        res = LiteralValueSema(os.path.join(params[0].value, params[1].value))
        return {res}
    except:
        return {typeStr}

def quasiSplit(params, **kwargs):
    try:
        value = params[0].value 
        res   = TupleSema()
        for elem in os.path.split(value):
            res.elems.append({LiteralValueSema(elem)})
        return {res}
    except:
        return {TupleSema()}

functions = [
                ['abspath' , quasiAbspath , 1],
                ['basename', quasiBasename, 1],
                ['dirname' , quasiDirname , 1],
                ['join'    , quasiJoin    , 2],
                ['split'   , quasiSplit   , 1],
            ]

variables = [
            ]

modules   = [
            ]

classes   = [
            ]

def getAll():
    return (functions, variables, modules, classes)
