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
            types.add(type_none)
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

def create_dummy_variable(nodeType):
    from typegraph import UsualVarTypeGraphNode
    res = UsualVarTypeGraphNode(None)
    res.nodeType = set([nodeType])
    return res

class TemplateValue:
    def __init__(self):
        self.ast    = None
        self.result = set()
        self.args   = None

def process_out_params(args, kwargs, elem, elem_copy, star_res, kw_res, attr_call):
    from typegraph import ClassInstanceTypeGraphNode, DependencyType

    if kw_res is not None:
        kw_arg = elem[kw_res]
        for pair in kwargs.items():
            key, arg = pair
            try:
                elem_type = kw_arg._dict[key]
            except KeyError:
                elem_type = None
            if isinstance(elem_type, (TypeStandard, ClassInstanceTypeGraphNode)):
                var = create_dummy_variable(elem_type)
                var.addDependency(DependencyType.Assign, arg)

    if star_res is None:
        star_res  = len(args)
    else:
        arg_index = star_res
        star_arg  = elem[star_res]
        if isinstance(star_arg, TypeTuple) and isinstance(star_arg.elems, tuple):
            for elem_type in star_arg.elems:
                arg = args[arg_index]
                if isinstance(elem_type, (TypeStandard, ClassInstanceTypeGraphNode)):
                    var = create_dummy_variable(elem_type)
                    var.addDependency(DependencyType.Assign, arg)
                arg_index += 1

    arg_index = 0
    for arg in args[0:star_res]:
        elem_atom = elem[arg_index]
        copy_atom = elem_copy[arg_index]
        if isinstance(copy_atom, (TypeStandard, ClassInstanceTypeGraphNode)):
            var = create_dummy_variable(elem_atom)
            if attr_call and arg_index == 0:
                var.addDependency(DependencyType.AttrObject, arg)
            else:
                var.addDependency(DependencyType.Assign, arg)
        arg_index += 1

def process_product_elem(pair, args, arg_elem, kwargs, kwarg_elem, attr_call):
    import __main__
    from tivisitor import TIVisitor
    from typegraph import DependencyType, ExternFuncDefTypeGraphNode, UsualFuncDefTypeGraphNode
    cls, func = pair
    cls_instance = make_new_instance(cls)
    if cls_instance:
        if not func:
            return set([cls_instance])
        arg_list  = [cls_instance]
        arg_list += list(arg_elem)
        arg_elem  = tuple(arg_list)
    elem, star_res, kw_res = func.params.getArgs(arg_elem, kwarg_elem)
    if elem is None:
        return set()
    key = find_previous_key(elem, func.templates.keys())
    if key is None:
        params_copy   = copy_params(func.params)
        elem_copy     = deepcopy(elem)
        params_copy.linkParamsAndArgs(elem)
        func.templates[elem_copy] = TemplateValue()
        saved_scope   = __main__.current_scope
        func_scope    = Scope(params_copy)
        __main__.current_scope = func_scope
        if isinstance(func, UsualFuncDefTypeGraphNode):
            ast_copy  = deepcopy(func.ast)
            saved_res = __main__.current_res
            __main__.current_res = set()
            try:
                filename = __main__.importer.get_ident(ast_copy[0].fileno).name
            except AttributeError:
                filename = None
            visitor = TIVisitor(filename)
            for stmt in ast_copy:
                visitor.visit(stmt)
            if cls_instance:
                __main__.current_scope = saved_scope
                del func.templates[elem_copy]
                return set([cls_instance])
            else:
                func.templates[elem_copy].ast    = ast_copy
                func.templates[elem_copy].result =             \
                    process_results(__main__.current_res,      \
                                    func.defReturn)
                func.templates[elem_copy].args   = elem
            __main__.current_res = saved_res
        elif isinstance(func, ExternFuncDefTypeGraphNode):
            func.templates[elem_copy].result = func.quasi(__main__.current_scope)
            func.templates[elem_copy].args   = elem
        __main__.current_scope = saved_scope
    else:
        elem_copy = key
        elem = func.templates[elem_copy].args
    if elem is not None:
        process_out_params(args, kwargs, elem, elem_copy, star_res, kw_res, attr_call)
    return func.templates[elem_copy].result
