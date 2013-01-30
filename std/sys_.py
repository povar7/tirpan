import sys

from typenodes import *
from configure import  config

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
    res = TypeList(True)
    main_path = config.importer.main_path
    tmp = []  
    if main_path is not None:
        tmp.append(get_new_string(main_path))
    for elem in sys.path[1:]:
        tmp.append(get_new_string(elem))
    res.elems = tmp
    return res

def quasi_builtin_module_names():
    res = TypeTuple()
    tmp = []
    for elem in sys.builtin_module_names:
        tmp.append(get_new_string(elem))
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
