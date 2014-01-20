'''
Created on 15.06.2013

@author: bronikkk
'''

import ast

def initBuiltinFunction(scope, name, quasi, num,
                        defaults = None, listArgs = False, dictArgs = False):
    from ti.tgnode import ExternalFunctionDefinitionTGNode, EdgeType
    func = ExternalFunctionDefinitionTGNode(num, quasi, name, scope,
                                            defaults, listArgs, dictArgs)
    var  = scope.findOrAddName(name)
    EdgeType.processAssign(func, var)
    scope.addVariable(var)

def initBuiltinVariable(scope, name, typeFunction):
    from ti.tgnode import VariableTGNode, EdgeType 
    ext = VariableTGNode(None, typeFunction())
    var = scope.findOrAddName(name)
    EdgeType.processAssign(ext, var)
    scope.addVariable(var)

def initBuiltinClass(scope, name, methods, fields):
    from ti.tgnode import ClassTGNode, EdgeType
    cls = ClassTGNode(name, scope)
    var = scope.findOrAddName(name)
    EdgeType.processAssign(cls, var)
    scope.addVariable(var)
    classScope = cls.getScope()
    for method in methods:
        initBuiltinFunction(classScope, *method)
    for field in fields:
        initBuiltinVariable(classScope, *field)

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

def getClass(name):
    import config
    scope = config.data.currentScope
    var   = scope.findName(name)
    assert len(var.nodeType) == 1
    return list(var.nodeType)[0]

def getDictClass():
    from std.builtin_ import getDictClassName
    return getClass(getDictClassName())

def getListClass():
    from std.builtin_ import getListClassName
    return getClass(getListClassName())
    
def getBaseStringClass():
    from std.builtin_ import getBaseStringClassName
    return getClass(getBaseStringClassName())

def getSysPathType():
    from std.sys_ import findSysName
    return findSysName('path')

operatorNames = {
                    ast.Add      : '+'  ,
                    ast.And      : 'and',
                    ast.BitAnd   : '&'  ,
                    ast.BitOr    : '|'  ,
                    ast.Div      : '/'  ,
                    ast.FloorDiv : '//' ,
                    ast.Invert   : '~'  ,
                    ast.LShift   : '<<' ,
                    ast.Mult     : '*'  ,
                    ast.Mod      : '%'  ,
                    ast.Not      : '!'  ,
                    ast.Or       : 'or' ,
                    ast.Pow      : '**' ,
                    ast.RShift   : '>>' ,
                    ast.Sub      : '-'  ,
                    ast.UAdd     : '+'  ,
                    ast.USub     : '-'  ,
                }

def getOperatorName(node):
    return operatorNames[node.__class__]
