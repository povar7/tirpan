'''
Created on 06.07.2013

@author: bronikkk
'''

import os

from ti.sema import *

def quasiListdir(params, **kwargs):
    res = ListSema()
    res.elems = [set()]
    try:
        filenames = os.listdir(params[0].value)
        for elem in filenames:
            res.elems.append({LiteralValueSema(elem)})
    except AttributeError:
        pass
    return {res}

def quasiWalk(params, **kwargs):
    res = ListSema()
    res.elems = [set()]
    try:
        for (dirpath, dirnames, filenames) in os.walk(params[0].value):
            tmpTuple = TupleSema()
            tmpTuple.elems = [set()]
            tmp1 = LiteralValueSema(dirpath)
            tmp2 = ListSema()
            tmp2.elems = [set()]
            for elem in dirnames:
                tmp2.elems.append({LiteralValueSema(elem)})
            tmp3 = ListSema()
            tmp3.elems = [set()]
            for elem in filenames:
                tmp3.elems.append({LiteralValueSema(elem)})
            tmpTuple.elems += [{tmp1}, {tmp2}, {tmp3}]
            res.elems.append({tmpTuple})
    except AttributeError:
        pass
    return {res}

def quasiEnviron():
    res = DictSema()
    for key, value in os.environ.items():
        res.elems[LiteralValueSema(key)] = {LiteralValueSema(value)}
    return {res}

def quasiPath():
    import config
    importer = config.data.importer
    res = set()
    try:
        module = importer.importedFiles['posixpath']
    except KeyError:
        return res
    res |= module.nodeType
    return res

functions = [
                ['listdir', quasiListdir, 1],
                ['walk'   , quasiWalk   , 1]
            ]

variables = [
                ['environ', quasiEnviron],
                ['path'   , quasiPath   ], 
            ]

modules   = [
            ]

objects   = [
            ]

def getAll():
    return (functions, variables, modules, objects)
