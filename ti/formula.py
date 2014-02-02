'''
Created on 02.02.2014

@author: bronikkk
'''

import itertools
import sys

import utils

bool_tuple = (False, True)

class CustomDict(dict):

    def __init__(self):
        self.changed = False

    def hasChanged(self):
        return self.changed

    def resetChanged(self):
        self.changed = False

    def setChanged(self):
        self.changed = True

class Default(object):

    def __init__(self, types):
        self.types = types
        self.value = None

    def getValue(self):
        if self.types.hasChanged():
            conds = getConditions(self.types)
            self.value = invertDisjunction(conds)
            self.types.resetChanged()
        return self.value

def calculateAtom(atom, mapping):
    if_node, flag = atom
    return mapping[if_node] == flag

def calculateAll(conj, mapping):
    if isinstance(conj, Default):
        value = conj.getValue()
        return calculateAny(value, mapping)
    else:
        return all(calculateAtom(atom, mapping) for atom in conj)

def calculateAny(disj, mapping):
    return any(calculateAll(conj, mapping) for conj in disj)

def findDefault(value):
    for elem in value:
        if isinstance(elem, Default):
            return elem
    return None

def getConditions(left):
    result = []
    for value in left.values():
        cond = set()
        for elem in value:
            if not isinstance(elem, Default):
                cond.add(elem)
        result.append(cond)
    return result

def getVariablesForConj(conj):
    if isinstance(conj, Default):
        value = conj.getValue()
        return getVariablesForCond(value)
    else:
        result = set()
        for if_node, _ in conj:
            result.add(if_node)
        return result

def getVariablesForCond(cond):
    result = set()
    for conj in cond:
        result |= getVariablesForConj(conj)
    return result

def getVariablesForConds(conds):
    result = set()
    for cond in conds:
        result |= getVariablesForCond(cond)
    return tuple(result)

def calculateJunction(conds, and_flag, not_flag):
    mapping   = {}
    result    = set()
    variables = getVariablesForConds(conds)
    number_of = len(variables)
    for elem_tuple in itertools.product(bool_tuple, repeat=number_of):
        index = 0
        for elem in elem_tuple:
            variable = variables[index]
            mapping[variable] = elem
            index += 1
        value = True
        if and_flag:
            value = all(calculateAny(cond, mapping) for cond in conds)
        else:
            value = any(calculateAny(cond, mapping) for cond in conds)
        if value != not_flag:
            continue
        index = 0
        tmp = set()
        for elem in elem_tuple:
            variable = variables[index]
            tmp.add((variable, elem))
            index += 1
        result.add(tuple(tmp))
    return result

def addCondition(cond, new_cond):
    if len(new_cond) == 0:
        return cond
    else:
        return calculateJunction([cond, new_cond], True, True)

def addStack(cond, stack):
    if not stack:
        return cond
    else:
        new_cond = {tuple(stack)}
        return calculateJunction([cond, new_cond], True, True)

def getStringFromCondition(conj):
    res = ''
    first = True
    value = sorted(conj, key = sortIfKey)
    for if_node, flag in value:
        filename = utils.getFileName(if_node.node)
        lineno   = utils.getLine    (if_node.node)
        if first:
            first = False
            prefix = ''
        else:
            prefix = ' and '
        added = '%s:%d == %s' % (filename, lineno, flag)
        res += prefix + added
    return res

def invertDisjunction(conds):
    return calculateJunction(conds, False, False)

def _printCondition(cond):
    for elem in cond:
        if not isinstance(elem, Default):
            print >> sys.stderr, '\tCondition: ' + getStringFromCondition(elem)

def printCondition(cond):
    to_print = [cond]
    default  = findDefault(cond)
    if default:
        value = default.getValue()
        to_print.append(value)
    for elem in to_print:
        _printCondition(elem)

def sortIfKey(tup):
    return utils.getLine(tup[0].node)
