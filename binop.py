from ast       import Mult, Sub
from typegraph import *
from typenodes import *

operator_names_table = {Mult : '*', Sub : '-'}

def get_operator_name(op):
    try:
        return operator_names_table[op]
    except KeyError:
        return op

type_int   = TypeInt()

def quasi_mult(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    if (type1 == type_int and type2 == type_int):
        return set([type_int])
    return set()

def quasi_sub(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    if (type1 == type_int and type2 == type_int):
        return set([type_int])
    return set()

def init_binop(op, quasi, scope):
    name = get_operator_name(op)
    func = ExternFuncDefTypeGraphNode(2, quasi, scope)
    var  = VarTypeGraphNode(name)
    func.addDependency(DependencyType.Assign, var)
    scope.add(var)

def init_binops(scope):
    init_binop(Mult, quasi_mult, scope) 
    init_binop(Sub , quasi_sub , scope) 
