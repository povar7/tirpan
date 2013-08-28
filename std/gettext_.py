'''
Created on 28.08.2013

@author: bronikkk
'''

def quasiGettext(params, **kwargs):
    res = params[0]
    return {res}

functions = [
                ['gettext', quasiGettext, 1],
            ]

variables = [
            ]

modules   = [
            ]

classes   = [
            ]

def getAll():
    return (functions, variables, modules, classes)
