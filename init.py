'''
Created on 24.03.2012

@author: bronikkk
'''

from binop   import init_binops
from builtin import init_builtins

def common_init(global_scope):
    init_binops(global_scope)
    init_builtins(global_scope)
