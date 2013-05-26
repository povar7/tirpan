'''
Created on 26.05.2013

@author: bronikkk
'''

import ast

def checkEqual(collection):
    try:
        iterator = iter(collection)
        first    = next(iterator)
        return all(first == rest for rest in iterator)
    except StopIteration:
        return True

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

def getColumn(node):
    offset = getattr(node, 'col_offset', None)
    if offset is None:
        return None
    else:
        return offset + 1

def getFileName(node):
    fileNumber = getattr(node, 'fileno', None)
    try:
        name = importer.getFileName(fileNumber)
    except KeyError:
        name = None
    return name

def getFileNumber(node):
    return getattr(node, 'fileno', None)

def findNode(tree, **kwargs):
    line = kwargs['line']
    col  = kwargs['col' ]
    kind = kwargs['kind']
    def callback(node):
        return ((getLine(node) == line  if line else True) and
                (getCol (node) == col   if col  else True) and
                (isinstance(node, kind) if kind else True))
    return findFirstNode(tree, callback)
