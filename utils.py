'''
Created on 26.05.2013

@author: bronikkk
'''

import ast
import types

class QuasiAlias(object):

    def __init__(self, name):
        self.name    = name
        self.asname  = None

class QuasiNode(object):

    def __init__(self, link):
        pass

class QuasiCall(object):

    def __init__(self, func, args, node = None):
        self.func = func
        self.args = args
        if hasattr(node, 'fileno'):
            self.fileno = node.fileno
        if hasattr(node, 'lineno'):
            self.lineno = node.lineno

class QuasiFunction(object):

    def __init__(self, name):
        self.name = name
        self.parent = None

    def getString(self):
        return self.name

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
    import config
    importer = config.data.importer
    fileNumber = getFileNumber(node)
    try:
        name = importer.getIdent(fileNumber).name
    except AttributeError:
        name = None
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

def sortParams(x, y):
    return cmp(x.number, y.number)

def getNodeType(elem):
    if elem.nodeType:
        return elem.nodeType
    else:
        return {None}

def makeSet(elem):
    if elem is not None:
        return {elem}
    else:
        return set()

def quasi_cons(params, **kwargs):
    obj = params[0]
    return {obj}

def quasi_none(params, **kwargs):
    from ti.sema import getNoneSema
    return {getNoneSema()}

def quasi_zero(params, **kwargs):
    return set()

def quasi_zero_var():
    return set()
