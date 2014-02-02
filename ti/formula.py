'''
Created on 02.02.2014

@author: bronikkk
'''

import itertools

bool_tuple = (False, True)

class Default(object):

    def __init__(self, types):
        self.types = types

    def getValue(self):
        conds = getConditions(self.types)
        return invertDisjunction(conds)

def calculateAtom(atom, mapping):
    if_node, flag = atom
    return mapping[if_node] == flag

def calculateAll(conj, mapping, defaults):
    if isinstance(conj, Default):
        try:
            value = defaults[conj]
        except KeyError:
            value = conj.getValue()
        return calculateAny(value, mapping, defaults)
    else:
        return all(calculateAtom(atom, mapping) for atom in conj)

def calculateAny(cond, mapping, defaults):
    return any(calculateAll(conj, mapping, defaults) for conj in cond)

def findDefault(value):
    for elem in value:
        if isinstance(elem, Default):
            return elem
    return None

def getConditions(left):
    res = []
    for value in left.values():
        if not findDefault(value):
            res.append(value)
    return res

def getVariablesForConj(conj, defaults):
    if isinstance(conj, Default):
        try:
            value = defaults[conj]
        except KeyError:
            value = conj.getValue()
        return getVariablesForCond(value, defaults)
    res = set()
    for if_node, _ in conj:
        res.add(if_node)
    return res

def getVariablesForCond(cond, defaults):
    res = set()
    for conj in cond:
        res |= getVariablesForConj(conj, defaults)
    return res

def getVariablesForConds(conds, defaults):
    res = set()
    for cond in conds:
        res |= getVariablesForCond(cond, defaults)
    return tuple(res)

def calculateAnd(conds, flag):
    res = set()
    defaults  = {}
    mapping   = {}
    variables = getVariablesForConds(conds, defaults)
    number_of = len(variables)
    for elem_tuple in itertools.product(bool_tuple, repeat=number_of):
        index = 0
        for elem in elem_tuple:
            variable = variables[index]
            mapping[variable] = elem
            index += 1
        value = True
        for cond in conds:
            if not calculateAny(cond, mapping, defaults):
                value = False
                break
        if value != flag:
            continue
        index = 0
        tmp_res = set()
        for elem in elem_tuple:
            variable = variables[index]
            tmp_res.add((variable, elem))
            index += 1
        res.add(tuple(tmp_res))
    return res

def calculateOr(conds, flag):
    res = set()
    defaults  = {}
    mapping   = {}
    variables = getVariablesForConds(conds, defaults)
    number_of = len(variables)
    for elem_tuple in itertools.product(bool_tuple, repeat=number_of):
        index = 0
        for elem in elem_tuple:
            variable = variables[index]
            mapping[variable] = elem
            index += 1
        value = False
        for cond in conds:
            if calculateAny(cond, mapping, defaults):
                value = True
                break
        if value != flag:
            continue
        index = 0
        tmp_res = set()
        for elem in elem_tuple:
            variable = variables[index]
            tmp_res.add((variable, elem))
            index += 1
        res.add(tuple(tmp_res))
    return res

def addCondition(cond, new_cond):
    if len(new_cond) == 0:
        return cond
    else:
        return calculateAnd([cond, new_cond], True)

def addStack(cond, stack):
    if not stack:
        return cond
    else:
        new_cond = {tuple(stack)}
        return calculateAnd([cond, new_cond], True)

def invertDisjunction(conds):
    return calculateOr(conds, False)
