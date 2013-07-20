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
    ext = VariableTGNode(None, typeFunction())
    var = scope.findOrAddName(name)
    ext.addEdge(EdgeType.ASSIGN, var)
    scope.addVariable(var)

def initBuiltinClass(scope, name, methods, fields):
    from ti.tgnode import ClassTGNode, EdgeType
    cls = ClassTGNode(name, [], scope)
    var = scope.findOrAddName(name)
    cls.addEdge(EdgeType.ASSIGN, var)
    scope.addVariable(var)
    classScope = cls.getScope()
    for method in methods:
        initBuiltinFunction(classScope, *method)

class QuasiModule(object):

    def __init__(self, name, scope):
        self.name     = name
        self.scope    = scope
        self.isLoaded = False

    def getScope(self):
        return self.scope

def initBuiltins(importer, globalScope): 
    builtinModule = QuasiModule('builtin', globalScope)
    importer.importStandardModule(builtinModule, globalScope)
    builtinModule.isLoaded = True

def getListClass():
    import config
    from   std.builtin_ import getListClassName
    var = config.data.currentScope.findName(getListClassName())
    assert(len(var.nodeType) == 1)
    return list(var.nodeType)[0]

def getBaseStringClass():
    import config
    from   std.builtin_ import getBaseStringClassName
    var = config.data.currentScope.findName(getBaseStringClassName())
    assert(len(var.nodeType) == 1)
    return list(var.nodeType)[0]
