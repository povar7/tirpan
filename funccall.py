'''
Created on 09.03.2012

@author: bronikkk
'''

from copy  import deepcopy
from scope import Scope

def copy_params(params):
    save   = params.parent
    params.parent = None
    result = deepcopy(params)
    params.parent = save
    result.parent = save
    return result

def process_results(results):
    types = set()
    for res in results:
        types = types.union(res.nodeType)
    return types

def process_product_elem(func, elem):
    import __main__
    from tivisitor import TIVisitor
    if elem not in func.templates:
        func.templates[elem] = set()
        ast_copy    = deepcopy(func.ast)
        params_copy = copy_params(func.params)
        params_copy.linkParamsAndArgs(elem)
        saved_scope = __main__.current_scope
        saved_res   = __main__.current_res
        func_scope = Scope(params_copy)
        __main__.current_scope = func_scope
        __main__.current_res   = set()
        visitor = TIVisitor(ast_copy[0].filelink.name)
        for stmt in ast_copy:
            visitor.visit(stmt)
        func.templates[elem]   = process_results(__main__.current_res)
        __main__.current_scope = saved_scope
        __main__.current_res   = saved_res
    return func.templates[elem] 
