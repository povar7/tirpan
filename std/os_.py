import os

from typenodes import *

type_str = TypeStr()

def quasi_listdir(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    res = TypeList()
    try:
        if type1.value.endswith(('docgen', 'webstuff', 'FamilySheet')):
            filenames = os.listdir(type1.value)
            for elem in filenames:
                if elem.endswith('.gpr.py'):
                     res.add_elem(get_new_string(elem))
    except:
        pass
    if len(res.elem_types()) == 0:
        res.add_elem(type_str)
    return set([res])

def quasi_walk(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    res = TypeList()        
    try:
        for (dirpath, dirnames, filenames) in os.walk(type1.value):
            tmp_tuple = TypeTuple()
            tmp1 = get_new_string(dirpath)
            tmp2 = TypeList()
            for elem in dirnames:
                tmp = get_new_string(elem)
                tmp2.add_elem(tmp)
            tmp3 = TypeList()
            for elem in filenames:
                tmp = get_new_string(elem)
                tmp3.add_elem(tmp)
            tmp_tuple.elems = (tmp1, tmp2, tmp3)
            res.add_elem(tmp_tuple)
    except:
        pass
    return set([res])

def quasi_environ():
    res = TypeDict()
    for pair in os.environ.items():
        new_pair = (pair[0], get_new_string(pair[1]))
        res.add_key(get_new_string(new_pair[0]))
        res.add_pair(new_pair)
    return res

functions = [                                       \
                ['listdir', quasi_listdir, 1],      \
                ['walk'   , quasi_walk   , 1]       \
            ]

stubs     = [                                       \
            ]

variables = [                                       \
                ['environ', quasi_environ]          \
            ]

modules   = [                                       \
            ]

objects   = [                                       \
            ]

def get_all():
    return (functions, stubs, variables, modules, objects)
