import ast

from typenodes import *

type_none    = TypeNone()
type_unknown = TypeUnknown()

def find_gtk_module():
    from typegraph import ModuleTypeGraphNode
    import __main__
    var = __main__.current_scope.find('gtk')
    try:
        for elem in var.nodeType:
            if isinstance(elem, ModuleTypeGraphNode):
                return elem
    except AttributeError:
        pass
    return None

def find_gtk_class(name):
    from typegraph import ClassDefTypeGraphNode
    module = find_gtk_module()
    try:
        var = module.getScope().find(name)
        for elem in var.nodeType:
            if isinstance(elem, ClassDefTypeGraphNode):
                return elem
    except AttributeError:
        pass
    return None

def quasi_actiongroup(scope):
    from typegraph import ClassInstanceTypeGraphNode
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    quasi_res = type1
    if not hasattr(quasi_res, '_actions'):
        quasi_res._actions = TypeList()
    if not hasattr(quasi_res, '_name'):
        try:
            quasi_res._name = str(type2.value)
        except AttributeError:
            quasi_res._name = ''
    return set([quasi_res])

def quasi_add_actions(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    try:
        for elem in type2.elems:
            if isinstance(elem, TypeTuple):
                type1._actions.add_elem(elem)
    except:
        pass
    return set([type_none])

def quasi_gtk_main(scope):
    try:
        import __main__
        from scope import Scope
        from tivisitor import TIVisitor
        from typegraph import ExternVarTypeGraphNode
        quasi_cls = find_gtk_class(get_quasi_actiongroup_name())
        if not quasi_cls:
            return set([type_none])
        save = __main__.current_scope
        __main__.current_scope = Scope(__main__.current_scope)
        callbacks = set()
        for inst in quasi_cls.getInstances():
            for action_tuple in inst._actions.elems:
                if isinstance(action_tuple, TypeTuple) and \
                   isinstance(action_tuple.elems, tuple) and \
                   len(action_tuple.elems) == 6:
                    callbacks.add(action_tuple.elems[5])
        var = ExternVarTypeGraphNode(get_quasi_callback_name(), callbacks)
        __main__.current_scope.add(var)
        module  = ast.parse('__callback__(None)')
        stmt    = module.body[0]
        stmt.value.func.id = get_quasi_callback_name()
        visitor = TIVisitor(None)
        visitor.visit(stmt)
        __main__.current_scope = save
    except:
        pass
    return set([type_none])

functions = [                                                             \
                ['main', quasi_gtk_main, 0],                              \
            ]

stubs     = [                                                             \
            ]

variables = [                                                             \
            ]

modules   = [                                                             \
            ]

def get_quasi_actiongroup_name():
    return 'ActionGroup'

def get_quasi_callback_name():
    return '#CALLBACK#'

quasi_actiongroup_object = (                                              \
                               get_quasi_actiongroup_name(),              \
                               [                                          \
                                   ['__init__',    quasi_actiongroup, 2], \
                                   ['add_actions', quasi_add_actions, 2]  \
                               ],                                         \
                               [                                          \
                               ]
                           )

objects   = [                                                             \
                quasi_actiongroup_object                                  \
            ]

def get_all():
    return (functions, stubs, variables, modules, objects)
