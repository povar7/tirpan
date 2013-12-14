'''
Created on 14.12.2013

@author: bronikkk
'''

import ast

import config
import ti.lookup
import ti.tgnode
import ti.sema
import orak.checkers

from utils import *

class OrakVisitor(ast.NodeVisitor):

    def __init__(self):
        self.visited = set()

    def visit_FunctionDef(self, node):
        pass

    def visit_Lambda(self, node):
        pass

    def visit_common_call(self, node, link):
        btrace = config.data.backTrace
        save   = config.data.currentScope
        for function, isInit in ti.lookup.getFunctions(link):
            if not isinstance(function, ti.sema.FunctionSema):
                continue
            origin = function.origin
            if isinstance(origin, ti.tgnode.ExternalFunctionDefinitionTGNode):
                continue
            if isinstance(origin, ti.tgnode.UsualFunctionDefinitionTGNode):
                usual = True
            else:
                usual = False
            templates = origin.getTemplates()
            for key, template in templates.items():
                if key in self.visited:
                    continue
                else:
                    self.visited.add(key)
                productElement, _ = key
                config.data.currentScope = template.getScope()
                if usual:
                    btrace.addFrame(node, save, function, productElement[0])
                for stmt in origin.ast:
                    self.visit(stmt)
                if usual:
                    btrace.deleteFrame()
                config.data.currentScope = save

    def visit_Call(self, node):
        orak.checkers.checkBasenameCall(node)
        self.generic_visit(node)
        try:
            link = getLink(node.func)
            self.visit_common_call(node, link)
        except AttributeError:
            pass

    def visit_For(self, node):
        self.visit(node.iter)
        try:
            link = getLink(node)
            self.visit_common_call(node, link)
        except AttributeError:
            pass

    def visit_TryExcept(self, node):
        skipBody = False
        skipElse = False
        for handler in node.handlers:
            if (handler.type is None or
                isinstance(handler.type, ast.Name) and
                handler.type.id == 'AttributeError'):
                skipBody = True
            self.visit(handler)
        if not skipBody:
            for stmt in node.body:
                self.visit(stmt)
        if not skipElse:
            for stmt in node.orelse:
                self.visit(stmt)
