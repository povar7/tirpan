'''
Created on 15.06.2013

@author: bronikkk
'''

def initBuiltinFunction(scope, name, quasi, num, defaults = None):
    from ti.tgnode import ExternalFunctionDefinitionTGNode, EdgeType
    func = ExternalFunctionDefinitionTGNode(num, quasi, name, scope, defaults)
    var  = scope.findOrAddName(name)
    func.addEdge(EdgeType.ASSIGN, var)
    scope.addVariable(var)

def initBuiltinVariable(scope, name, typeFunction):
    from ti.tgnode import VariableTGNode, EdgeType 
    ext = VariableTGNode(name, typeFunction)
    var = scope.findOrAddName(name)
    ext.addEdge(EdgeType.ASSIGN, var)
    scope.addVariable(var)

def initBuiltinClass(scope, name, methods, fields):
    from ti.tgnode import ClassTGNode, EdgeType
    cls = ClassTGNode(name, scope)
    var = scope.findOrAddName(name)
    cls.addEdge(EdgeType.ASSIGN, var)
    scope.addVariable(var)
    classScope = cls.getScope()
    for method in methods:
        initBuiltinFunction(classScope, *method)

def importStandardModule(module, importer, name = None):
    name = name or module.name
    command = 'from std.%s_ import getAll' % name
    exec command
    functions, variables, modules, classes = getAll()
    scope = module.getScope()
    for func in functions:
        initBuiltinFunction(scope, *func)
    for var in variables:
        initBuiltinVariable(scope, *var)
    for mod in modules:
        importer.addModule(scope, *mod)
    for cls in classes:
        initBuiltinClass(scope, *cls)

class QuasiModule(object):

    def __init__(self, name, scope):
        self.name     = name
        self.scope    = scope
        self.isLoaded = False

    def getScope(self):
        return self.scope

def initBuiltins(importer, globalScope): 
    builtinModule = QuasiModule('builtin', globalScope)
    importStandardModule(builtinModule, importer)
    builtinModule.isLoaded = True

def getListClass():
    import config
    from   std.builtin_ import getListClassName
    var = config.data.currentScope.findName(getListClassName())
    assert(len(var.nodeType) == 1)
    return list(var.nodeType)[0]
