from typenodes import *

type_str = TypeStr()

def quasi_listdir(scope):
    res = TypeList()
    res.add_elem(type_str)
    return set([res])

functions = [                                       \
                ['listdir', quasi_listdir, 1],      \
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
