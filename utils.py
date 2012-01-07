'''
Created on 07.01.2012

@author: bronikkk
'''

import ast

def findFirstNode(tree, callback):
    for node in ast.walk(tree):
        if callback(node):
            return node
    return None

def findAllNodes(tree, callback):
    for node in ast.walk(tree):
        if callback(node):
            yield node
    yield None

def getLine(node):
    return getattr(node, 'lineno', None)

def getCol (node):
    offset = getattr(node, 'col_offset', None)
    return offset + 1 if offset else None

def findNode(tree, **kwargs):
    try:
        line = kwargs['line']
    except KeyError:
        line = None
    try:
        col = kwargs['col']
    except KeyError:
        col = None
    try:
        kind = kwargs['kind']
    except KeyError:
        kind = None
    callback = lambda(node) : \
               (getLine(node) == line  if line else True) and \
               (getCol (node) == col   if col  else True) and \
               (isinstance(node, kind) if kind else True)
    return findFirstNode(tree, callback)
