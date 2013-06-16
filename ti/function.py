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

def linkCall(function, kwKeys, argsTypes, listArgsTypes, dictArgsTypes):
    origin    = function.origin
    params    = origin.getOrdinaryParams()
    listParam = origin.getListParam()
    dictParam = origin.getDictParam()

    scope = ti.sema.ScopeSema()
    
    index = 0
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

    index = 0
    if dictParam:
        dictParamCopy = copy.deepcopy(dictParam)
        dictType  = ti.sema.DictSema()
        for key in kwKeys:
            keyElement = ti.sema.LiteralValueSema(key)
            dictType.elems[keyElement] = {dictArgsTypes[index]}
            index += 1
        dictParamCopy.nodeType = {dictType}
        scope.addVariable(dictParamCopy)

    return scope

def matchCall(function, argumentNodes, KWArgumentNodes):
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
            paramIndex += 1
            dictResult  = KWArgumentNodes
        else:
            if argIndex >= argNumber:
                try:
                    nameParam = KWArgumentNodes[param.name]
                    del KWArgumentNodes[param.name]
                    normResult.append(nameParam)
                    paramIndex += 1
                except KeyError:
                    return None
            else:
                normResult.append(argumentNodes[argIndex])
                argIndex   += 1
                paramIndex += 1

    if argIndex < argNumber:
        return None

    return normResult, listResult, dictResult, firstParam

def getProductElements(listArgumentType,
                       normResult, listResult, dictResult, firstParam):
    if firstParam:
        normResultTypes = [{firstParam}]
    else:
        normResultTypes = []

    index = 0
    for elem in normResult:
        if elem:
            normResultTypes.append(elem.nodeType)
        else:
            normResultTypes.append(listArgumentType[index])
            index += 1

    listResultTypes  = [elem.nodeType for elem in listResult]
  
    kwKeys = []
    dictResultTypes = []
    for pair in dictResult.items():
        kwKeys.append(pair[0])
        dictResultTypes.append(pair[1].nodeType)

    for elem in itertools.product(itertools.product(*normResultTypes),
                                  itertools.product(*listResultTypes),
                                  itertools.product(*dictResultTypes)):
        yield elem, kwKeys

def processProductElement(function, tgnode, productElement, kwKeys):
    key         = productElement
    origin      = function.origin
    templates   = origin.getTemplates()
    template    = templates.get(key)
    newTemplate = template is None
    if newTemplate:
        params   = linkCall(function, kwKeys, *productElement)
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

def processCall(node, functionNode, argumentNodes, KWArgumentNodes,
                listArgumentType):
    for function in functionNode.nodeType:
        if not isinstance(function, ti.tgnode.FunctionSema):
           continue
        matchResult = matchCall(function, argumentNodes, KWArgumentNodes)
        if not matchResult:
            continue
        for productElement, kwKeys in getProductElements(listArgumentType, *matchResult):
            processProductElement(function, node, productElement, kwKeys)
