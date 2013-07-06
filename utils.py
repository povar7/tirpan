'''
Created on 26.05.2013

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
    line = kwargs.get('line')
    col  = kwargs.get('col' )
    kind = kwargs.get('kind')
    def callback(node):
        return ((getLine  (node) == line if line is not None else True) and
                (getColumn(node) == col  if col  is not None else True) and
                (isinstance(node, kind)  if kind is not None else True))
    return findFirstNode(tree, callback)
