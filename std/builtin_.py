'''
Created on 05.06.2013

@author: bronikkk
'''

import types

from ti.sema import *

typeInt  = LiteralSema(int)
typeNone = LiteralSema(types.NoneType)
typeType = LiteralSema(type)

def quasiAppend(params):
    if isinstance(params[0], ListSema):
        params[0].addElementsAtIndex(None, {params[1]})
    return {typeNone}

def quasiRange1(params):
    return quasiRange3(params + [typeInt, typeInt])

def quasiRange3(params):
    if params[0] == typeInt and params[1] == typeInt and params[2] == typeInt:
        listType = ListSema(0)
        listType.addElementsAtIndex(None, {typeInt})
        return {listType}
    else:
        return set()

def quasiType(params):
    return {typeType}

def quasiTypeVar():
    return {typeType}

listClassName = str(type([]))

def getListClassName():
    return listClassName

listClass = (
                listClassName,
                [
                    ['append', quasiAppend, 2],
                ],
                [
                ]
            )

functions = [
                ['range'     , quasiRange1  , 1],
                ['range'     , quasiRange3  , 3 , {'3' : {typeInt}}],
                ['type'      , quasiType    , 1],
            ]

variables = [
                ['int'       , quasiTypeVar    ],
                ['type'      , quasiTypeVar    ],
            ]

modules   = [
                ['os' ],
                ['sys'],
            ]

classes   = [
                listClass,
            ]

def getAll():
    return (functions, variables, modules, classes)
