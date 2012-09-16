'''
Created on 25.03.2012

@author: bronikkk
'''

import ast

def init_builtin_function(scope, name, quasi, num, def_vals = {}):
    from typegraph import ExternFuncDefTypeGraphNode, DependencyType
    func = ExternFuncDefTypeGraphNode(num, quasi, name, scope, def_vals)
    var  = scope.findOrAdd(name)
    func.addDependency(DependencyType.Assign, var)
    scope.add(var)

def init_builtin_stub(scope, name, quasi):
    from tivisitor import TIVisitor
    from typegraph import UsualFuncDefTypeGraphNode, DependencyType
    module  = ast.parse(quasi)
    stmt    = module.body[0]
    visitor = TIVisitor(None)
    visitor.visit(stmt)

def init_builtin_variable(scope, name, type_func):
    from typegraph import ExternVarTypeGraphNode, DependencyType
    ext  = ExternVarTypeGraphNode(name, type_func())
    var  = scope.findOrAdd(name)
    ext.addDependency(DependencyType.Assign, var)
    scope.add(var)

def init_builtin_object(scope, name, methods, fields):
    from typegraph import ExternClassDefTypeGraphNode, DependencyType
    obj = ExternClassDefTypeGraphNode(name, scope)
    var = scope.findOrAdd(name)
    obj.addDependency(DependencyType.Assign, var)
    scope.add(var)
    obj_scope = obj.getScope()
    for method in methods:
        init_builtin_function(obj_scope, *method)

def import_standard_module(module, importer):
    if module.isLoaded:
        return
    command = 'from std.%s import get_all' % module.name
    exec command
    functions, stubs, variables, modules, objects = get_all()
    scope = module.getScope()
    for func in functions:
        init_builtin_function(scope, *func)
    for stub in stubs:
        init_builtin_stub(scope, *stub)
    for var in variables:
        init_builtin_variable(scope, *var)
    for mod in modules:
        importer.add_module(scope, *mod)
    for obj in objects:
        init_builtin_object(scope, *obj)
    module.isLoaded = True

class QuasiModule(object):
    def __init__(self, name, scope):
        self.name     = name
        self.scope    = scope
        self.isLoaded = False

    def getScope(self):
        return self.scope

def init_builtins(global_scope, importer):
    builtin_module = QuasiModule('builtin', global_scope)
    import_standard_module(builtin_module, importer)

def get_quasi_list():
    import __main__
    from std.builtin import get_quasi_list_name
    var = __main__.current_scope.find(get_quasi_list_name())
    cls = list(var.nodeType)[0]
    return cls
