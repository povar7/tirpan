'''
Created on 26.05.2013

@author: bronikkk
'''

import ast
import copy
import os
import types
import itertools

import config
import ti.lookup
from   ti.sema   import *

classes = (CollectionSema, LiteralSema, ClassSema, InstanceSema, ModuleSema)

class EdgeType(object):

    ARGUMENT           = 'Argument'
    ASSIGN             = 'Assign'
    ASSIGN_CUSTOM      = 'AssignCustom'
    ASSIGN_ELEMENT     = 'AssignElement'
    ASSIGN_INDEX       = 'AssignIndex'
    ASSIGN_ITER        = 'AssignIter'
    ASSIGN_OBJECT      = 'AssignObject'
    ASSIGN_SLICE       = 'AssignSlice'
    ASSIGN_TRUE        = 'AssignTrue'
    ASSIGN_YIELD       = 'AssignYield'
    ATTR_INDEX         = 'AttrIndex'
    ATTR_SLICE         = 'AttrSlice'
    ATTR_OBJECT        = 'AttrObject'
    ELEMENT            = 'Element'
    FUNC               = 'Func'
    KWARGUMENT         = 'KWArgument'
    LISTARGUMENT       = 'ListArgument'
    REV_ARGUMENT       = 'RevArgument'
    REV_ASSIGN         = 'RevAssign'
    REV_ASSIGN_ELEMENT = 'RevAssignElement'
    REV_ELEMENT        = 'RevElement'
    REV_FUNC           = 'RevFunc'
    REV_KWARGUMENT     = 'RevKWArgument'
    REV_LISTARGUMENT   = 'RevListArgument'

    @staticmethod
    def updateRight(right, types):
        if len(types - right.nodeType) > 0:
            length = len(right.nodeType)
            right.nodeType |= types
            if len(right.nodeType) > length:
                right.process()
                right.walkEdges()

    @staticmethod
    def updateRightWithCondition(right, types, condition):
        if len(types - right.nodeType) > 0:
            length = len(right.nodeType)
            for elem in types:
                if condition(elem):
                    right.nodeType.add(elem)
            if len(right.nodeType) > length:
                right.process()
                right.walkEdges()

    @staticmethod
    def processArgument(left, right, *args):
        length = len(right.nodeType)
        right.processCall()
        if len(right.nodeType) > length:
            right.walkEdges()

    @staticmethod
    def processAssign(left, right, *args):
        update_flag = True

        # Remove simple loops in type variables graph (1)
        try:
            if (left, ()) in right.edges[EdgeType.ARGUMENT]:
                right.removeEdge(EdgeType.ARGUMENT, left)
        except KeyError:
            pass
        # Remove simple loops in type variables graph (2)
        subs = set()
        if isinstance(left, (TupleTGNode, ListTGNode)):
            try:
                for node, args in left.edges[EdgeType.REV_ELEMENT]:
                    if isinstance(node, SubscriptTGNode):
                        subs.add(node)
            except KeyError:
                pass
        elif isinstance(left, SubscriptTGNode):
            subs.add(left)
        for sub in subs:
            try:
                if (right, ()) in sub.edges[EdgeType.ASSIGN_OBJECT]:
                    sub.removeEdge(EdgeType.ASSIGN_OBJECT, right)
            except KeyError:
                pass
        # Remove simple loops in type variables graph (3)
        opers = [left]
        index = 0
        while index < len(opers):
            oper = opers[index]
            
            index += 1
            
            if isinstance(oper, FunctionCallTGNode):
                for new_index in range(oper.getArgumentNodesNumber()):
                    opers.append(oper.getArgumentNode(new_index))
                continue

            if oper == right:
                update_flag = False
                break

            try:
                if (right, ()) in oper.edges[EdgeType.ASSIGN_OBJECT]:
                    oper.removeEdge(EdgeType.ASSIGN_OBJECT, right)
            except KeyError:
                pass
            
        if update_flag:
            EdgeType.updateRight(right, left.nodeType)

    @staticmethod
    def processAssignCustom(left, right, *args):
        from ti.visitor import Visitor 
        test  = args[0]
        types = left.nodeType
        if test:
            def condition(x):
                visitor = Visitor(None, False)
                astCopy = copy.deepcopy(test.comparators[0])
                visitor.visit(astCopy)
                rType = astCopy.link.nodeType 
                lType = ti.lookup.lookupTypes(x, test.left.attr)
                return lType.issuperset(rType)
            EdgeType.updateRightWithCondition(right, types, condition)
        else:
            EdgeType.updateRight(right, types)

    @staticmethod
    def processAssignElement(left, right, *args):
        index = args[0]
        types = left.getElementsTypes(index)
        EdgeType.updateRight(right, types)

    @staticmethod
    def processAssignIndex(left, right, *args):
        pass

    @staticmethod
    def processAssignIter(left, right, *args):
        flag = args[0]
        def condition(x):
            try:
                x.getElements()
                return flag
            except:
                return not flag
        EdgeType.updateRightWithCondition(right, left.nodeType, condition)

    @staticmethod
    def processAssignObject(left, right, *args):
        pass

    @staticmethod
    def processAssignSlice(left, right, *args):
        pass

    @staticmethod
    def processAssignTrue(left, right, *args):
        flag = args[0]
        def condition(x):
            try:
                return flag if x.value else not flag
            except AttributeError:
                pass
            try:
                return flag if x.ltype != types.NoneType else not flag
            except AttributeError:
                pass
            try:
                return flag if len(x.getElements()) > 0 else not flag
            except AttributeError:
                pass
            return flag
        EdgeType.updateRightWithCondition(right, left.nodeType, condition)

    @staticmethod
    def processAssignYield(left, right, *args):
        listType = ListSema(0)
        listType.elems[0] |= left.nodeType
        types = {listType}
        EdgeType.updateRight(right, types)

    @staticmethod
    def processAttrIndex(left, right, *args):
        EdgeType.processCommon(left, right, args)

    @staticmethod
    def processAttrObject(left, right, *args):
        EdgeType.processCommon(left, right, args)

    @staticmethod
    def processAttrSlice(left, right, *args):
        EdgeType.processCommon(left, right, args)

    @staticmethod
    def processCommon(left, right, *args):
        length = len(right.nodeType)
        right.process()
        if len(right.nodeType) > length:
            right.walkEdges()

    @staticmethod
    def processElement(left, right, *args):
        try:
            index = args[0]
        except IndexError:
            index = None

        for obj in right.nodeType:
            if not isinstance(obj, CollectionSema):
                continue
            obj.addElementsAtIndex(index, left.nodeType)

        # Remove simple loops in type variables graph
        try:
            if (left, ()) in right.edges[EdgeType.ASSIGN]:
                right.removeEdge(EdgeType.ASSIGN, left)
        except KeyError:
            pass

        right.walkEdges()

    @staticmethod
    def processFunc(left, right, *args):
        length = len(right.nodeType)
        right.processCall()
        if len(right.nodeType) > length:
            right.walkEdges()

    @staticmethod
    def processKWArgument(left, right, *args):
        length = len(right.nodeType)
        right.processCall()
        if len(right.nodeType) > length:
            right.walkEdges()

    @staticmethod
    def processListArgument(left, right, *args):
        length = len(right.nodeType)
        right.processCall()
        if len(right.nodeType) > length:
            right.walkEdges()

    @staticmethod
    def isNotReverse(edgeType):
        return not edgeType.startswith('Rev')

    @staticmethod
    def isNotReverseAssign(edgeType):
        return edgeType != EdgeType.REV_ASSIGN

class TGNode(object):

    def __init__(self):
        self.edges    = {}
        self.nodeType = set()

    def addEdge(self, edgeType, node, *args):
        if edgeType == EdgeType.ASSIGN:
            node.addEdge(EdgeType.REV_ASSIGN, self)
        elif edgeType == EdgeType.ELEMENT:
            node.addEdge(EdgeType.REV_ELEMENT, self)
        if not edgeType in self.edges:
            self.edges[edgeType] = set()
        self.edges[edgeType].add((node, args))
        self.walkEdge(edgeType, node, *args)

    def removeEdge(self, edgeType, node):
        self.edges[edgeType].discard((node, ()))
    
    def walkEdge(self, edgeType, node, *args):
        if EdgeType.isNotReverse(edgeType):
            getattr(EdgeType, 'process' + edgeType)(self, node, *args)

    def walkEdges(self):
        for edgeType, edgeValue in self.edges.items():
            for node, args in edgeValue:
                self.walkEdge(edgeType, node, *args)

    def getEdges(self, edgeType):
        try:
            return self.edges[edgeType]
        except KeyError:
            return set()

    def getElementsTypes(self, index):
        res = set()
        for singleType in self.nodeType:
            res |= singleType.getElementsAtIndex(index)
        return res

    def commonRetrieve(self, attr, condition):
        memo   = set()
        result = set()

        data = (memo, result)
        self._commonRetrieve(attr, condition, data)

        return result

    def _commonRetrieve(self, attr, condition, data):
        memo, result = data
        if self in memo:
            return
        else:
            memo.add(self)

        callback = getattr(self, attr + 'Callback', None)
        if callback:
            callback(result)

        for edgeType, edgeValue in self.edges.items():
            if condition(edgeType):
                continue
            for node, args in edgeValue:
                node._commonRetrieve(attr, condition, data)

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash((self.__class__, id(self)))

class ConstTGNode(TGNode):

    def __init__(self, node, getValue = False):
        super(ConstTGNode, self).__init__()
        if isinstance(node, ast.Num):
            value = node.n
        elif isinstance(node, ast.Str):
            value = node.s
        elif (isinstance(node, ast.Name)   and node.id == 'None' or
              isinstance(node, (ast.Return, ast.Yield)) and not node.value):
            value = None
        else:
            assert False
        self.value = value
        if getValue:
            self.nodeType = {LiteralValueSema(value)}
        else:
            self.nodeType = {LiteralSema(value.__class__)}

    def getValue(self):
        return self.value

    def constantsCallback(self, result):
        if self.value is not None:
            newType = LiteralValueSema(self.value)
            if newType not in self.nodeType:
                self.nodeType.add(newType)
                self.walkEdges()

class VariableTGNode(TGNode):

    def __init__(self, name, nodeType = None):
        super(VariableTGNode, self).__init__()
        self.name   = name
        self.number = None
        # self.parent = None

        if nodeType is not None:
            self.nodeType = nodeType
        else:
            self.nodeType = set()

    def setNumber(self, number):
        self.number = number

    def setParent(self, parent):
        # self.parent = parent
        pass

    def process(self):
        pass

class ListTGNode(TGNode):

    def __init__(self, node):
        super(ListTGNode, self).__init__()
        if isinstance(node, ast.List):
            elems = node.elts
            listSema      = ListSema(len(elems))
            self.nodeType = {listSema}
            index = 0
            for elem in elems:
                link = elem.link
                link.addEdge(EdgeType.ELEMENT, self, index)
                index += 1
        else:
            link = node.elt.link
            listSema = ListSema()
            self.nodeType = {listSema}
            link.addEdge(EdgeType.ELEMENT, self)

class TupleTGNode(TGNode):

    def __init__(self, node):
        super(TupleTGNode, self).__init__()
        if isinstance(node, ast.ClassDef):
            elems = node.bases
        else:
            elems = node.elts
        tupleSema     = TupleSema(len(elems))
        self.nodeType = {tupleSema}
        if (isinstance(node, ast.Tuple) or
            isinstance(node, ast.ClassDef)):
            index = 0
            for elem in elems:
                link = elem.link
                link.addEdge(EdgeType.ELEMENT, self, index)
                index += 1

class DictTGNode(TGNode):

    def __init__(self):
        super(DictTGNode, self).__init__()
        dictSema = DictSema()
        self.nodeType = {dictSema}

class AttributeTGNode(TGNode):

    def __init__(self, attr):
        super(AttributeTGNode, self).__init__()
        self.attr = attr

    def getObjects(self):
       objects = set()
       for node, args in self.getEdges(EdgeType.ASSIGN_OBJECT):
           objects |= node.nodeType
       return objects

    def getRights(self):
       rights = set()
       for node, args in self.getEdges(EdgeType.REV_ASSIGN):
           rights |= node.nodeType
       return rights

    def process(self):
       objects = self.getObjects()
       rights  = self.getRights()
       self.setValues(objects, self.attr, rights)
       self.nodeType = self.getValues(objects, self.attr)

    @staticmethod
    def setValuesWithAttr(obj, attr, values):
        from ti.lookup import setTypes
        setTypes(obj, attr, values)

    @staticmethod
    def setValues(objects, attr, values):
        for obj in objects:
            if not isinstance(obj, classes):
                continue
            AttributeTGNode.setValuesWithAttr(obj, attr, values)

    @staticmethod
    def getValuesWithAttr(obj, attr):
        from ti.lookup import lookupTypes
        return lookupTypes(obj, attr)

    @staticmethod
    def getValues(objects, attr):
        res = set()
        for obj in objects:
            if not isinstance(obj, classes):
                continue
            newTypes = AttributeTGNode.getValuesWithAttr(obj, attr)
            res |= newTypes
        return res

    def objectsCallback(self, result):
        result |= self.getObjects()

class SubscriptTGNode(TGNode):

    def __init__(self, hasIndex):
        super(SubscriptTGNode, self).__init__()
        self.hasIndex = hasIndex

    def getIndices(self):
       indices = set()
       for node, args in self.getEdges(EdgeType.ASSIGN_INDEX):
           indices |= node.nodeType
       return indices

    def getRights(self):
       rights = set()
       for node, args in self.getEdges(EdgeType.REV_ASSIGN):
           rights |= node.nodeType
       return rights

    def getSlices(self):
       lowers = set()
       for node, args in self.getEdges(EdgeType.ASSIGN_SLICE):
           if args[0] != 0:
               continue
           lowers |= node.nodeType
       uppers = set()
       for node, args in self.getEdges(EdgeType.ASSIGN_SLICE):
           if args[0] != 1:
               continue
           uppers |= node.nodeType
       if len(uppers) == 0:
           uppers.add(None)
       steps = set()
       for node, args in self.getEdges(EdgeType.ASSIGN_SLICE):
           if args[0] != 2:
               continue
           steps |= node.nodeType
       if len(steps) == 0:
           steps.add(None)
       return (lowers, uppers, steps)
           
    def getObjects(self):
       objects = set()
       for node, args in self.getEdges(EdgeType.ASSIGN_OBJECT):
           objects |= node.nodeType
       return objects

    def process(self):
       objects = self.getObjects()
       rights  = self.getRights()
       if self.hasIndex:
           indices = self.getIndices()
       else:
           indices = self.getSlices()
       self.setValues(objects, indices, rights, self.hasIndex)
       self.nodeType = self.getValues(objects, indices, self.hasIndex)

    @staticmethod
    def setValuesWithIndex(obj, slices, values):
        for elem in slices:
            if isinstance(obj, DictSema):
                index = None
            else:
                index = getattr(elem, 'value', None)
            if index is not None:
                obj.addElementsAtIndex(index, values)
            else:
                obj.addElementsAtKey(elem, values)

    @staticmethod
    def setValuesWithoutIndex(obj, values):
        if not isinstance(obj, ListSema):
            return
        for value in values:
            obj.addElements(value.getElements())

    @staticmethod
    def setValues(objects, indices, values, hasIndex):
        for obj in objects:
            if not isinstance(obj, CollectionSema):
                continue
            if hasIndex:
                SubscriptTGNode.setValuesWithIndex(obj, indices, values)
            else:
                SubscriptTGNode.setValuesWithoutIndex(obj, values)

    @staticmethod
    def getValuesWithIndex(obj, slices):
        res = set()
        for elem in slices:
            if isinstance(obj, DictSema):
                index = None
            else:
                index = getattr(elem, 'value', None)
            if index is not None:
                newTypes = obj.getElementsAtIndex(index)
            else:
                newTypes = obj.getElementsAtKey(elem)
            res |= newTypes
        return res

    @staticmethod
    def getValuesWithoutIndex(obj):
        if isinstance(obj, ListSema):
            objCopy = ListSema(0)
            objCopy.addElementsAtKey(None, obj.getElements())
            return {objCopy}
        else:
            return set()
            
    @staticmethod
    def getValues(objects, indices, hasIndex):
        res = set()
        for obj in objects:
            if hasIndex:
                if isinstance(obj, CollectionSema):
                    newTypes = SubscriptTGNode.getValuesWithIndex(obj, indices)
                else:
                    newTypes = set()
            else:
                if isinstance(obj, CollectionSema):
                    newTypes = SubscriptTGNode.getValuesWithoutIndex(obj)
                elif (isinstance(obj, LiteralSema) and
                      obj.ltype in (str, unicode)):
                    newTypes = set()
                    for elem in itertools.product(*indices):
                        try:
                            value = obj.value
                            lower = getattr(elem[0], 'value', None)
                            upper = getattr(elem[1], 'value', None)
                            if upper:
                                step = getattr(elem[2], 'value', None)
                                if step:
                                    strSlice = value[lower:upper:step]
                                else:
                                    strSlice = value[lower:upper]
                            else:
                                strSlice = value[lower:]
                            newTypes.add(LiteralValueSema(strSlice))
                        except:
                            pass
                else:
                    newTypes = set()
            res |= newTypes
        return res

class FunctionDefinitionTGNode(TGNode):

    def __init__(self, name, scope, defaults):
        super(FunctionDefinitionTGNode, self).__init__()

        nodeType = FunctionSema(self, scope)
        self.nodeType  = {nodeType}

        self.name      = name
        self.parent    = scope
        self.templates = {}

        self.params    = ScopeSema()
        self.listParam = None
        self.dictParam = None

        self.defaults  = defaults if defaults else {}

        self.globalDestructive = False

        self.globalNames = set()

    def isListParam(self, param):
        return param and param is self.listParam

    def isDictParam(self, param):
        return param and param is self.dictParam

    @staticmethod
    def sortParams(x, y):
        return cmp(x.number, y.number)

    def getAllParams(self):
        res = self.getOrdinaryParams()
        if self.listParam:
            res.append(self.listParam)
        if self.dictParam:
            res.append(self.dictParam)
        return res

    def getOrdinaryParams(self):
        variables = self.params.variables.values() 
        unsorted = [var for var in variables if var.number]
        return sorted(unsorted, self.sortParams)

    def getListParam(self):
        return self.listParam

    def getDictParam(self):
        return self.dictParam

    def getParams(self):
        return self.params

    def getParent(self):
        return self.parent

    def getDefaults(self):
        return self.defaults

    def getTemplates(self):
        return self.templates

    def hasDefaultReturn(self):
        return False

    def rehashTemplates(self):
        newTemplates = {}
        for key, value in self.templates.items():
            productElement, oldNode = key
            if oldNode:
                newNode = oldNode
            else:
                newNode = value.tgNode
            newKey = productElement, newNode
            newTemplates[newKey] = value
        self.templates = newTemplates

    def isGlobalDestructive(self):
        return self.globalDestructive

    def setGlobalDestructive(self):
        if not self.globalDestructive:
            self.rehashTemplates()
            self.globalDestructive = True 

class UsualFunctionDefinitionTGNode(FunctionDefinitionTGNode):

    def __init__(self, node, name, scope, visitor):
        super(UsualFunctionDefinitionTGNode, self).__init__(name, scope, None)

        if isinstance(node, ast.Lambda):
            self.ast = [node.body]
            self.defaultReturn = False
        else:
            self.ast = node.body
            self.defaultReturn = not self.checkReturns(self.ast)

        if node.args.vararg:
            self.listParam = VariableTGNode(node.args.vararg)

        if node.args.kwarg:
            self.dictParam = VariableTGNode(node.args.kwarg)

        save = config.data.currentScope
        config.data.currentScope = self.getParams()
        visitor.visit_arguments(node.args, self, save)
        config.data.currentScope = save

    def hasDefaultReturn(self):
        return self.defaultReturn

    @staticmethod
    def checkReturns(body):
        for stmt in body:
            if isinstance(stmt, ast.Return):
                return True
            elif isinstance(stmt, ast.If):
                if (UsualFunctionDefinitionTGNode.checkReturns(stmt.body) and
                    UsualFunctionDefinitionTGNode.checkReturns(stmt.orelse)):
                    return True
        return False

class ExternalFunctionDefinitionTGNode(FunctionDefinitionTGNode):

    def __init__(self, num, quasi, name, scope, defaults, listArgs, dictArgs):
        super(ExternalFunctionDefinitionTGNode, self).__init__(name,
                                                               scope,
                                                               defaults)

        self.quasi = quasi

        number = 0
        for index in range(num):
            number = index + 1
            param = VariableTGNode(str(number))
            param.setNumber(number)
            self.params.addVariable(param)

        if listArgs:
            number += 1
            self.listParam = VariableTGNode('args')
            self.listParam.setNumber(number)

        if dictArgs:
            number += 1
            self.dictParam = VariableTGNode('kwargs')
            self.dictParam.setNumber(number)

class ForFunctionDefinitionTGNode(FunctionDefinitionTGNode):

    FUNC_NAME = '#func'
    ITER_NAME = '#iter'

    def __init__(self, node, scope):
        super(ForFunctionDefinitionTGNode, self).__init__(self.FUNC_NAME,
                                                          scope,
                                                          None)

        self.ast    = node.body
        self.target = node.target

        param = VariableTGNode(self.ITER_NAME)
        param.setNumber(1)
        self.params.addVariable(param)

class FunctionCallTGNode(TGNode):

    def __init__(self, node, var = None):
        super(FunctionCallTGNode, self).__init__()
        self.node = node

        self._isLocked = True

        if isinstance(node, ast.BinOp):
            func = var
            args = [node.left, node.right]
        elif isinstance(node, ast.UnaryOp):
            func = var
            args = [node.operand]
        elif isinstance(node, ast.AugAssign):
            func = var
            args = [node.value]
        else:
            func = node.func.link
            args = node.args

        func.addEdge(EdgeType.FUNC, self)
        self.addEdge(EdgeType.REV_FUNC, func)

        index = 0
        for arg in args:
            link = arg.link
            link.addEdge(EdgeType.ARGUMENT, self)
            self.addEdge(EdgeType.REV_ARGUMENT, link, index)
            index += 1
        self.argsNum = index

        if isinstance(node, ast.Call):
            for pair in node.keywords:
                link = pair.value.link
                link.addEdge(EdgeType.KWARGUMENT, self)
                self.addEdge(EdgeType.REV_KWARGUMENT, link, pair.arg)

            if node.starargs:
                link = node.starargs.link
                link.addEdge(EdgeType.LISTARGUMENT, self)
                self.addEdge(EdgeType.REV_LISTARGUMENT, link)

        self._isLocked = False

        self.processCall()

    def getArgumentNodesNumber(self):
        return self.argsNum

    def getArgumentNode(self, index):
        for node, args in self.getEdges(EdgeType.REV_ARGUMENT):
            try:
                if args[0] == index:
                    return node
            except IndexError:
                pass
        return None

    def getFunctionNode(self):
        edges = self.getEdges(EdgeType.REV_FUNC)
        assert len(edges) == 1
        for node, args in edges:
            return node
        return None

    def getKWArgumentNodes(self):
        res = {}
        for node, args in self.getEdges(EdgeType.REV_KWARGUMENT):
            key = args[0]
            res[key] = node
        return res

    def getListArgumentNode(self):
        edges = self.getEdges(EdgeType.REV_LISTARGUMENT)
        assert len(edges) <= 1
        for node, args in edges:
            return node
        return None

    def isLocked(self):
        return self._isLocked

    def process(self):
        pass
 
    def processCall(self):
        from ti.function import processFunc

        if self._isLocked:
            return
        functionNode     = self.getFunctionNode()
        oldArgumentNodes = []
        KWArgumentNodes  = self.getKWArgumentNodes()
        listArgumentNode = self.getListArgumentNode()
        if listArgumentNode:
            listArgumentTypes = []
            for oneType in listArgumentNode.nodeType:
                if isinstance(oneType, TupleSema):
                    listArgumentTypes.append(oneType.elems[1:])
        else:
            listArgumentTypes = [[]]
        for index in range(self.getArgumentNodesNumber()):
            oldArgumentNodes.append(self.getArgumentNode(index))
        for listArgumentType in listArgumentTypes:
            argumentNodes = oldArgumentNodes[:]
            for elem in listArgumentType:
                argumentNodes.append(None)
            processFunc(self, functionNode,
                        argumentNodes, KWArgumentNodes, listArgumentType)

class FunctionTemplateTGNode(TGNode):

    def __init__(self, params, function, inst, tgNode):
        super(FunctionTemplateTGNode, self).__init__()

        if isinstance(function, FunctionDefinitionTGNode):
            self.function = function
            self.parent   = function.getParent()
            self.scope    = TemplateSema(self)

            if not inst and self.function.hasDefaultReturn():
                self.nodeType.add(LiteralSema(types.NoneType))
        else:
            self.function = None
            self.parent   = None
            self.scope    = None

        if inst:
            self.nodeType.add(inst)

        self.params = params
        self.tgNode = tgNode

    def getParams(self):
        return self.params

    def getParent(self):
        return self.parent

    def getScope(self):
        return self.scope

    def process(self):
        pass

class ClassTGNode(TGNode):

    def __init__(self, name, bases, scope, count = False):
        super(ClassTGNode, self).__init__()

        nodeType = ClassSema(self)
        self.nodeType = {nodeType}

        self.name   = name
        self.parent = scope
        self.scope  = nodeType
        self.bases  = bases
        self.body   = ScopeSema()

        self.templates = {}

        self.instancesNumber = 0
        if count:
            self.instances = set()
        else:
            self.instances = None

    def getBases(self):
        return self.bases

    def getBody(self):
        return self.body

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def getScope(self):
        return self.scope

    def getTemplates(self):
        return self.templates

    def addInstance(self, inst):
        try:
            self.instances.add(inst)
        except AttributeError:
            pass
        self.instancesNumber += 1

    def getInstances(self):
        return self.instances

    def getInstancesNumber(self):
        return self.instancesNumber

class ModuleTGNode(TGNode):

    def __init__(self, name, parent, inheritedScope):
        super(ModuleTGNode, self).__init__()
        self.name = name

        self._inherited = inheritedScope is not None
        if self._inherited:
            self.body   = None
            self.scope  = inheritedScope
        else:
            self.body  = ScopeSema()
            self.scope = ModuleSema(self)

        self.parent   = parent
        self.nodeType = {self.scope}

    def getBody(self):
        return self.body

    def getParent(self):
        return self.parent

    def getScope(self):
        return self.scope

    def isInherited(self):
        return self._inherited

class UsualModuleTGNode(ModuleTGNode):

    def __init__(self, ast, name, parentScope, inheritedScope = None):
        super(UsualModuleTGNode, self).__init__(name,
                                                parentScope,
                                                inheritedScope)
        self.ast = ast

    def getAST(self):
        return self.ast

class ExternalModuleTGNode(ModuleTGNode):

    def __init__(self, name, parentScope, asname = None):
        super(ExternalModuleTGNode, self).__init__(name, parentScope, None)
        self.asname = asname if asname else self.name

    def getAliasName(self):
        return self.asname

class BooleanOperationTGNode(TGNode):

    def __init__(self, op):
        super(BooleanOperationTGNode, self).__init__()
        self.isAnd = isinstance(op, ast.And)

    def process(self):
        pass

class UnknownTGNode(TGNode):

    def __init__(self, node):
        super(UnknownTGNode, self).__init__()
        self.nodeType = {NoSema()}
