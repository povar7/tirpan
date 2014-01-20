'''
Created on 20.01.2014

@author: bronikkk
'''

class MirVisitor(object):
    
    def __init__(self):
        pass

    def visit(self, node):
        getattr(self, 'visit_' + node.__class__.__name__)(node)

    def visit_AssignMirNode(self, node):
        pass

    def visit_AttrLMirNode(self, node):
        pass

    def visit_AttrRMirNode(self, node):
        pass

    def visit_BeginMirNode(self, node):
        pass

    def visit_BinOpMirNode(self, node):
        pass

    def visit_BoolOpMirNode(self, node):
        pass

    def visit_CallMirNode(self, node):
        pass

    def visit_ClassMirNode(self, node):
        pass

    def visit_DictMirNode(self, node):
        pass

    def visit_FuncMirNode(self, node):
        pass

    def visit_ListMirNode(self, node):
        pass

    def visit_LiteralMirNode(self, node):
        pass

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
