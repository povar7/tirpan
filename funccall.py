'''
Created on 09.03.2012

@author: bronikkk
'''

from safecopy  import deepcopy
from scope     import Scope

def process_results(results):
    types = set()
    for res in results:
        types = types.union(res.nodeType)
    return types

def find_previous_key(elem, keys):
    for key in keys:
        if key == elem:
            return key
    return None

def process_product_elem(func, arg_elem, kwarg_elem):
    import __main__
    from tivisitor import TIVisitor
    from typegraph import ExternFuncDefTypeGraphNode, UsualFuncDefTypeGraphNode
    elem = func.params.getArgs(arg_elem, kwarg_elem)
    if elem is None:
        return set()
    key = find_previous_key(elem, func.templates.keys())
    if key is None:
        params_copy   = deepcopy(func.params)
        params_copy.linkParamsAndArgs(elem)
        func.templates[elem] = set()
        saved_scope   = __main__.current_scope
        func_scope    = Scope(params_copy)
        __main__.current_scope = func_scope
        if isinstance(func, UsualFuncDefTypeGraphNode):
            ast_copy  = deepcopy(func.ast)
            saved_res = __main__.current_res
            __main__.current_res = set()
            visitor   = TIVisitor(ast_copy[0].filelink.name)
            for stmt in ast_copy:
                visitor.visit(stmt)
            func.templates[elem] = process_results(__main__.current_res)
            __main__.current_res = saved_res
        elif isinstance(func, ExternFuncDefTypeGraphNode):
            func.templates[elem] = func.quasi(__main__.current_scope)
        __main__.current_scope = saved_scope
    else:
        elem = key
    return func.templates[elem] 
