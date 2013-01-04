'''
Created on 09.03.2012

@author: bronikkk
'''

import ast

from copy      import deepcopy
from itertools import product

from classes   import make_new_instance
from scope     import Scope
from typenodes import *

type_none = TypeNone()

class QuasiIndex(object):
    def __init__(self, n):
        self.n = n

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
            if isinstance(res, ast.Return):
                types = types.union(res.value.link.nodeType)
            elif isinstance(res, ast.Yield):
                res_type = res.value.link.nodeType
                tmp = TypeList()
                for elem in res_type:
                    tmp.add_elem(elem)
                types.add(tmp)
            else:
                types = types.union(res.link.nodeType)
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

def find_previous_key_index(elem, keys, index):
    for key in keys:
        try:
            if unicode(key[index].value) == unicode(elem[index].value):
                return key
        except AttributeError:
            pass
        except IndexError:
            pass
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
                    star_index  = arg_index - len(args)
                    quasi_index = QuasiIndex(star_index)
                    star_link   = SubscriptTypeGraphNode(True, quasi_index)
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
            star_index  = arg_index - len(args)
            quasi_index = QuasiIndex(star_index)
            star_link   = SubscriptTypeGraphNode(True, quasi_index)
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

def process_product_elem(pair, args, arg_elem, starargs, stararg_elem, kwargs, kwarg_elem, attr_call, file_number):
    import __main__
    from tivisitor import TIVisitor
    from typegraph import DependencyType, AttributeTypeGraphNode, ExternFuncDefTypeGraphNode, UsualFuncDefTypeGraphNode
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
    if func.name == 'execfile':
        key = find_previous_key_index(elem, func.templates.keys(), 0)
    else:
        key = find_previous_key(elem, func.templates.keys())
    if key is None:
        if func.mustBeExternal() or func.isLoadTooBig(cls):
            return set()
        params_copy   = copy_params(func.params)
        elem_copy     = deepcopy(elem)
        params_copy.linkParamsAndArgs(elem)
        load_increase = False
        try:
            func.templates[elem_copy] = TemplateValue()
            load_increase = func.increaseLoad(elem_copy)
        except RuntimeError:
            return set()
        saved_scope   = __main__.current_scope
        func_scope    = Scope(params_copy)
        __main__.current_scope = func_scope
        if isinstance(func, UsualFuncDefTypeGraphNode):
            if func.name == 'scan_dir' and \
               len(elem_copy) > 1 and \
               isinstance(elem_copy[1], TypeBaseString):
                if elem_copy[1].value is None or \
                   not elem_copy[1].value.endswith(('docgen', 'webstuff', 'FamilySheet')):
                    del func.templates[elem_copy]
                    func.decreaseLoad()
                    return set()
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
                if load_increase:
                    func.decreaseLoad()
                return set([cls_instance])
            else:
                if elem_copy not in func.templates:
                    func.templates[elem_copy] = TemplateValue()
                    func.increaseLoad(elem_copy)
                func.templates[elem_copy].ast    = ast_copy
                if not func.name:
                    __main__.current_res.add(ast_copy[0])
                func.templates[elem_copy].result =             \
                    process_results(__main__.current_res,      \
                                    func.defReturn)
                func.templates[elem_copy].args   = elem
            __main__.current_res = saved_res
            __main__.current_scope = saved_scope
        elif isinstance(func, ExternFuncDefTypeGraphNode):
            args_scope = __main__.current_scope
            __main__.current_scope = saved_scope
            try:
                if func.name == 'connect' and \
                   len(args) == 3 and \
                   isinstance(args[2], AttributeTypeGraphNode):
                    func.templates[elem_copy].result = func.quasi(args_scope, OBJECTS=args[2].objects)
                else:
                    func.templates[elem_copy].result = func.quasi(args_scope, FILE_NUMBER=file_number)
            except TypeError:
                func.templates[elem_copy].result = func.quasi(args_scope)
            func.templates[elem_copy].args = elem
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
        result = func.templates[elem_copy].result
        if func.name == 'newplugin':
            del func.templates[elem_copy]
            func.decreaseLoad()
        return result
    except KeyError:
        return set()
