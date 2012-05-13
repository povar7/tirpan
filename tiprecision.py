'''
Created on 03.01.2012

@author: ramil
'''

import ast

import __main__

from tistat    import HitsCounter
from typegraph import *
from typenodes import TypeUnknown

def check_types(node, counter):
    try:
        types = node.link.nodeType
        cond  = len(types) > 0 and \
                not any([isinstance(elem, TypeUnknown) for elem in types])
        counter.check_condition(cond , None)
    except AttributeError:
        counter.check_condition(False, None)

class TIPrecision(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.counter  = HitsCounter()

    def getCounter(self):
        return self.counter

    def visit_Name(self, node):
        self.generic_visit(node)
        check_types(node, self.counter)

    def visit_Call(self, node):
        self.generic_visit(node)
        check_types(node, self.counter)

    def visit_FunctionDef(self, node):
        try:
            types = node.link.nodeType
            funcs = set([elem for elem in types if isinstance(elem, FuncDefTypeGraphNode)])
            for func in funcs:
                if not isinstance(func, UsualFuncDefTypeGraphNode):
                    continue
                template_values = func.templates.values()
                if len(template_values) > 0:
                    stmts = template_values[0].ast
                else:
                    continue
                for stmt in stmts:
                    self.visit(stmt)
        except AttributeError:
            self.counter.check_condition(False, None)   

    def visit_BinOp(self, node):
        self.generic_visit(node)
        check_types(node, self.counter)

    def visit_UnaryOp(self, node):
        self.generic_visit(node)
        check_types(node, self.counter)

    def visit_BoolOp(self, node):
        self.generic_visit(node)
        check_types(node, self.counter)

    def visit_List(self, node):
        self.generic_visit(node)
        check_types(node, self.counter)
        
    def visit_Dict(self, node):
        self.generic_visit(node)
        check_types(node, self.counter)
    
    def visit_Tuple(self, node):
        self.generic_visit(node)
        check_types(node, self.counter)
