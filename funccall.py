'''
Created on 09.03.2012

@author: bronikkk
'''

from copy      import deepcopy
from itertools import product

from classes   import make_new_instance
from scope     import Scope
from typenodes import *

type_none = TypeNone()

def must_be_skipped(func):
    try:
        if func.name == 'rmtree':
            return True
    except AttributeError:
        pass
    return False

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
        except RuntimeError:
            pass
    return types

def find_previous_key(elem, keys):
    for key in keys:
        try:
            if key == elem:
                return key
        except RuntimeError:
            pass
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
    try: 
        res.nodeType = set([nodeType])
    except RuntimeError:
        pass
    return res

class TemplateValue:
    def __init__(self):
        self.ast    = None
        self.result = set()
        self.args   = None

def process_out_params(args, starargs, kwargs, elem, elem_copy, star_res, kw_res, attr_call):
    from typegraph import ClassInstanceTypeGraphNode, SubscriptTypeGraphNode, DependencyType

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
        last_index   = len(args)
    else:
        last_index   = star_res
        arg_index    = star_res
        star_arg     = elem[star_res]
        if isinstance(star_arg, TypeTuple) and isinstance(star_arg.elems, tuple):
            for elem_type in star_arg.elems:
                if not isinstance(elem_type, (TypeStandard, ClassInstanceTypeGraphNode)):
                    arg_index += 1
                    continue
                var = create_dummy_variable(elem_type)
                try:
                    arg = args[arg_index]
                    var.addDependency(DependencyType.Assign, arg)
                except IndexError:
                    star_index = arg_index - len(args)
                    star_link  = SubscriptTypeGraphNode(True, star_index)
                    star_link.addDependency(DependencyType.AssignObject, starargs)
                    starargs.addDependency(DependencyType.AttrObject, star_link)
                    var.addDependency(DependencyType.Assign, star_link)
                arg_index += 1

    arg_index = 0
    for arg in args[0:last_index]:
        elem_atom = elem[arg_index]
        copy_atom = elem_copy[arg_index]
        if isinstance(copy_atom, (TypeStandard, ClassInstanceTypeGraphNode)):
            var = create_dummy_variable(elem_atom)
            if attr_call and arg_index == 0:
                var.addDependency(DependencyType.AttrObject, arg)
            else:
                var.addDependency(DependencyType.Assign, arg)
        arg_index += 1

    if starargs is None:
        return

    if star_res is None:
        last_index = len(elem)
    else:
        last_index = star_res

    for arg_index in range(len(args), last_index):
        elem_atom = elem[arg_index]
        copy_atom = elem_copy[arg_index]
        if isinstance(copy_atom, (TypeStandard, ClassInstanceTypeGraphNode)):
            var = create_dummy_variable(elem_atom)
            star_index = arg_index - len(args)
            star_link  = SubscriptTypeGraphNode(True, star_index)
            star_link.addDependency(DependencyType.AssignObject, starargs)
            starargs.addDependency(DependencyType.AttrObject, star_link)
            var.addDependency(DependencyType.Assign, star_link)

def get_elem_set(elem, params_copy):
    sorted_params = params_copy.getSortedParams()
    params_types  = []
    for param_index in range(0, len(elem)):
        params_types.append(sorted_params[param_index].nodeType)
    for item in product(*params_types):
        yield item

def process_product_elem(pair, args, arg_elem, starargs, stararg_elem, kwargs, kwarg_elem, attr_call):
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
    elem, star_res, kw_res = func.params.getArgs(arg_elem, stararg_elem, kwarg_elem)
    if elem is None:
        return set()
    key = find_previous_key(elem, func.templates.keys())
    if key is None:
        if len(func.templates.keys()) > 100:
            return set()
        params_copy   = copy_params(func.params)
        elem_copy     = deepcopy(elem)
        params_copy.linkParamsAndArgs(elem)
        try:
            func.templates[elem_copy] = TemplateValue()
        except RuntimeError:
            return set()
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
                if elem_copy not in func.templates:
                    func.templates[elem_copy] = TemplateValue()
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
        params_copy = None
        elem_copy   = key
        try:
            elem = func.templates[elem_copy].args
        except KeyError:
            return set()
    if elem is not None:
        if params_copy is None:
            process_out_params(args, starargs, kwargs, elem, elem_copy, star_res, kw_res, attr_call)
        else:
            for new_elem in get_elem_set(elem, params_copy):
                process_out_params(args, starargs, kwargs, new_elem, elem_copy, star_res, kw_res, attr_call)
    try:
        return func.templates[elem_copy].result
    except KeyError:
        return set()
