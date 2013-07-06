'''
Created on 06.07.2013

@author: bronikkk
'''

import ast

import utils

def checkSkipNotMain(condition):
    if not isinstance(condition, ast.Compare):
        return False
    left = condition.left
    if (not isinstance(condition.left, ast.Name) or
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
skipElseTemplates = [
                    ]


def checkSkipIf(condition):
    return any(template(condition) for template in skipIfTemplates)

def checkSkipElse(condition):
    return any(template(condition) for template in skipElseTemplates)
