'''
Created on 05.06.2013

@author: bronikkk
'''

from ti.sema import *

typeNone = LiteralValueSema(None)

def quasiAppend(types):
    if isinstance(types[0], ListSema):
        types[0].addElementsAtIndex(None, {types[1]})
    return {typeNone}

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
            ]

variables = [
            ]

modules   = [
            ]

classes   = [
                listClass
            ]

def getAll():
    return (functions, variables, modules, classes)
