'''
Created on 06.07.2013

@author: bronikkk
'''

import ast

import config
import ti.tgnode
import ti.sema
import utils

def addSubvariable(var, edgeType, flag):
    scope  = ti.sema.ScopeSema(config.data.currentScope)
    newVar = ti.tgnode.VariableTGNode(var.name)
    scope.addVariable(newVar)
    var.addEdge(edgeType, newVar, flag)
    newVar.addEdge(ti.tgnode.EdgeType.ASSIGN, var)
    config.data.currentScope = scope

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

skipIfTemplates   = [
                        checkSkipNotMain,
                        checkSkipSysFrozen,
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
    nodeType = comp.link.nodeType
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
    return arg.link

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

def checkFilteringCondition(condition):
    return isinstance(condition, (ast.Name, ast.BoolOp))
