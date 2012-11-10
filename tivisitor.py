'''
Created on 03.01.2012

@author: ramil
'''

import ast

import __main__

from init      import get_operator_name 
from typegraph import *
from utils     import *

class TIVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename  = filename
        self.left_part = False

    def visit_Num(self, node):
        node.link = ConstTypeGraphNode(node.n)
    
    def visit_Str(self, node):
        node.link = ConstTypeGraphNode(node.s, self.filename.endswith('const.py'))
        
    def visit_Name(self, node):
        if node.id == 'None':
            node.link = ConstTypeGraphNode(None)
        else:
            if self.left_part:
                file_scope = __main__.importer.get_ident(node.fileno).scope 
                link       = __main__.current_scope.findOrAdd(node.id, True, file_scope)
            else:
                link       = __main__.current_scope.findOrAdd(node.id)
            node.link = link
            try:
                node.link.setPos(node)
            except AttributeError:
                pass
        
    def visit_Assign(self, node):
        self.visit(node.value)
        target = node.targets[0]
        save   = self.left_part
        self.left_part = True
        if isinstance(target, ast.Tuple):
            for ast_el in target.elts:
                self.visit(ast_el)
            self.left_part = save
            index = 0
            for ast_el in target.elts:
                node.value.link.addDependency(DependencyType.AssignElem, ast_el.link, index)
                index += 1
        else:
            self.visit(target)
            self.left_part = save
            node.value.link.addDependency(DependencyType.Assign, target.link)
        node.link = node.value.link

    def visit_AugAssign(self, node):
        self.visit(node.value)
        target = node.target
        save   = self.left_part
        self.left_part = True
        self.visit(target)
        self.left_part = save
        name = get_operator_name(node.op.__class__)
        var = __main__.current_scope.find(name)
        node.link = FuncCallTypeGraphNode(node, var)
        node.link.processCall()
        node.link.addDependency(DependencyType.Assign, target.link)

    def visit_List(self, node):
        self.generic_visit(node)
        node.link = ListTypeGraphNode(node)
        
    def visit_Dict(self, node):
        self.generic_visit(node)
        node.link = DictTypeGraphNode(node)
    
    def visit_Tuple(self, node):
        self.generic_visit(node)
        node.link = TupleTypeGraphNode(node)

    def visit_Import(self, node):
        __main__.import_files(self.filename, node.names)

    def visit_ImportFrom(self, node):
        __main__.import_from_file(self.filename, node.module, node.names)

    def visit_Module(self, node):
        from typenodes import TypeBool
        type_bool = TypeBool()
        __main__.current_scope = node.link.getScope()
        var_true  = ExternVarTypeGraphNode('True' , type_bool)
        __main__.current_scope.add(var_true)
        var_false = ExternVarTypeGraphNode('False', type_bool)
        __main__.current_scope.add(var_false)
        self.generic_visit(node)
        __main__.current_scope = __main__.current_scope.getParent()

    def visit_arguments(self, node):
        nonDefs = len(node.args) - len(node.defaults)
        for i in range(len(node.args)):
            defPos = i - nonDefs
            defVal = node.defaults[defPos] if defPos >= 0 else None
            if defVal:
                self.visit(defVal)
        for i in range(len(node.args)):
            arg    = node.args[i]
            defPos = i - nonDefs
            defVal = node.defaults[defPos] if defPos >= 0 else None
            save   = __main__.current_scope.parent
            __main__.current_scope.parent = None 
            self.visit(arg)
            __main__.current_scope.parent = save
            arg.link.setParamNumber(i + 1)
            if defVal:
                defVal.link.addDependency(DependencyType.Assign, arg.link)
                arg.link.setDefaultParam()
            
    def visit_FunctionDef(self, node):
        name = node.name
        funcDefNode = UsualFuncDefTypeGraphNode(node, name, __main__.current_scope)
        var  = __main__.current_scope.findOrAdd(name)
        var.setPos(node)
        node.link = funcDefNode
        __main__.current_scope = funcDefNode.getParams()
        self.visit(node.args)
        __main__.current_scope = __main__.current_scope.getParent()
        funcDefNode.addDependency(DependencyType.Assign, var)

    def visit_Call(self, node):
        for arg in node.args:
            self.visit(arg)
        if node.starargs is not None:
            self.visit(node.starargs)
        for kwarg in node.keywords:
            self.visit(kwarg.value)
        
        self.visit(node.func)
        node.link = FuncCallTypeGraphNode(node)
        node.link.processCall()

    def visit_For(self, node):
        self.visit(node.iter)
        target = node.target
        save   = self.left_part
        self.left_part = True
        if isinstance(target, ast.Tuple):
            for ast_el in target.elts:
                self.visit(ast_el)
            self.left_part = save
            index = 0
            for ast_el in target.elts:
                node.iter.link.addDependency(DependencyType.AssignDouble, ast_el.link, index)
                index += 1
        else:
            self.visit(target)
            self.left_part = save
            node.iter.link.addDependency(DependencyType.AssignElem, target.link)
        for nn in node.body:
            self.visit(nn)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        name = get_operator_name(node.op.__class__)
        var = __main__.current_scope.find(name)
        node.link = FuncCallTypeGraphNode(node, var)
        node.link.processCall()

    def visit_UnaryOp(self, node):
        self.visit(node.operand)
        name = get_operator_name(node.op.__class__)
        var = __main__.current_scope.find(name)
        node.link = FuncCallTypeGraphNode(node, var)
        node.link.processCall()
        
    def visit_BoolOp(self, node):
        for value in node.values:
            self.visit(value)
        name = get_operator_name(node.op.__class__)
        var = __main__.current_scope.find(name)
        node.link = FuncCallTypeGraphNode(node, var)
        node.link.processCall()

    def visit_Compare(self, node):
        node.link = ConstTypeGraphNode(False)

    def visit_Return(self, node):
        self.generic_visit(node)
        __main__.current_res.add(node)

    def visit_Yield(self, node):
        self.generic_visit(node)
        __main__.current_res.add(node)

    def visit_Lambda(self, node):
        node.link = UnknownTypeGraphNode(node)

    def visit_Attribute(self, node):
        save = self.left_part
        self.left_part = False
        self.visit(node.value)
        node.link = AttributeTypeGraphNode(node)
        node.link.addDependency(DependencyType.AssignObject, node.value.link)
        node.value.link.addDependency(DependencyType.AttrObject, node.link)
        self.left_part = save

    def visit_Subscript(self, node): 
        self.visit(node.value)
        sub_slice = node.slice
        self.visit(sub_slice) 
        is_index = isinstance(sub_slice, Index)
        if isinstance(sub_slice, Index):
            if isinstance(sub_slice.value, Num):
                index = sub_slice.value.n
            elif isinstance(sub_slice.value, Str):
                index = sub_slice.value.s
            else:
                index = None
        else:
            index = None
        node.link = SubscriptTypeGraphNode(is_index, index)
        node.link.addDependency(DependencyType.AssignObject, node.value.link)
        node.value.link.addDependency(DependencyType.AttrObject, node.link)
        if isinstance(sub_slice, ast.Index):
            sub_slice.value.link.addDependency(DependencyType.AttrSlice, node.link)

    def visit_ListComp(self, node):
        node.link = UnknownTypeGraphNode(node)

    def visit_IfExp(self, node):
        node.link = UnknownTypeGraphNode(node)

    def visit_If(self, node):
        fileno    = getFileNumber(node)
        skip_if   = False
        skip_else = False
        test      = node.test
        if fileno != 0:
            if isinstance(test, ast.Compare):
                if isinstance(test.left, ast.Name) and \
                   test.left.id  == '__name__' and \
                   len(test.ops) == 1 and \
                   isinstance(test.ops[0], ast.Eq) and \
                   len(test.comparators) == 1 and \
                   isinstance(test.comparators[0], ast.Str) and \
                   test.comparators[0].s == '__main__':
                    skip_if = True
        if isinstance(test, ast.Call):
            if isinstance(test.func, ast.Name) and \
               test.func.id == 'hasattr' and \
               len(test.args) == 2 and \
               isinstance(test.args[0], ast.Name) and \
               test.args[0].id == 'sys' and \
               isinstance(test.args[1], ast.Str) and \
               test.args[1].s == 'frozen':
                skip_if = True
            if isinstance(test.func, ast.Attribute) and \
               isinstance(test.func.value, ast.Name) and \
               test.func.value.id == 'argpars' and \
               test.func.attr == 'need_gui':
                skip_else = True
        elif isinstance(test, ast.Compare):
            if isinstance(test.left, ast.Str) and \
               isinstance(test.left.s, str) and \
               len(test.ops) == 1 and \
               isinstance(test.ops[0], ast.In) and \
               len(test.comparators) == 1 and \
               isinstance(test.comparators[0], ast.Name):
                save = self.left_part
                self.left_part = False
                self.visit(test.comparators[0])
                nodeType = test.comparators[0].link.nodeType
                if len(nodeType) == 1:
                    type1 = list(nodeType)[0]
                    if isinstance(type1, TypeTuple):
                        tmp_str  = TypeStr(test.left.s)
                        if tmp_str in type1.elem_types():
                            skip_else = True
                self.left_part = save 
        if not skip_if:
            for stmt in node.body:
                self.visit(stmt)
        if not skip_else:
            for stmt in node.orelse:
                self.visit(stmt)

    def visit_GeneratorExp(self, node):
        node.link = UnknownTypeGraphNode(node)

    def visit_Global(self, node):
        __main__.current_scope.addGlobalNames(node.names)

    def visit_ClassDef(self, node):
        for base in node.bases:
            self.visit(base)
        classDefNode = UsualClassDefTypeGraphNode(node, __main__.current_scope)
        var  = __main__.current_scope.findOrAdd(node.name)
        var.setPos(node)
        node.link = classDefNode
        __main__.current_scope = classDefNode.getScope()
        for stmt in node.body:
            self.visit(stmt)
        __main__.current_scope = __main__.current_scope.getParent()
        classDefNode.addDependency(DependencyType.Assign, var)

    def visit_Print(self, node):
        for value in node.values:
             self.visit(value)
        node.link = PrintTypeGraphNode()

    def visit_Index(self, node):
        self.generic_visit(node)

    def visit_Slice(self, node):
        self.generic_visit(node)

    def visit_Set(self, node):
        node.link = UnknownTypeGraphNode(node)

