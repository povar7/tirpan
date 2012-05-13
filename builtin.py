'''
Created on 25.03.2012

@author: bronikkk
'''

from typegraph import *

def init_builtin_function(scope, name, quasi, num, def_vals = {}):
    func = ExternFuncDefTypeGraphNode(num, quasi, name, scope, def_vals)
    var  = scope.findOrAdd(name)
    func.addDependency(DependencyType.Assign, var)
    scope.add(var)

def init_builtin_variable(scope, name, type_func):
    ext  = ExternVarTypeGraphNode(name, type_func())
    var  = scope.findOrAdd(name)
    ext.addDependency(DependencyType.Assign, var)
    scope.add(var)

def import_standard_module(module, importer):
    if module.isLoaded:
        return
    command = 'from std.%s import get_all' % module.name
    exec command
    functions, variables, modules = get_all()
    scope = module.getScope()
    for func in functions:
        init_builtin_function(scope, *func)
    for var in variables:
        init_builtin_variable(scope, *var)
    for mod in modules:
        importer.add_module(scope, *mod)
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
