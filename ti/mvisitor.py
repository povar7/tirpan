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
    
    def visit(self, node, ifstack):
        try:
            state = ifstack[-1]
        except IndexError:
            state = None
        getattr(self, 'visit_' + node.__class__.__name__)(node, state)

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

    def visit_AssignMirNode(self, node, state):
        scope = config.data.currentScope
        l_var = scope.findOrAddName(node.left, True, None)
        r_var = scope.findOrAddName(node.right)
        ti.tgnode.replaceTypes(l_var, r_var.nodeType, state)

    def visit_AttrLMirNode(self, node, state):
        scope = config.data.currentScope
        o_var = scope.findName(node.obj)
        r_var = scope.findName(node.right)
        ti.lookup.setTypes(o_var.nodeType, node.attr, r_var.nodeType, state)

    def visit_AttrRMirNode(self, node, state):
        scope = config.data.currentScope
        l_var = scope.findOrAddName(node.left, True, None)
        o_var = scope.findOrAddName(node.obj)
        types = ti.lookup.getTypes(o_var.nodeType, node.attr)
        ti.tgnode.replaceTypes(l_var, types, state)

    def visit_BeginMirNode(self, node, state):
        pass

    def visit_BinOpMirNode(self, node, state):
        pass

    def visit_BoolOpMirNode(self, node, state):
        pass

    def visit_CallMirNode(self, node, state):
        scope = config.data.currentScope
        l_var = scope.findOrAddName(node.left, True, None)
        types = node.process()
        ti.tgnode.replaceTypes(l_var, types, state)

    def visit_ClassMirNode(self, node, state):
        import ti.mir
        name  = node.name
        scope = config.data.currentScope
        sema  = ti.sema.ClassSema(node.name, scope)
        var   = scope.findOrAddName(name, True, None)
        var.nodeType = {sema}
        config.data.currentScope = sema
        ti.mir.walkChain(node.mir, self.file_scope)
        config.data.currentScope = scope

    def visit_DictMirNode(self, node, state):
        pass

    def visit_FuncMirNode(self, node, state):
        name  = node.func.name
        scope = config.data.currentScope
        func  = ti.tgnode.UsualFunctionDefinitionTGNode(node.func, name, scope)
        var   = self.visit_common_left_part(name)
        ti.tgnode.replaceTypes(var, func.nodeType, state)
        config.data.currentScope = func.getParams()
        self.visit_common_arguments(node.func.args, node.func)
        config.data.currentScope = scope

    def visit_ListMirNode(self, node, state):
        pass

    def visit_LiteralMirNode(self, node, state):
        scope = config.data.currentScope
        l_var = scope.findOrAddName(node.left, True, None)
        if node.value == None:
            sema = ti.sema.LiteralSema(types.NoneType)
        else:
            sema = ti.sema.LiteralValueSema(node.value)
        ti.tgnode.replaceTypes(l_var, {sema}, state)

    def visit_PrintMirNode(self, node, state):
        pass

    def visit_SetMirNode(self, node, state):
        pass

    def visit_SubtLMirNode(self, node, state):
        pass

    def visit_SubtRMirNode(self, node, state):
        pass

    def visit_TupleMirNode(self, node, state):
        pass

    def visit_UnaryOpMirNode(self, node, state):
        pass
