import sys

from ti.sema import *

typeInt = LiteralSema(int)

def quasiGetsizeof1(scope):
    return {typeInt}

def quasiGetsizeof2(scope):
    return {typeInt}

def quasiArgv():
    res = ListSema()
    res.elems = [set()]
    for elem in sys.argv:
        res.elems.append({LiteralValueSema(elem)})
    return {res}

def quasiMaxint():
    return {typeInt}

def quasiPath():
    import config
    res = ListSema()
    mainPath = config.data.importer.mainPath
    res.elems = [set()]
    if mainPath is not None:
        res.elems.append({LiteralValueSema(mainPath)})
    for elem in sys.path[1:]:
        res.elems.append({LiteralValueSema(elem)})
    return {res}

def quasiBuiltinModuleNames():
    res = TupleSema()
    res.elems = [set()]
    for elem in sys.builtin_module_names:
        res.elems.append({LiteralValueSema(elem)})
    return {res}

functions = [
                ['getsizeof', quasiGetsizeof1, 1],
                ['getsizeof', quasiGetsizeof2, 2],
            ]

variables = [
                ['argv'                , quasiArgv              ],
                ['builtin_module_names', quasiBuiltinModuleNames],
                ['maxint'              , quasiMaxint            ],
                ['path'                , quasiPath              ],
            ]

modules   = [
            ]

objects   = [
            ]

def getAll():
    return (functions, variables, modules, objects)
