'''
Created on 24.03.2012

@author: bronikkk
'''

from binop   import init_binops, get_binary_operator_name
from unop    import init_unops, get_unary_operator_name
from builtin import init_builtins

def get_operator_name(op):
    try:
        return get_binary_operator_name(op)
    except KeyError:
        pass
    try:
        return get_unary_operator_name(op)
    except KeyError:
        pass
    return op

def common_init(global_scope, importer):
    init_binops(global_scope)
    init_unops(global_scope)
    init_builtins(global_scope, importer)
