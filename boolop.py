'''
Created on 03.11.2012

@author: bronikkk
'''

from ast       import And, Not, Or
from typegraph import *
from typenodes import *

operator_names_table = {                    \
                           And : 'and',     \
                           Not : 'not',     \
                           Or  : 'or' ,     \
                       }

def get_boolean_operator_name(op):
    return operator_names_table[op]

type_bool = TypeBool()

def quasi_and(scope):
    index = 0
    res   = set()
    while True:
        arg_type = scope.findStarParam(index) 
        if arg_type is None:
            return res
        res.add(arg_type)
        index += 1

def quasi_not(scope):
    return set([type_bool])

def quasi_or(scope):
    return quasi_and(scope)

def init_andor(scope, op, quasi):
    name = get_boolean_operator_name(op)
    func = ExternFuncDefTypeGraphNode(0, quasi, name, scope, {}, True)
    var  = scope.findOrAdd(name)
    func.addDependency(DependencyType.Assign, var)
    scope.add(var)

def init_not(scope, op, quasi):
    name = get_boolean_operator_name(op)
    func = ExternFuncDefTypeGraphNode(1, quasi, name, scope)
    var  = scope.findOrAdd(name)
    func.addDependency(DependencyType.Assign, var)
    scope.add(var)

def init_boolops(scope):
    init_andor(scope, And, quasi_and)
    init_andor(scope, Or , quasi_or )
    init_not  (scope, Not, quasi_not)

