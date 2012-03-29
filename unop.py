'''
Created on 24.03.2012

@author: bronikkk
'''

from ast       import UAdd, USub, Invert
from typegraph import *
from typenodes import *

operator_names_table = {UAdd : '+', USub : '-', Invert : '~'}

def get_unary_operator_name(op):
    return operator_names_table[op]

type_int     = TypeInt()
type_long    = TypeLong()
type_float   = TypeFloat()
type_complex = TypeComplex()
type_str     = TypeStr()
type_unicode = TypeUnicode()
type_bool    = TypeBool()
type_none    = TypeNone()

def quasi_uplus(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    if not isinstance(type1, TypeNumOrBool):
        return set()
    return set([type1])

def quasi_uminus(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    if type1 == type_int:
        return set([type_int, type_long])
    return quasi_uplus(scope)

def init_unop(op, quasi, scope):
    name = get_unary_operator_name(op)
    func = ExternFuncDefTypeGraphNode(1, quasi, scope)
    var  = scope.findOrAdd(name)
    func.addDependency(DependencyType.Assign, var)
    scope.add(var)

def init_unops(scope):
    init_unop(UAdd     , quasi_uplus    , scope) 
    init_unop(USub     , quasi_uminus   , scope) 
