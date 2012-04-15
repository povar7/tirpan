'''
Created on 24.03.2012

@author: bronikkk
'''

from ast       import Add, BitAnd, BitOr, Div, FloorDiv, LShift, Mod, Mult, RShift, Sub
from typegraph import *
from typenodes import *

operator_names_table = {                    \
                           Add      : '+' , \
                           BitAnd   : '&' , \
                           BitOr    : '|' , \
                           Div      : '/' , \
                           FloorDiv : '//', \
                           LShift   : '<<', \
                           Mult     : '*' , \
                           Mod      : '%' , \
                           RShift   : '>>', \
                           Sub      : '-'   \
                       }

def get_binary_operator_name(op):
    return operator_names_table[op]

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
    if type1 == type_bool and type2 == type_bool:
        return set([type_int])
    return set([type_int, type_long])

def quasi_bitand(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]

    if not isinstance(type1, (TypeBool, TypeInt, TypeLong)):
        return set()
    if not isinstance(type2, (TypeBool, TypeInt, TypeLong)):
        return set()

    if isinstance(type1, TypeLong) or isinstance(type2, TypeLong):
        return set([type_long])
    if isinstance(type1, TypeInt) or isinstance(type2, TypeInt):
        return set([type_int])
    return set([type_bool])

def quasi_bitor(scope):
    return quasi_bitand(scope)

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

def quasi_floordiv(scope):
    return quasi_div(scope)

def quasi_lshift(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]

    if not isinstance(type1, (TypeBool, TypeLong, TypeInt)):
        return set()
    if not isinstance(type2, (TypeBool, TypeLong, TypeInt)):
        return set()

    if isinstance(type1, TypeBool):
        type1 = type_int
    if isinstance(type2, TypeBool):
        return set([type1])
    if isinstance(type1, TypeLong) or isinstance(type2, TypeLong):
        return set([type_long])
    return set([type_int, type_long])

def quasi_mod(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    if type1 == type_str:
        return set([type_str])
    if type1 == type_unicode:
        return set([type_unicode])
    return quasi_div(scope)

def quasi_mult(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]

    if isinstance(type1, (TypeBaseString, TypeListOrTuple)) and (type2 == type_bool or type2 == type_int or type2 == type_long):
        return set([type1])
    if isinstance(type2, (TypeBaseString, TypeListOrTuple)) and (type1 == type_bool or type1 == type_int or type1 == type_long):
        return set([type2])
    if type1 == type_int and type2 == type_int:
        return set([type_int, type_long])

    return quasi_div(scope)

def quasi_rshift(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]

    if not isinstance(type1, (TypeBool, TypeLong, TypeInt)):
        return set()
    if not isinstance(type2, (TypeBool, TypeLong, TypeInt)):
        return set()

    if isinstance(type1, TypeBool):
        type1 = type_int
    if isinstance(type2, TypeBool):
        return set([type1])
    if isinstance(type1, TypeLong) or isinstance(type2, TypeLong):
        return set([type_long])
    return set([type_int])

def quasi_sub(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    if isinstance(type1, (TypeBaseString, TypeListOrTuple)):
        return set()
    if isinstance(type2, (TypeBaseString, TypeListOrTuple)):
        return set()

    return quasi_plus(scope)

def init_binop(scope, op, quasi):
    name = get_binary_operator_name(op)
    func = ExternFuncDefTypeGraphNode(2, quasi, scope)
    var  = scope.findOrAdd(name)
    func.addDependency(DependencyType.Assign, var)
    scope.add(var)

def init_binops(scope):
    init_binop(scope, Add     , quasi_plus    )
    init_binop(scope, BitAnd  , quasi_bitand  )
    init_binop(scope, BitOr   , quasi_bitor   )
    init_binop(scope, Div     , quasi_div     )
    init_binop(scope, FloorDiv, quasi_floordiv)
    init_binop(scope, LShift  , quasi_lshift  )
    init_binop(scope, Mult    , quasi_mult    )
    init_binop(scope, Mod     , quasi_mod     )
    init_binop(scope, RShift  , quasi_rshift  )
    init_binop(scope, Sub     , quasi_sub     )
