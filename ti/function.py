'''
Created on 09.06.2013

@author: bronikkk
'''

import copy
import itertools

import config
import ti.checkers
import ti.lookup
import ti.sema
import ti.skips
import ti.tgnode
import ti.visitor
import utils

class Flags(object):

    def __init__(self):
        self._destructive = False

    def isDestructive(self):
        return self._destructive

    def setDestructive(self):
        self._destructive = True

def copyParam(param):
    paramCopy = copy.copy(param)
    paramCopy.edges = {}
    paramCopy.nodeType = set()
    return paramCopy

def getNodeType(elem):
    if (len(elem.nodeType) > 0 or
        ti.tgnode.EdgeType.REV_ASSIGN_ELEMENT in elem.edges):
        return elem.nodeType
    else:
        return {None}

def makeSet(elem):
    if elem is not None:
        return {elem}
    else:
        return set()

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

    if isinstance(function, ti.sema.ClassSema):
        argType = argsTypes[0]
        inst = argType.getClassInstance()
        return None, inst

    origin    = function.origin
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
                paramCopy.nodeType = makeSet(argType)
        except IndexError:
            paramCopy.nodeType = set()
        scope.addVariable(paramCopy)
        index += 1

    if listParam:
        listParamCopy = copyParam(listParam)
        tupleType = ti.sema.TupleSema(0)
        for elem in listArgsTypes:
            tupleType.elems.append(makeSet(elem))
        listParamCopy.nodeType = {tupleType}
        scope.addVariable(listParamCopy)

    index = 0
    if dictParam:
        dictParamCopy = copyParam(dictParam)
        dictType  = ti.sema.DictSema()
        for key in kwKeys:
            keyElement = ti.sema.LiteralValueSema(key)
            dictType.elems[keyElement] = makeSet(dictArgsTypes[index])
            index += 1
        dictParamCopy.nodeType = {dictType}
        scope.addVariable(dictParamCopy)

    return scope, inst

def matchCall(function, isInit, argumentNodes, KWArgumentNodes):
    origin = function.origin

    if isinstance(function, ti.sema.FunctionSema):
        params   = origin.getAllParams()
        defaults = origin.getDefaults()
        parent   = function.parent
    else:
        params   = []
        defaults = {}
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
            normResultTypes.append(getNodeType(elem))
        else:
            normResultTypes.append(listArgumentType[index])
            index += 1

    listResultTypes = []
    # DON'T set index = 0
    for elem in listResult:
        if elem:
            listResultTypes.append(getNodeType(elem))
        else:
            listResultTypes.append(listArgumentType[index])
            index += 1
  
    kwKeys = []
    dictResultTypes = []
    for pair in dictResult.items():
        kwKeys.append(pair[0])
        dictResultTypes.append(getNodeType(pair[1]))

    for elem in itertools.product(itertools.product(*normResultTypes),
                                  itertools.product(*listResultTypes),
                                  itertools.product(*dictResultTypes)):
        yield elem, kwKeys

def processProductElement(function, isInit, tgNode, productElement, kwKeys):
    btrace = config.data.backTrace
    origin = function.origin

    if isInit or origin.isGlobalDestructive():
        key = productElement, tgNode
    else:
        key = productElement, None

    templates   = origin.getTemplates()
    template    = templates.get(key)
    newTemplate = template is None

    if newTemplate:
        params, inst = linkCall(function, isInit, kwKeys, *productElement)
        template = ti.tgnode.FunctionTemplateTGNode(params, origin,
                                                    inst  , tgNode)
    if (tgNode, ()) not in template.edges:
        template.addEdge(ti.tgnode.EdgeType.ASSIGN, tgNode)
     
    globalDestructive = False

    if newTemplate:
        templates[key] = template
        save = config.data.currentScope

        if (isinstance(origin, ti.tgnode.UsualFunctionDefinitionTGNode) or
            isinstance(origin, ti.tgnode.ForFunctionDefinitionTGNode)):
            astCopy  = copy.deepcopy(origin.ast)
            filename = utils.getFileName(astCopy[0])
            visitor  = ti.visitor.Visitor(filename)
            
            templateScope = template.getScope()
            config.data.currentScope = ti.sema.ScopeSema(templateScope)

            if isinstance(origin, ti.tgnode.UsualFunctionDefinitionTGNode):
                usual = True
            else:
                usual = False
                var = params.findName(origin.ITER_NAME)
                targetCopy = copy.deepcopy(origin.target)
                visitor.visit_common_target(var, targetCopy)

            if usual:
                btrace.addFrame(tgNode.node, save, function, productElement)

            for stmt in astCopy:
                res = visitor.visit(stmt)
                if res == visitor.SKIP_NEXT:
                    break

            if usual:
                btrace.deleteFrame()

            config.data.currentScope = save

            if not origin.name:
                astCopy[0].link.addEdge(ti.tgnode.EdgeType.ASSIGN, template)

            try:
                globalDestructive = origin.isGlobalDestructive()
            except AttributeError:
                pass
        elif isinstance(origin, ti.tgnode.ExternalFunctionDefinitionTGNode):
            unsorted     = [var for var in params.variables.values()
                            if var.number]
            sortParams   = ti.tgnode.FunctionDefinitionTGNode.sortParams
            sortedParams = sorted(unsorted, sortParams)
            types = []
            for param in sortedParams:
                assert len(param.nodeType) <= 1
                try:
                    newType = list(param.nodeType)[0]
                except IndexError:
                    newType = None
                types.append(newType)

            btrace.addFrame(tgNode.node, save, function, productElement)
            flags = Flags()
            template.nodeType = origin.quasi(types,
                                             NODE=tgNode.node,
                                             FLAGS=flags)
            ti.checkers.checkBasenameCall(tgNode.node,
                                          function,
                                          types)
            btrace.deleteFrame()

            template.walkEdges()

            globalDestructive = ti.skips.checkGlobalDestructive(flags,
                                                                tgNode.node)

        if globalDestructive:
            config.data.currentScope.setGlobalDestructive()

def processFunc(node, functionNode, argumentNodes, KWArgumentNodes,
                listArgumentType):
    classes = (ti.sema.FunctionSema, ti.sema.ClassSema)
    for function, isInit in getFunctions(functionNode):
        if not isinstance(function, classes):
            continue
        matchResult = matchCall(function, isInit,
                                argumentNodes, KWArgumentNodes)
        if not matchResult:
            continue
        for productElement, kwKeys in getProductElements(listArgumentType,
                                                         *matchResult):
            processProductElement(function, isInit,
                                  node, productElement, kwKeys)
