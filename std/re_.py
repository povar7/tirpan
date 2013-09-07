'''
Created on 21.07.2013

@author: bronikkk
'''

import re

from ti.sema import *

def findReModule():
    import config
    importer = config.data.importer
    return importer.importedFiles['re']

def findReName(name):
    module = findReModule()
    var = module.getScope().findName(name)
    assert len(var.nodeType) == 1
    return list(var.nodeType)[0]

def quasiCompile(params, **kwargs):
    try:
        pattern = re.compile(params[0].value)
        cls = findReName(getPatternClassName())
        if not cls:
            return set()
        res = cls.getClassInstance()
        res.data = pattern
        return {res}
    except:
        return set()

def quasiMatch(params, **kwargs):
    try:
        match = params[0].data.match(params[1].value)
        cls = findReName(getMatchClassName())
        if not cls:
            return set()
        res = cls.getClassInstance()
        res.data = match
        return {res}
    except:
        return set()

def quasiGroups(params, **kwargs):
    try:
        groups = params[0].data.groups()
        res = TupleSema()
        res.elems = [set()]
        for elem in groups:
            res.elems.append({LiteralValueSema(elem)})
        return {res}
    except:
        return set()

functions = [
                ['compile', quasiCompile, 1],
            ]

variables = [
            ]

modules   = [
            ]

def getPatternClassName():
    return 'SRE_Pattern'

patternClass = (
                   getPatternClassName(),
                   [
                       ['match', quasiMatch, 2],
                   ],
                   [
                   ]
               )

def getMatchClassName():
    return 'SRE_Match'

matchClass = (
                 getMatchClassName(),
                 [
                     ['groups', quasiGroups, 1],
                 ],
                 [
                 ]
             )

classes   = [
                patternClass,
                matchClass
            ]

def getAll():
    return (functions, variables, modules, classes)
