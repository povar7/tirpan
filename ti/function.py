'''
Created on 09.06.2013

@author: bronikkk
'''

import copy
import itertools

import config
import ti.sema
import ti.tgnode
import ti.visitor

def linkCall(function, argsTypes, listArgsTypes):
    origin    = function.origin
    params    = origin.getOrdinaryParams()
    listParam = origin.getListParam()
    scope     = ti.sema.ScopeSema()
    index     = 0
    for param in params:
        paramCopy = copy.deepcopy(param)
        try:
            paramCopy.nodeType = {argsTypes[index]}
        except IndexError:
            paramCopy.nodeType = set()
        scope.addVariable(paramCopy)
        index += 1
    if listParam:
        listParamCopy = copy.deepcopy(listParam)
        tupleType = ti.sema.TupleSema(0)
        for elem in listArgsTypes:
            tupleType.elems.append({elem})
        listParamCopy.nodeType = {tupleType}
        scope.addVariable(listParamCopy)
    return scope

def matchCall(function, argumentNodes):
    origin      = function.origin

    defaults    = origin.getDefaults()
    params      = origin.getAllParams()

    if isinstance(function.parent, ti.sema.CollectionSema):
        paramIndex = 1
        firstParam = function.parent
    else:
        paramIndex = 0
        firstParam = None
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

    return normResult, listResult, dictResult, firstParam

def getProductElements(normResult, listResult, dictResult, firstParam):
    if firstParam:
        normResultTypes = [{firstParam}]
    else:
        normResultTypes = []
    normResultTypes += [elem.nodeType for elem in normResult]
    listResultTypes  = [elem.nodeType for elem in listResult]
    for elem in itertools.product(itertools.product(*normResultTypes),
                                  itertools.product(*listResultTypes)):
        yield elem

def processProductElement(function, tgnode, productElement):
    key         = productElement
    origin      = function.origin
    templates   = origin.getTemplates()
    template    = templates.get(key)
    newTemplate = template is None
    if newTemplate:
        params   = linkCall(function, *productElement)
        template = ti.tgnode.FunctionTemplateTGNode(params, origin)
    if (tgnode, ()) not in template.edges:
        template.addEdge(ti.tgnode.EdgeType.ASSIGN, tgnode)
    if newTemplate:
        templates[key] = template
        save = config.data.currentScope
        templateScope = template.getScope()
        if isinstance(origin, ti.tgnode.UsualFunctionDefinitionTGNode):
            astCopy = copy.deepcopy(origin.ast)
            visitor = ti.visitor.Visitor(None)
            config.data.currentScope = ti.sema.ScopeSema(templateScope)
            for stmt in astCopy:
                visitor.visit(stmt)
            config.data.currentScope = save
        else:
            unsorted = [var for var in params.variables.values() if var.number]
            sortParams = ti.tgnode.FunctionDefinitionTGNode.sortParams
            sortedParams = sorted(unsorted, sortParams)
            types = []
            for param in sortedParams:
                assert(len(param.nodeType) == 1)
                types.append(list(param.nodeType)[0])
            template.nodeType = origin.quasi(types)
            template.walkEdges()

def processCall(node, functionNode, argumentNodes):
    for function in functionNode.nodeType:
        if not isinstance(function, ti.tgnode.FunctionSema):
           continue
        matchResult = matchCall(function, argumentNodes)
        if not matchResult:
            continue
        for productElement in getProductElements(*matchResult):
            processProductElement(function, node, productElement)
