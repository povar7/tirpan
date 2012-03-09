'''
Created on 09.03.2012

@author: bronikkk
'''

from copy import deepcopy
import itertools

from scope import Scope
from tivisitor import TIVisitor

def process_product_elem(func, elem):
    import __main__
    if elem in func.templates:
        res = func.templates[elem]
    else:
        func.templates[elem] = set()
        ast_copy    = deepcopy(func.ast)
        func.params.linkParamsAndArgs(elem)
        saved_scope = __main__.current_scope
        saved_res   = __main__.current_res
        func_scope = Scope(func.params)
        __main__.current_scope = func_scope
        __main__.current_res   = set()
        visitor = TIVisitor(ast_copy[0].filelink.name)
        for stmt in ast_copy:
            visitor.visit(stmt)
        func.templates[elem] = __main__.current_res
        __main__.current_scope = saved_scope
        __main__.current_res   = saved_res

def process_function_call(funcs, args):
    types = [arg.link.nodeType for arg in args]
    for elem in itertools.product(*types):
        for func in funcs:
            process_product_elem(func, elem)
