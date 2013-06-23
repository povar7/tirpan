'''
Created on 09.06.2013

@author: bronikkk
'''

import copy
import itertools

import config
import ti.lookup
import ti.sema
import ti.tgnode
import ti.visitor

def getFunctions(functionNode):
    for elem in functionNode.nodeType:
        if isinstance(elem, ti.sema.FunctionSema):
            yield elem, False
        elif isinstance(elem, ti.sema.ClassSema):
            var = ti.lookup.lookupVariable(elem, '__init__')
            if var:
                for atom in var.nodeType:
                    if isinstance(atom, ti.sema.FunctionSema):
                        yield atom, True
            else:
                yield elem, True

def linkCall(function, isInit, kwKeys,
             argsTypes, listArgsTypes, dictArgsTypes):

    origin    = function.origin
    params    = origin.getOrdinaryParams()
    listParam = origin.getListParam()
    dictParam = origin.getDictParam()

    scope = ti.sema.ScopeSema()
    inst  = None
    
    index = 0
    for param in params:
        paramCopy = copy.deepcopy(param)
        try:
            argType = argsTypes[index]
            if isInit and index == 0:
                try:
                    inst = argType.getClassInstance()
                    argType = inst
                except AttributeError:
                    pass
            paramCopy.nodeType = {argType}
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

    return inst, scope

def matchCall(function, argumentNodes, KWArgumentNodes):
    origin      = function.origin

    defaults    = origin.getDefaults()
    params      = origin.getAllParams()

    classes = (ti.sema.ClassSema, ti.sema.CollectionSema)
    if isinstance(function.parent, classes):
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
    index = 0

    if firstParam:
        normResultTypes = [{firstParam}]
    else:
        normResultTypes = []
    for elem in normResult:
        if isinstance(elem, set):
            normResultTypes.append(elem)
        elif elem:
            normResultTypes.append(elem.nodeType)
        else:
            normResultTypes.append(listArgumentType[index])
            index += 1

    listResultTypes = []
    # DON'T set index = 0
    for elem in listResult:
        if elem:
            listResultTypes.append(elem.nodeType)
        else:
            listResultTypes.append(listArgumentType[index])
            index += 1
  
    kwKeys = []
    dictResultTypes = []
    for pair in dictResult.items():
        kwKeys.append(pair[0])
        dictResultTypes.append(pair[1].nodeType)

    for elem in itertools.product(itertools.product(*normResultTypes),
                                  itertools.product(*listResultTypes),
                                  itertools.product(*dictResultTypes)):
        yield elem, kwKeys

def processProductElement(function, isInit, tgnode, productElement, kwKeys):
    key         = productElement
    origin      = function.origin
    templates   = origin.getTemplates()
    template    = templates.get(key)
    newTemplate = template is None
    if newTemplate:
        inst, params = linkCall(function, isInit, kwKeys, *productElement)
        template = ti.tgnode.FunctionTemplateTGNode(params, origin, inst)
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
            if not origin.name:
                astCopy[0].link.addEdge(ti.tgnode.EdgeType.ASSIGN, template)
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

def processFunc(node, functionNode, argumentNodes, KWArgumentNodes,
                listArgumentType):
    for function, isInit in getFunctions(functionNode):
        if not isinstance(function, ti.tgnode.FunctionSema):
            continue
        matchResult = matchCall(function, argumentNodes, KWArgumentNodes)
        if not matchResult:
            continue
        for productElement, kwKeys in getProductElements(listArgumentType,
                                                         *matchResult):
            processProductElement(function, isInit,
                                  node, productElement, kwKeys)
