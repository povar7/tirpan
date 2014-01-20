'''
Created on 09.06.2013

@author: bronikkk
'''

import copy
import itertools

import config
import ti.lookup
import ti.mir
import ti.mvisitor
import ti.sema
import ti.tgnode
import ti.visitor
import utils

classes = (ti.sema.FunctionSema, ti.sema.ClassSema)

typeNone = ti.sema.getNoneSema()

def copyParam(param):
    paramCopy = copy.copy(param)
    paramCopy.nodeType = set()
    return paramCopy

def getParamsTypes(params):
    unsorted = [var for var in params.variables.values() if var.number]
    sortedParams = sorted(unsorted, sortParams)
    types = []
    for param in sortedParams:
        assert len(param.nodeType) <= 1
        try:
            newType = list(param.nodeType)[0]
        except IndexError:
            newType = None
        types.append(newType)
    return types

def linkCall(function, isInit, kwKeys,
             argsTypes, listArgsTypes, dictArgsTypes):

    if isinstance(function, ti.sema.ClassSema):
        argType = argsTypes[0]
        inst = argType.getClassInstance()
        return None, inst

    origin    = function.getOrigin()
    params    = origin.getOrdinaryParams()
    listParam = origin.getListParam()
    dictParam = origin.getDictParam()

    scope = ti.sema.ScopeSema()
    inst  = None
    index = 0
    for param in params:
        paramCopy = copyParam(param)
        try:
            argType = argsTypes[index]
            if isInit and index == 0:
                inst = argType.getClassInstance()
                paramCopy.nodeType = {inst}
            else:
                paramCopy.nodeType = utils.makeSet(argType)
        except IndexError:
            paramCopy.nodeType = set()
        scope.addVariable(paramCopy)
        index += 1

    if listParam:
        listParamCopy = copyParam(listParam)
        tupleType = ti.sema.TupleSema(0)
        for elem in listArgsTypes:
            tupleType.elems.append(utils.makeSet(elem))
        listParamCopy.nodeType = {tupleType}
        scope.addVariable(listParamCopy)

    index = 0
    if dictParam:
        dictParamCopy = copyParam(dictParam)
        dictType  = ti.sema.DictSema()
        for key in kwKeys:
            keyElement = ti.sema.LiteralValueSema(key)
            dictType.elems[keyElement] = utils.makeSet(dictArgsTypes[index])
            index += 1
        dictParamCopy.nodeType = {dictType}
        scope.addVariable(dictParamCopy)

    return scope, inst

def matchCall(function, isInit, argumentNodes, KWArgumentNodes):
    origin = function.getOrigin()

    if isinstance(function, ti.sema.FunctionSema):
        params   = origin.getAllParams()
        defaults = origin.getDefaults()
        parent   = function.parent
    else:
        params   = []
        defaults = dict()
        parent   = function

    if (isinstance(parent, ti.sema.ClassSema) and isInit or
        isinstance(parent, (ti.sema.CollectionSema,
                            ti.sema.LiteralSema, 
                            ti.sema.InstanceSema))):
        paramIndex = 1
        firstParam = parent
    else:
        paramIndex = 0
        firstParam = None
    paramNumber = len(params)

    argIndex    = 0
    argNumber   = len(argumentNodes)

    normResult  = []
    listResult  = []
    dictResult  = dict()

    while True:
        if paramIndex >= paramNumber:
            break
        param = params[paramIndex]
        if param.name in defaults:
            if argIndex < argNumber:
                normResult.append(argumentNodes[argIndex])
                argIndex += 1
            else:
                try:
                    nameParam = KWArgumentNodes[param.name]
                    normResult.append(nameParam)
                except KeyError:
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
            normResultTypes.append(utils.getNodeType(elem))
        else:
            normResultTypes.append(listArgumentType[index])
            index += 1

    listResultTypes = []
    # DON'T set index = 0
    for elem in listResult:
        if elem:
            listResultTypes.append(utils.getNodeType(elem))
        else:
            listResultTypes.append(listArgumentType[index])
            index += 1
  
    kwKeys = []
    dictResultTypes = []
    for pair in dictResult.items():
        kwKeys.append(pair[0])
        dictResultTypes.append(utils.getNodeType(pair[1]))

    for elem in itertools.product(itertools.product(*normResultTypes),
                                  itertools.product(*listResultTypes),
                                  itertools.product(*dictResultTypes)):
        yield elem, kwKeys

def processProductElement(function, isInit, tgNode, productElement, kwKeys):
    origin = function.getOrigin()
    params, inst = linkCall(function, isInit, kwKeys, *productElement)
    if isinstance(origin, ti.tgnode.UsualFunctionDefinitionTGNode):
        tree = origin.ast
        if len(tree) == 0:
            return {typeNone}
        first_node = tree[0]
        filename   = utils.getFileName(first_node)
        if not origin.mir:
            origin.mir  = ti.mir.BeginMirNode()
            ast_visitor = ti.visitor.Visitor(filename, origin.mir)
            for stmt in tree:
                ast_visitor.visit(stmt)
        template = ti.tgnode.FunctionTemplateTGNode(params, origin,
                                                    inst  , tgNode)
        scope = config.data.currentScope
        config.data.currentScope = ti.sema.ScopeSema(template.getScope())
        file_scope = utils.getFileScope(first_node)
        ti.mir.walkChain(origin.mir, file_scope)
        config.data.currentScope = scope
        if inst:
            return {inst}
        else:
            return set()
    elif isinstance(origin, ti.tgnode.ExternalFunctionDefinitionTGNode):
        types = getParamsTypes(params)
        return origin.quasi(types, TGNODE=tgNode)

def processFunc(node, functionNode, argumentNodes, KWArgumentNodes,
                listArgumentType):
    types = set()
    if not functionNode:
        return types
    for function, isInit in ti.lookup.getFunctions(functionNode):
        if not isinstance(function, classes):
            continue
        matchResult = matchCall(function, isInit,
                                argumentNodes, KWArgumentNodes)
        if not matchResult:
            continue
        for productElement, kwKeys in getProductElements(listArgumentType,
                                                         *matchResult):
            types |= processProductElement(function, isInit,
                                           node, productElement, kwKeys)
    return types
