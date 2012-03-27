'''
Created on 24.03.2012

@author: bronikkk
'''

from ast       import Add, Div, Mult, Sub
from typegraph import *
from typenodes import *

operator_names_table = {Add : '+', Div : '/', Mult : '*', Sub : '-'}

def get_operator_name(op):
    try:
        return operator_names_table[op]
    except KeyError:
        return op

type_int     = TypeInt()
type_long    = TypeLong()
type_float   = TypeFloat()
type_complex = TypeComplex()
type_str     = TypeStr()
type_unicode = TypeUnicode()
type_bool    = TypeBool()
type_none    = TypeNone()

def quasi_plus(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]

    if isinstance(type1, TypeList) and isinstance(type2, TypeList):
        res = deepcopy(type1)
        for elem in type2.elems:
            res.add_elem(elem)
        return set([res])

    if isinstance(type1, TypeTuple) and isinstance(type2, TypeTuple):
        res = deepcopy(type1)
        for elem in type2.elems:
            res.add_elem(elem)
        return set([res])

    if isinstance(type1, TypeBaseString) and isinstance(type2, TypeBaseString):
        if type1 == type_unicode or type2 == type_unicode:
            return set([type_unicode])
        else:
            return set([type_str])

    if not isinstance(type1, TypeNumOrBool) or not isinstance(type2, TypeNumOrBool):
        return set()
    if type1 == type_complex or type2 == type_complex:
        return set([type_complex])
    if type1 == type_float or type2 == type_float:
        return set([type_float])
    if type1 == type_long or type2 == type_long:
        return set([type_long])
    return set([type_int])

def quasi_div(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]

    if not isinstance(type1, TypeNumOrBool) or not isinstance(type2, TypeNumOrBool):
        return set()
    if type1 == type_complex or type2 == type_complex:
        return set([type_complex])
    if type1 == type_float or type2 == type_float:
        return set([type_float])
    if type1 == type_long or type2 == type_long:
        return set([type_long])
    return set([type_int])

def quasi_mult(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]

    if isinstance(type1, (TypeBaseString, TypeListOrTuple)) and (type2 == type_bool or type2 == type_int or type2 == type_long):
        return set([type1])
    if isinstance(type2, (TypeBaseString, TypeListOrTuple)) and (type1 == type_bool or type1 == type_int or type1 == type_long):
        return set([type2])

    return quasi_div(scope)

def quasi_sub(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    if isinstance(type1, (TypeBaseString, TypeListOrTuple)):
        return set()
    if isinstance(type2, (TypeBaseString, TypeListOrTuple)):
        return set()

    return quasi_plus(scope)

def init_binop(op, quasi, scope):
    name = get_operator_name(op)
    func = ExternFuncDefTypeGraphNode(2, quasi, scope)
    var  = scope.findOrAdd(name)
    func.addDependency(DependencyType.Assign, var)
    scope.add(var)

def init_binops(scope):
    init_binop(Add , quasi_plus, scope) 
    init_binop(Div , quasi_div , scope)
    init_binop(Mult, quasi_mult, scope) 
    init_binop(Sub , quasi_sub , scope) 
