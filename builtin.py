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

def quasi_argv():
    res = TypeList()
    res.add_elem(type_str)
    return res

def quasi_path():
    res = TypeList()
    res.add_elem(type_str)
    return res

def init_builtin_function(name, quasi, scope, num, def_vals = {}):
    func = ExternFuncDefTypeGraphNode(num, quasi, scope, def_vals)
    var  = scope.findOrAdd(name)
    func.addDependency(DependencyType.Assign, var)
    scope.add(var)

def init_builtin_variable(name, var_type_func, scope):
    var = ExternVarTypeGraphNode(name, var_type_func())
    scope.add(var)

def init_builtins(global_scope, importer):
    init_builtin_function('range', quasi_range1, global_scope, 1)
    init_builtin_function('range', quasi_range3, global_scope, 3, {3 : type_int})
    sys_module = importer.add_module(global_scope, 'sys')
    init_builtin_variable('argv', quasi_argv, sys_module.getScope())
    init_builtin_variable('path', quasi_path, sys_module.getScope())
