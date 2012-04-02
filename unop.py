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

type_bool = TypeBool()
type_int  = TypeInt()
type_long = TypeLong()

def quasi_uplus(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    if not isinstance(type1, TypeNumOrBool):
        return set()
    if type1 == type_bool:
        type1 = type_int
    return set([type1])

def quasi_uminus(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    if type1 == type_int:
        return set([type_int, type_long])
    return quasi_uplus(scope)

def init_unop(scope, op, quasi):
    name = get_unary_operator_name(op)
    func = ExternFuncDefTypeGraphNode(1, quasi, scope)
    var  = scope.findOrAdd(name)
    func.addDependency(DependencyType.Assign, var)
    scope.add(var)

def init_unops(scope):
    init_unop(scope, UAdd, quasi_uplus )
    init_unop(scope, USub, quasi_uminus)
