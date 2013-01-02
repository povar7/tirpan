'''
Created on 09.12.2012

@author: bronikkk
'''

import ast

from typenodes import *

type_none = TypeNone()

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
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    quasi_res = type1
    if not hasattr(quasi_res, '_actions'):
        quasi_res._actions = TypeList()
    if not hasattr(quasi_res, '_name'):
        try:
            quasi_res._name = str(type2.value)
        except AttributeError:
            quasi_res._name = None
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

def quasi_button(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    quasi_res = type1
    if not hasattr(quasi_res, '_handlers'):
        quasi_res._handlers = TypeList()
    if not hasattr(quasi_res, '_label'):
        try:
            quasi_res._label = str(type2.value)
        except AttributeError:
            quasi_res._label = None
    return set([quasi_res])

def quasi_connect(scope, **kwargs):
    from typegraph import ExternVarTypeGraphNode
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    type3 = list(scope.findParam(3).nodeType)[0]
    try:
        try:
            var_type = kwargs['OBJECTS']
        except KeyError:
            var_type = set()
        var = ExternVarTypeGraphNode('parent', var_type)
        tmp = TypeTuple()
        tmp.elems = (type2, type3, var)
        type1._handlers.add_elem(tmp)
    except:
        pass
    return set([type_none])

def quasi_dialog(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    quasi_res = type1
    if not hasattr(quasi_res, '_buttons'):
        quasi_res._buttons = TypeList()
    if not hasattr(quasi_res, '_title'):
        try:
            quasi_res._title = str(type2.value)
        except AttributeError:
            quasi_res._title = None
    return set([quasi_res])

def quasi_add_button(scope):
    try:
        from classes import make_new_instance
        type1 = list(scope.findParam(1).nodeType)[0]
        type2 = list(scope.findParam(2).nodeType)[0]
        quasi_cls = find_gtk_class(get_quasi_button_name())
        if not quasi_cls:
            return set([type_none])
        quasi_res = make_new_instance(quasi_cls)
        quasi_res._handlers = TypeList()
        quasi_res._label = None
        type1._buttons.add_elem(quasi_res)
        return set([quasi_res])
    except:
        return set([type_none]) 

def quasi_gtk_main(scope):
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
    return set([type_none])

def quasi_run(scope):
    import __main__
    from scope import Scope
    from tivisitor import TIVisitor
    from typegraph import ExternVarTypeGraphNode
    type1 = list(scope.findParam(1).nodeType)[0]
    buttons = type1._buttons
    save = __main__.current_scope
    __main__.current_scope = Scope(__main__.current_scope)
    var_callback = ExternVarTypeGraphNode(get_quasi_callback_name(), set())
    __main__.current_scope.add(var_callback)
    var_parent   = ExternVarTypeGraphNode(get_quasi_handler_parent_name(), set())
    __main__.current_scope.add(var_parent)
    for button in buttons.elems:
        handlers = button._handlers
        for handler in handlers.elems:
            var_callback.nodeType = set([handler.elems[1]])
            var_parent.nodeType = handler.elems[2].nodeType
            if len(var_parent.nodeType) > 0:
                module = ast.parse('__callback__(__parent__, None)')
            else:
                module = ast.parse('__callback__(None)')
            stmt = module.body[0]
            stmt.value.func.id = get_quasi_callback_name()
            if len(var_parent.nodeType) > 0:
                stmt.value.args[0].id = get_quasi_handler_parent_name()
            visitor = TIVisitor(None)
            visitor.visit(stmt)
    __main__.current_scope = save
    return set([type_none])

def quasi_response_ok():
    return TypeInt(-4)

def quasi_stock_ok():
    return get_new_string('gtk-ok')

functions = [                                                             \
                ['main', quasi_gtk_main, 0],                              \
            ]

stubs     = [                                                             \
            ]

variables = [                                                             \
                ['RESPONSE_OK', quasi_response_ok],                       \
                ['STOCK_OK'   , quasi_stock_ok   ]                        \
            ]

modules   = [                                                             \
            ]

def get_quasi_actiongroup_name():
    return 'ActionGroup'

def get_quasi_callback_name():
    return '#CALLBACK#'

def get_quasi_handler_parent_name():
    return '#HANDLER_PARENT#'

def get_quasi_button_name():
    return 'Button'

def get_quasi_dialog_name():
    return 'Dialog'

quasi_actiongroup_object = (                                              \
                               get_quasi_actiongroup_name(),              \
                               [                                          \
                                   ['__init__',    quasi_actiongroup, 2], \
                                   ['add_actions', quasi_add_actions, 2]  \
                               ],                                         \
                               [                                          \
                               ]
                           )

quasi_button_object = (                                                   \
                          get_quasi_button_name(),                        \
                          [                                               \
                               ['__init__', quasi_button , 2],            \
                               ['connect' , quasi_connect, 3],            \
                          ],                                              \
                          [                                               \
                          ]
                      )

quasi_dialog_object = (                                                   \
                          get_quasi_dialog_name(),                        \
                          [                                               \
                               ['__init__'  , quasi_dialog    , 2],       \
                               ['add_button', quasi_add_button, 3],       \
                               ['run'       , quasi_run,        1],       \
                          ],                                              \
                          [                                               \
                          ]
                      )

objects   = [                                                             \
                quasi_actiongroup_object,                                 \
                quasi_button_object,                                      \
                quasi_dialog_object                                       \
            ]

def get_all():
    return (functions, stubs, variables, modules, objects)
