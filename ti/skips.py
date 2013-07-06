'''
Created on 06.07.2013

@author: bronikkk
'''

import ast

import ti.sema
import utils

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

skipIfTemplates   = [
                        checkSkipNotMain,
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
