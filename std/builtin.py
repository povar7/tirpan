'''
Created on 01.04.2012

@author: bronikkk
'''

from typenodes import *

type_int  = TypeInt()
type_type = TypeType()

def quasi_range1(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    if type1 == type_int:
        return set([type_int])
    else:
        return set()

def quasi_range3(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    type3 = list(scope.findParam(3).nodeType)[0]
    if type1 == type_int and type2 == type_int and type3 == type_int:
        return set([type_int])
    else:
        return set()

def quasi_type1(scope):
    return set([type_type])

def quasi_type_var():
    return type_type

functions = [
                ['range', quasi_range1, 1],                 \
                ['range', quasi_range3, 3, {3 : type_int}], \
                ['type' , quasi_type1 , 1]                  \
            ]

variables = [                                               \
                ['type',  quasi_type_var],                  \
                ['int' ,  quasi_type_var]                   \
            ]

modules   = [                                               \
                ['sys']                                     \
            ]

def get_all():
    return (functions, variables, modules)
