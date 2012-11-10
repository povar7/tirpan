import os

from typenodes import *

type_str     = TypeStr()
type_unknown = TypeUnknown()

def quasi_abspath(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    try:
        res_str = os.path.abspath(type1.value)
        if isinstance(res_str, str):
            res = TypeStr(res_str)
        elif isinstance(res_str, unicode):
            res = TypeUnicode(res_str)
        else:
            res = TypeUnknown()
        return set([res])
    except:
        pass
    return set([type_str])

def quasi_dirname(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    try:
        res_str = os.path.dirname(type1.value)
        if isinstance(res_str, str):
            res = TypeStr(res_str)
        elif isinstance(res_str, unicode):
            res = TypeUnicode(res_str)
        else:
            res = TypeUnknown()
        return set([res])
    except:
        pass
    return set([type_str])

def quasi_join(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    try:
        res_str = os.path.join(type1.value, type2.value)
        if isinstance(res_str, str):
            res = TypeStr(res_str)
        elif isinstance(res_str, unicode):
            res = TypeUnicode(res_str)
        else:
            res = TypeUnknown()
        return set([res])
    except:
        pass
    return set([type_str])

functions = [                                       \
                ['abspath', quasi_abspath, 1],      \
                ['dirname', quasi_dirname, 1],      \
                ['join',    quasi_join   , 2],      \
            ]

stubs     = [                                       \
            ]

variables = [                                       \
            ]

modules   = [                                       \
            ]

objects   = [                                       \
            ]

def get_all():
    return (functions, stubs, variables, modules, objects)
