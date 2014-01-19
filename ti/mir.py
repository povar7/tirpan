'''
Created on 19.01.2014

@author: bronikkk
'''

import ti.lookup

def printChain(node):
    while True:
        try:
            if not isinstance(node, EmptyMirNode):
                print node.getString()
            node = node.next
        except:
            return

class MirNode(object):

    def __init__(self):
        pass

class SerialMirNode(object):

    def __init__(self):
        super(SerialMirNode, self).__init__()
        self.next = None

    def getString(self):
        return ''

class AssignMirNode(SerialMirNode):

    def __init__(self, left, right):
        super(AssignMirNode, self).__init__()
        self.left  = left
        self.right = right

    def getString(self):
        return self.left + ' = ' + self.right

class AttrLMirNode(SerialMirNode):

    def __init__(self, obj, attr, right):
        super(AttrLMirNode, self).__init__()
        self.obj   = obj
        self.attr  = attr
        self.right = right

    def getString(self):
        return self.obj + '.' + self.attr + ' = ' + self.right

class AttrRMirNode(SerialMirNode):

    def __init__(self, obj, attr):
        super(AttrRMirNode, self).__init__()
        self.left = None
        self.obj  = obj
        self.attr = attr

    def getString(self):
        return self.left + ' = ' + self.obj + '.' + self.attr

class BinOpMirNode(SerialMirNode):

    def __init__(self, func, args):
        super(BinOpMirNode, self).__init__()
        self.left = None
        self.func = func
        self.args = args

    def getString(self):
        l_op = self.args[0]
        r_op = self.args[1]
        name = ti.lookup.getOperatorName(self.func)
        res  = self.left + ' = ' + l_op + ' ' + name + ' ' + r_op
        return res

class BoolOpMirNode(SerialMirNode):

    def __init__(self, func, args):
        super(BoolOpMirNode, self).__init__()
        self.left = None
        self.func = func
        self.args = args

    def getString(self):
        name  = ti.lookup.getOperatorName(self.func)
        res   = self.left + ' = '
        first = True
        for arg in self.args:
            added = arg
            if first:
                first  = False
                prefix = ''
            else:
                prefix = ' ' + name + ' '
            res += prefix + added
        return res

class CallMirNode(SerialMirNode):

    def __init__(self, func, args, pairs, star, kw):
        super(CallMirNode, self).__init__()
        self.left  = None
        self.func  = func
        self.args  = args
        self.pairs = pairs
        self.star  = star
        self.kw    = kw

    def getString(self):
        res = self.left + ' = ' + self.func + '('
        first = True
        for arg in self.args:
            added = arg
            if first:
                first  = False
                prefix = ''
            else:
                prefix = ', '
            res += prefix + added
        for key, value in self.pairs.items():
            added = key + ' = ' + value
            if first:
                first  = False
                prefix = ''
            else:
                prefix = ', '
            res += prefix + added
        if self.star:
            added = '*' + self.star
            if first:
                first  = False
                prefix = ''
            else:
                prefix = ', '
            res += prefix + added
        if self.kw:
            added = '**' + self.kw
            if first:
                first  = False
                prefix = ''
            else:
                prefix = ', '
            res += prefix + added
        res += ')'
        return res

class ClassMirNode(SerialMirNode):

    def __init__(self, node):
        super(ClassMirNode, self).__init__()
        self.child = EmptyMirNode()
        self.node  = node

    def getString(self):
        return 'class ' + self.node.name

class DictMirNode(SerialMirNode):

    def __init__(self, elems):
        super(DictMirNode, self).__init__()
        self.left  = None
        self.elems = elems

    def getString(self):
        res = self.left + ' = {'
        first = True
        for key, value in self.elems.items():
            added = key + ': ' + value
            if first:
                first  = False
                prefix = ''
            else:
                prefix = ', '
            res += prefix + added  
        res += '}'
        return res

class EmptyMirNode(SerialMirNode):
    
    def __init__(self):
        super(EmptyMirNode, self).__init__()

class FuncMirNode(SerialMirNode):

    def __init__(self, node):
        super(FuncMirNode, self).__init__()
        self.child = EmptyMirNode()
        self.node  = node

    def getString(self):
        return 'def ' + self.node.name

class ListMirNode(SerialMirNode):

    def __init__(self, elems):
        super(ListMirNode, self).__init__()
        self.left  = None
        self.elems = elems

    def getString(self):
        res = self.left + ' = ['
        first = True
        for elem in self.elems:
            added = elem
            if first:
                first  = False
                prefix = ''
            else:
                prefix = ', '
            res += prefix + added
        res += ']'
        return res

class LiteralMirNode(SerialMirNode):
   
    def __init__(self, value):
        super(LiteralMirNode, self).__init__()
        self.left  = None
        self.value = value

    def getString(self):
        return self.left + ' = ' + self.value.__repr__()

class PrintMirNode(SerialMirNode):

    def __init__(self, values):
        super(PrintMirNode, self).__init__()
        self.values = values

    def getString(self):
        res = 'print'
        first = True
        for value in self.values:
            added = value
            if first:
                first  = False
                prefix = ' '
            else:
                prefix = ', '
            res += prefix + added
        return res

class SetMirNode(SerialMirNode):

    def __init__(self, elems):
        super(SetMirNode, self).__init__()
        self.left  = None
        self.elems = elems

    def getString(self):
        res = self.left + ' = {'
        first = True
        for elem in self.elems:
            added = elem
            if first:
                first  = False
                prefix = ''
            else:
                prefix = ', '
            res += prefix + added
        res += '}'
        return res

class SubtLMirNode(SerialMirNode):

    def __init__(self, obj, idx, right):
        super(SubtLMirNode, self).__init__()
        self.obj   = obj
        self.idx   = idx
        self.right = right

    def getString(self):
        if self.idx:
            idx_str = self.idx
        else:
            idx_str = '...'
        return self.obj + '[' + idx_str + '] = ' + self.right

class SubtRMirNode(SerialMirNode):

    def __init__(self, obj, idx):
        super(SubtRMirNode, self).__init__()
        self.left = None
        self.obj  = obj
        self.idx  = idx

    def getString(self):
        if self.idx:
            idx_str = self.idx
        else:
            idx_str = '...'
        return self.left + ' = ' + self.obj + '[' + idx_str + ']'

class TupleMirNode(SerialMirNode):

    def __init__(self, elems):
        super(TupleMirNode, self).__init__()
        self.left  = None
        self.elems = elems

    def getString(self):
        res = self.left + ' = ('
        first = True
        for elem in self.elems:
            added = elem
            if first:
                first  = False
                prefix = ''
            else:
                prefix = ', '
            res += prefix + added
        if len(self.elems) != 1:
            res += ')'
        else:
            res += ',)'
        return res

class UnaryOpMirNode(SerialMirNode):

    def __init__(self, func, args):
        super(UnaryOpMirNode, self).__init__()
        self.left = None
        self.func = func
        self.args = args

    def getString(self):
        oper = self.args[0]
        name = ti.lookup.getOperatorName(self.func)
        res  = self.left + ' = ' + name + oper
        return res
