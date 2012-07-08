'''
Created on 09.03.2012

@author: bronikkk
'''

from copy  import deepcopy

from classes   import make_new_instance
from scope     import Scope
from typenodes import *

type_none = TypeNone()

def process_results(results, def_return):
    if def_return:
        types = set([type_none])
    else:
        types = set()
    for res in results:
        try:
            types = types.union(res.value.link.nodeType)
        except AttributeError:
            types = types.union(set([type_none]))
    return types

def find_previous_key(elem, keys):
    for key in keys:
        if key == elem:
            return key
    return None

def copy_params(params):
    save   = params.parent
    params.parent = None
    result = deepcopy(params)
    params.parent = save
    result.parent = save
    return result

class TemplateValue:
    def __init__(self):
        self.ast    = None
        self.result = set()

def process_product_elem(pair, arg_elem, kwarg_elem, func_call):
    import __main__
    from tivisitor import TIVisitor
    from typegraph import ExternFuncDefTypeGraphNode, UsualFuncDefTypeGraphNode
    cls, func = pair
    cls_instance = make_new_instance(cls)
    if cls_instance:
        if not func:
            return set([cls_instance])
        arg_list  = [cls_instance]
        arg_list += list(arg_elem)
        arg_elem  = tuple(arg_list)
    elem = func.params.getArgs(arg_elem, kwarg_elem)
    if elem is None:
        return set()
    key = find_previous_key(elem, func.templates.keys())
    if key is None:
        params_copy = copy_params(func.params)
        params_copy.linkParamsAndArgs(elem)
        func.templates[elem] = TemplateValue()
        saved_scope   = __main__.current_scope
        func_scope    = Scope(params_copy)
        __main__.current_scope = func_scope
        if isinstance(func, UsualFuncDefTypeGraphNode):
            ast_copy  = deepcopy(func.ast)
            saved_res = __main__.current_res
            __main__.current_res = set()
            visitor   = TIVisitor(__main__.importer.get_ident(ast_copy[0].fileno).name)
            for stmt in ast_copy:
                visitor.visit(stmt)
            if cls_instance:
                from typegraph import DependencyType
                __main__.current_scope = saved_scope
                cls_instance.addDependency(DependencyType.Object, func_call)
                del func.templates[elem]
                return set([cls_instance])
            else:
                func.templates[elem].ast    = ast_copy
                func.templates[elem].result =             \
                    process_results(__main__.current_res, \
                                    func.defReturn)
            __main__.current_res = saved_res
        elif isinstance(func, ExternFuncDefTypeGraphNode):
            func.templates[elem].result = func.quasi(__main__.current_scope)
        __main__.current_scope = saved_scope
    else:
        elem = key
    return func.templates[elem].result 
