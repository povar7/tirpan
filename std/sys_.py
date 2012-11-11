import sys

from typenodes import *

type_str = TypeStr()
type_int = TypeInt()

def quasi_getsizeof1(scope):
    return set([type_int])

def quasi_getsizeof2(scope):
    return set([type_int])

def quasi_argv():
    res = TypeList()
    res.add_elem(type_str)
    return res

def quasi_maxint():
    res = type_int
    return res

def quasi_path():
    res = TypeList()
    res.add_elem(type_str)
    return res

def quasi_builtin_module_names():
    res = TypeTuple()
    tmp = []
    for elem in sys.builtin_module_names:
        tmp.append(TypeStr(elem))
    res.elems = tuple(tmp)
    return res

functions = [                                                         \
                ['getsizeof', quasi_getsizeof1, 1],                   \
                ['getsizeof', quasi_getsizeof2, 2]                    \
            ]

stubs     = [                                                         \
            ]

variables = [                                                         \
                ['argv'  , quasi_argv  ],                             \
                ['builtin_module_names', quasi_builtin_module_names], \
                ['maxint', quasi_maxint],                             \
                ['path'  , quasi_path  ]                              \
            ]

modules   = [                                                         \
            ]

objects   = [                                                         \
            ]

def get_all():
    return (functions, stubs, variables, modules, objects)
