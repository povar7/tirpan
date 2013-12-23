'''
Created on 14.12.2013

@author: bronikkk
'''

import ast

import config
import ti.lookup
import ti.tgnode
import ti.sema

import orak.api

from utils import *

def callCheckers(node, func):
    orak.api.invokeCallbacks(node)
    func(node)

def skipTemplate(template, node):
    tgNode = getLink(node) 
    return (tgNode, ()) not in template.edges[ti.tgnode.EdgeType.ASSIGN]

class OrakVisitor(ast.NodeVisitor):

    def __init__(self, mainModule):
        self.modules   = {mainModule}
        self.templates = set()

    def visit_FunctionDef(self, node):
        pass

    def visit_Lambda(self, node):
        pass

    def visit_external_function(self, node, origin):
        parentNode = getLink(node)
        save = config.data.currentScope
        if origin.name == '__import__':
            for elem in parentNode.nodeType:
                if not isinstance(elem, ti.sema.ModuleSema):
                    continue
                self.visit_common_module(elem.origin)
        elif origin.name == 'execfile':
            executedFiles = config.data.importer.executedFiles 
            modules = executedFiles.getModules(parentNode)
            for module in modules:
                self.visit_common_module(module)
        for scope, tgNode, quasiCall in origin.calls:
            if tgNode != parentNode:
                continue
            config.data.currentScope = scope
            quasiLink = getLink(quasiCall.func)
            self.visit_common_call(quasiCall, quasiLink)
            config.data.currentScope = save

    def visit_common_call(self, node, link):
        btrace = config.data.backTrace
        save = config.data.currentScope
        for function, isInit in ti.lookup.getFunctions(link):
            if not isinstance(function, ti.sema.FunctionSema):
                continue
            origin = function.origin
            if isinstance(origin, ti.tgnode.ExternalFunctionDefinitionTGNode):
                self.visit_external_function(node, origin)
                continue
            if isinstance(origin, ti.tgnode.UsualFunctionDefinitionTGNode):
                usual = True
            else:
                usual = False
            templates = origin.getTemplates()
            for key, template in templates.items():
                if template in self.templates or skipTemplate(template, node):
                    continue
                else:
                    self.templates.add(template)
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
        orak.api.invokeCallbacks(node)
        self.generic_visit(node)
        try:
            link = getLink(node.func)
        except AttributeError:
            return
        self.visit_common_call(node, link)

    def visit_For(self, node):
        orak.api.invokeCallbacks(node)
        self.visit(node.iter)
        try:
            link = getLink(node)
        except AttributeError:
            return
        self.visit_common_call(node, link)

    def visit_TryExcept(self, node):
        orak.api.invokeCallbacks(node)
        skipBody = False
        skipElse = False
        for handler in node.handlers:
            if (isinstance(handler.type, ast.Name) and
                handler.type.id == 'AttributeError'):
                skipBody = True
            self.visit(handler)
        if not skipBody:
            for stmt in node.body:
                self.visit(stmt)
        if not skipElse:
            for stmt in node.orelse:
                self.visit(stmt)

    def visit_common_module(self, module):
        if not isinstance(module, ti.tgnode.UsualModuleTGNode):
            return
        elif module in self.modules:
            return
        else:
            self.modules.add(module)
        save = config.data.currentScope
        config.data.currentScope = module.getScope()
        self.visit(module.getAST())
        config.data.currentScope = save

    def visit_Import(self, node):
        orak.api.invokeCallbacks(node)
        for alias in node.names:
            try:
                module = getLink(alias)
            except AttributeError:
                module = None
            self.visit_common_module(module)

    def visit_ImportFrom(self, node):
        orak.api.invokeCallbacks(node)
        try:
            module = getLink(node)
        except AttributeError:
            module = None
        self.visit_common_module(module)

    def __getattr__(self, name):
        func = super(OrakVisitor, self).__getattr__(name)
        return lambda node : callCheckers(node, func)
