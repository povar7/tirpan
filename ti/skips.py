'''
Created on 06.07.2013

@author: bronikkk
'''

import ast

import config
import ti.tgnode
import ti.sema
import utils

def addSubvariable(var, edgeType, flag, filtered = None):
    if not var:
        return
    scope  = ti.sema.ScopeSema(config.data.currentScope, False)
    newVar = ti.tgnode.VariableTGNode(var.name)
    scope.addVariable(newVar)
    var.addEdge(edgeType, newVar, flag)
    newVar.addEdge(ti.tgnode.EdgeType.ASSIGN, var)
    config.data.currentScope = scope
    if flag:
        try:
            filtered[var] = edgeType
        except TypeError:
            pass

def checkSkipNotMain(condition):
    if not isinstance(condition, ast.Compare):
        return False
    left = condition.left
    if (not isinstance(left, ast.Name) or
        left.id != '__name__'):
        return False
    ops = condition.ops
    if len(ops) != 1:
        return False
    op = ops[0]
    if not isinstance(op, ast.Eq):
        return False
    comps = condition.comparators
    if len(comps) != 1:
        return False
    comp = comps[0]
    if not isinstance(comp, ast.Str):
        return False
    if comp.s != '__main__':
        return False
    return utils.getFileNumber(condition) != 0

def checkSkipSysFrozen(condition):
    if not isinstance(condition, ast.Call):
        return False
    func = condition.func
    if (not isinstance(condition.func, ast.Name) or
        func.id != 'hasattr'):
        return False
    args = condition.args
    if len(args) != 2:
        return False
    obj = args[0]
    if (not isinstance(obj, ast.Name) or
        obj.id != 'sys'):
        return False
    attr = args[1]
    if (not isinstance(attr, ast.Str) or
        attr.s != 'frozen'):
        return False 
    return True

def checkSkipNonEqualNumbers(condition):
    if not isinstance(condition, ast.Compare):
        return False
    left = condition.left

    ops = condition.ops
    if len(ops) != 1:
        return False
    op = ops[0]
    if not isinstance(op, ast.Eq):
        return False
    comps = condition.comparators
    if len(comps) != 1:
        return False
    comp = comps[0]
    if not isinstance(comp, ast.Num):
        return False
    num = comp.n

    def callback(x, value):
        return isinstance(x, ti.sema.LiteralValueSema) and x.value != value

    nodeType = utils.getLink(left).nodeType
    return any(callback(elem, num) for elem in nodeType)

def checkSkipHasKey(condition):
    if not isinstance(condition, ast.Call):
        return False
    func = condition.func
    if not isinstance(func, ast.Attribute):
        return False
    value = func.value

    attr = func.attr
    if attr != 'has_key':
        return False
    args = condition.args
    if len(args) != 1:
        return False
    arg = args[0]
    if not isinstance(arg, ast.Str):
        return False
    nodeType = utils.getLink(value).nodeType
    if len(nodeType) != 1:
        return False
    theDict = list(nodeType)[0]
    dictKey = ti.sema.LiteralValueSema(arg.s) 
    return not theDict.elems.has_key(dictKey)

def checkSkipWrongArch(condition):
    if not isinstance(condition, ast.Compare):
        return False
    left = condition.left
    leftType = utils.getLink(left).nodeType
    if len(leftType) != 1:
        return False
    type1 = list(leftType)[0]
    if not isinstance(type1, ti.sema.LiteralValueSema):
        return False
    ops = condition.ops
    if len(ops) != 1:
        return False
    op = ops[0]
    if not isinstance(op, ast.In):
        return False
    comps = condition.comparators
    if len(comps) != 1:
        return False
    comp = comps[0]
    rightType = utils.getLink(comp).nodeType
    if len(rightType) != 1:
        return False
    type2 = list(rightType)[0]
    if not isinstance(type2, ti.sema.ListSema):
        return False
    for elem in type2.getElements():
        if not isinstance(elem, ti.sema.LiteralValueSema):
            return False
        if type1 == elem:
            return False
    return True

def checkSkipFalseFunction(condition):
    if not isinstance(condition, ast.Call):
        return False
    nodeType = utils.getLink(condition).nodeType
    if len(nodeType) != 1:
        return False
    type1 = list(nodeType)[0]
    return isinstance(type1, ti.sema.LiteralValueSema) and not type1.value
                
skipIfTemplates   = [
                        checkSkipNotMain,
                        checkSkipSysFrozen,
                        checkSkipNonEqualNumbers,
                        checkSkipHasKey,
                        checkSkipWrongArch,
                        checkSkipFalseFunction,
                    ]


def checkSkipNotPosix(condition):
    if not isinstance(condition, ast.Compare):
        return False
    left = condition.left
    if not isinstance(left, ast.Str):
        return False
    ops = condition.ops
    if len(ops) != 1:
        return False
    op = ops[0]
    if not isinstance(op, ast.In):
        return False
    comps = condition.comparators
    if len(comps) != 1:
        return False
    comp = comps[0]
    if not isinstance(comp, ast.Name):
        return False
    nodeType = utils.getLink(comp).nodeType
    if len(nodeType) != 1:
        return False
    type1 = list(nodeType)[0]
    if not isinstance(type1, ti.sema.TupleSema):
        return False
    tmp = ti.sema.LiteralValueSema(left.s)
    for elem in type1.elems:
        if tmp in elem:
            return True
    return False

skipElseTemplates = [
                        checkSkipNotPosix,
                    ]


def checkSkipIf(condition):
    return any(template(condition) for template in skipIfTemplates)

def checkSkipElse(condition):
    return any(template(condition) for template in skipElseTemplates)


def checkSkipNotIterable(stmt):
    if not isinstance(stmt, ast.Expr):
        return None
    value = stmt.value
    if not isinstance(value, ast.Call):
        return None
    func = value.func
    if (not isinstance(func, ast.Name) or
        func.id != 'iter'):
        return None
    args = value.args
    if len(args) != 1:
        return None
    arg = args[0]
    if not isinstance(arg, ast.Name):
        return None
    return utils.getLink(arg)

def checkHandlerType(handler):
    if not handler.type:
        return True
    htype = handler.type
    if not isinstance(htype, ast.Name):
        return False
    return htype.id == 'TypeError'

def checkComprehension(ifs, target):
    if not isinstance(target, ast.Name):
        return None
    if len(ifs) != 1:
        return None
    first = ifs[0]
    if not isinstance(first, ast.Compare):
        return None
    comparators = first.comparators
    if len(comparators) != 1:
        return None
    left = first.left
    if not isinstance(left, ast.Attribute):
        return None
    value = left.value
    if (not isinstance(value, ast.Name) or
        value.id != target.id):
        return None
    ops = first.ops
    if len(ops) != 1:
        return None
    op = ops[0]
    if not isinstance(op, ast.Eq):
        return None
    return first


def checkFilteringIsInstance(expr):
    if not isinstance(expr, ast.Call):
        return False
    func = expr.func
    if (not isinstance(expr.func, ast.Name) or
        func.id != 'isinstance'):
        return False
    args = expr.args
    if len(args) != 2:
        return False
    obj = args[0]
    if not isinstance(obj, ast.Name):
        return False
    cls = args[1]
    if (not isinstance(cls, ast.Name) or
        cls.id != 'list'):
        return False
    return True

def checkFilteringName(expr):
    return isinstance(expr, ast.Name)

def checkFilteringOperand(expr):
    return checkFilteringName(expr) or checkFilteringIsInstance(expr)

def checkFilteringCondition(expr):
    return isinstance(expr, ast.BoolOp) or checkFilteringOperand(expr)

def checkSkipAfterIf(condition):
    if not isinstance(condition, ast.UnaryOp):
        return False
    operand = condition.operand
    if not isinstance(operand, ast.Compare):
        return False
    comparators = operand.comparators
    if len(comparators) != 1:
        return False
    ops = operand.ops
    if len(ops) != 1:
        return False
    op = ops[0]
    if not isinstance(op, ast.Eq):
        return False
    type1 = utils.getLink(operand.left).nodeType
    if len(type1) != 1:
        return False
    elem1 = list(type1)[0]
    type2 = utils.getLink(comparators[0]).nodeType
    if len(type2) != 1:
        return False
    elem2 = list(type2)[0]
    try:
        return elem1.value != elem2.value
    except:
        return False

def checkGlobalDestructive(flags, node):
    if not flags.isDestructive():
        return False

    try:
        link = utils.getLink(node.func.value)
        objects = link.commonRetrieve('objects',
                                      ti.tgnode.EdgeType.isNotReverseAssign)
    except AttributeError:
        objects = set()

    def callback(elem):
        return isinstance(elem, ti.sema.InstanceSema) and elem.isSingleton()

    return any(callback(elem) for elem in objects)
