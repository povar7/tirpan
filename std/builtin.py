'''
Created on 01.04.2012

@author: bronikkk
'''

from typenodes import *

type_int  = TypeInt()
type_type = TypeType()

def quasi_len(scope):
    return set([type_int])

def quasi_range1(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    if type1 == type_int:
        type_list = TypeList()
        type_list.add_elem(type_int)
        return set([type_list])
    else:
        return set()

def quasi_range3(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    type3 = list(scope.findParam(3).nodeType)[0]
    if type1 == type_int and type2 == type_int and type3 == type_int:
        type_list = TypeList()
        type_list.add_elem(type_int)
        return set([type_list])
    else:
        return set()

def quasi_type1(scope):
    return set([type_type])

def quasi_type_var():
    return type_type

functions = [
                ['len'  , quasi_len   , 1],                 \
                ['range', quasi_range1, 1],                 \
                ['range', quasi_range3, 3, {3 : type_int}], \
                ['type' , quasi_type1 , 1]                  \
            ]

variables = [                                               \
                ['type'     , quasi_type_var],              \
                ['object'   , quasi_type_var],              \
                ['int'      , quasi_type_var],              \
                ['long'     , quasi_type_var],              \
                ['float'    , quasi_type_var],              \
                ['bool'     , quasi_type_var],              \
                ['complex'  , quasi_type_var],              \
                ['str'      , quasi_type_var],              \
                ['unicode'  , quasi_type_var],              \
                ['buffer'   , quasi_type_var],              \
                ['tuple'    , quasi_type_var],              \
                ['list'     , quasi_type_var],              \
                ['dict'     , quasi_type_var],              \
                ['file'     , quasi_type_var],              \
                ['xrange'   , quasi_type_var],              \
                ['slice'    , quasi_type_var],              \
                ['NameError', quasi_type_var]               \
            ]

modules   = [                                               \
                ['sys']                                     \
            ]

def get_all():
    return (functions, variables, modules)
