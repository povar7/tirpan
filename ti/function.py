'''
Created on 09.06.2013

@author: bronikkk
'''

import copy
import itertools

import config
import ti.sema
from   ti.tgnode  import EdgeType, FunctionTemplateTGNode
from   ti.visitor import Visitor

def linkCall(function, argumentTypes):
    origin = function.origin
    params = origin.getAllParams()
    scope  = ti.sema.ScopeSema()
    index  = 0
    for param in params:
        paramCopy = copy.deepcopy(param)
        try:
            paramCopy.nodeType = {argumentTypes[index]}
        except IndexError:
            paramCopy.nodeType = set()
        scope.addVariable(paramCopy)
        index += 1
    return scope

def matchCall(function, argumentNodes):
    origin      = function.origin

    defaults    = origin.getDefaults()
    params      = origin.getAllParams()

    paramIndex  = 0
    paramNumber = len(params)

    argIndex    = 0
    argNumber   = len(argumentNodes)

    normResult  = []
    listResult  = []
    dictResult  = {}

    while True:
        if paramIndex >= paramNumber:
            break
        param = params[paramIndex]
        if param.name in defaults:
            if argIndex < argNumber:
                normResult.append(argumentNodes[argIndex])
                argIndex += 1
            else:
                normResult.append(defaults[param.name])
            paramIndex += 1
            continue
        elif origin.isListParam(param):
            listResult  = argumentNodes[argIndex:argNumber]
            argIndex    = argNumber
            paramIndex += 1
        elif origin.isDictParam(param):
            # We must also generate dictResult here
            paramIndex += 1 
        else:
            if argIndex >= argNumber:
                # We must also check for dict values here
                return None
            normResult.append(argumentNodes[argIndex])
            argIndex   += 1
            paramIndex += 1

    if argIndex < argNumber:
        return None

    return normResult, listResult, dictResult

def getProductElements(normResult, listResult, dictResult):
    normResultTypes = [elem.nodeType for elem in normResult]
    for elem in itertools.product(*normResultTypes):
        yield elem

def processProductElement(function, tgnode, argumentTypes):
    key       = argumentTypes
    origin    = function.origin
    templates = origin.getTemplates()
    template  = templates.get(key)
    if not template:
        params   = linkCall(function, argumentTypes)
        template = FunctionTemplateTGNode(params, origin.getParent())
        templates[key] = template
        template.addEdge(EdgeType.ASSIGN, tgnode)
        save = config.data.currentScope
        templateScope = template.getScope()
        astCopy = copy.deepcopy(origin.ast)
        visitor = Visitor(None)
        config.data.currentScope = ti.sema.ScopeSema(templateScope)
        for stmt in astCopy:
            visitor.visit(stmt)
        config.data.currentScope = save

def processCall(node, functionNode, argumentNodes):
    for function in functionNode.nodeType:
        matchResult = matchCall(function, argumentNodes)
        if not matchResult:
            continue
        for productElement in getProductElements(*matchResult):
            processProductElement(function, node, productElement)
