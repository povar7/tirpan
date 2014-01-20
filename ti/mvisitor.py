'''
Created on 20.01.2014

@author: bronikkk
'''

import config
import types

import ti.lookup
import ti.tgnode
import ti.sema

class MirVisitor(object):

    def __init__(self, file_scope):
        self.file_scope = file_scope
    
    def visit(self, node):
        getattr(self, 'visit_' + node.__class__.__name__)(node)

    def visit_common_left_part(self, name):
        scope = config.data.currentScope
        return scope.findOrAddName(name, True, self.file_scope)

    def visit_common_arguments(self, node, func):
        scope   = config.data.currentScope
        nonDefs = len(node.args) - len(node.defaults)
        index = 0
        for param in node.args:
            var = scope.addName(param.id)
            defPos = index - nonDefs
            defVal = node.defaults[defPos] if defPos >= 0 else None
            if defVal:
                func.defaults[var.name] = None
            index += 1
            var.setNumber(index)

    def visit_AssignMirNode(self, node):
        scope = config.data.currentScope
        l_var = scope.findOrAddName(node.left, True, None)
        r_var = scope.findOrAddName(node.right)
        ti.tgnode.replaceSet(l_var.nodeType, r_var.nodeType)

    def visit_AttrLMirNode(self, node):
        scope = config.data.currentScope
        o_var = scope.findName(node.obj)
        r_var = scope.findName(node.right)
        ti.lookup.setTypes(o_var.nodeType, node.attr, r_var.nodeType)

    def visit_AttrRMirNode(self, node):
        scope = config.data.currentScope
        l_var = scope.findOrAddName(node.left, True, None)
        o_var = scope.findOrAddName(node.obj)
        types = ti.lookup.getTypes(o_var.nodeType, node.attr)
        ti.tgnode.replaceSet(l_var.nodeType, types)

    def visit_BeginMirNode(self, node):
        pass

    def visit_BinOpMirNode(self, node):
        pass

    def visit_BoolOpMirNode(self, node):
        pass

    def visit_CallMirNode(self, node):
        scope = config.data.currentScope
        l_var = scope.findOrAddName(node.left, True, None)
        types = node.process()
        ti.tgnode.replaceSet(l_var.nodeType, types)

    def visit_ClassMirNode(self, node):
        import ti.mir
        name  = node.name
        scope = config.data.currentScope
        sema  = ti.sema.ClassSema(node.name, scope)
        var   = scope.findOrAddName(name, True, None)
        var.nodeType = {sema}
        config.data.currentScope = sema
        ti.mir.walkChain(node.mir, self.file_scope)
        config.data.currentScope = scope

    def visit_DictMirNode(self, node):
        pass

    def visit_FuncMirNode(self, node):
        name  = node.func.name
        scope = config.data.currentScope
        func  = ti.tgnode.UsualFunctionDefinitionTGNode(node.func, name, scope)
        var   = self.visit_common_left_part(name)
        ti.tgnode.replaceSet(var.nodeType, func.nodeType)
        config.data.currentScope = func.getParams()
        self.visit_common_arguments(node.func.args, node.func)
        config.data.currentScope = scope

    def visit_ListMirNode(self, node):
        pass

    def visit_LiteralMirNode(self, node):
        scope = config.data.currentScope
        l_var = scope.findOrAddName(node.left, True, None)
        if node.value == None:
            sema = ti.sema.LiteralSema(types.NoneType)
        else:
            sema = ti.sema.LiteralValueSema(node.value)
        ti.tgnode.replaceSet(l_var.nodeType, {sema})

    def visit_PrintMirNode(self, node):
        pass

    def visit_SetMirNode(self, node):
        pass

    def visit_SubtLMirNode(self, node):
        pass

    def visit_SubtRMirNode(self, node):
        pass

    def visit_TupleMirNode(self, node):
        pass

    def visit_UnaryOpMirNode(self, node):
        pass
