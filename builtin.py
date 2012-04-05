'''
Created on 25.03.2012

@author: bronikkk
'''

from typegraph import *
from typenodes import *

type_int     = TypeInt()
type_long    = TypeLong()
type_float   = TypeFloat()
type_complex = TypeComplex()
type_str     = TypeStr()
type_unicode = TypeUnicode()
type_bool    = TypeBool()
type_none    = TypeNone()

def quasi_type(scope):
    return set([type_str])

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

def init_builtin(name, quasi, scope, num, def_vals = {}):
    func = ExternFuncDefTypeGraphNode(num, quasi, scope, def_vals)
    var  = scope.findOrAdd(name)
    func.addDependency(DependencyType.Assign, var)
    scope.add(var)

def init_builtins(scope):
    init_builtin('range', quasi_range1, scope, 1)
    init_builtin('range', quasi_range3, scope, 3, {3 : type_int})
    init_builtin('type', quasi_type, scope, 1)