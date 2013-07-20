'''
Created on 14.07.2013

@author: bronikkk
'''

import os

from ti.sema import *

typeStr = LiteralSema(str)

def quasiAbspath(params, **kwargs):
    try:
        res = LiteralValueSema(os.path.abspath(params[0].value))
        return {res}
    except:
        pass
    return {typeStr}

def quasiBasename(params, **kwargs):
    try:
        res = LiteralValueSema(os.path.basename(params[0].value))
        return {res}
    except:
        pass
    return {typeStr}

def quasiDirname(params, **kwargs):
    try:
        res = LiteralValueSema(os.path.dirname(params[0].value))
        return {res}
    except:
        pass
    return {typeStr}

def quasiJoin(params, **kwargs):
    try:
        res = LiteralValueSema(os.path.join(params[0].value, params[1].value))
        return {res}
    except:
        pass
    return {typeStr}

functions = [
                ['abspath' , quasiAbspath , 1],
                ['basename', quasiBasename, 1],
                ['dirname' , quasiDirname , 1],
                ['join'    , quasiJoin    , 2],
            ]

variables = [
            ]

modules   = [
            ]

objects   = [
            ]

def getAll():
    return (functions, variables, modules, objects)
