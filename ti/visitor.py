'''
Created on 19.01.2014

@author: bronikkk
'''

import ast

import config
import ti.mir
import ti.tgnode
import ti.sema

class QuasiName(object):

    def __init__(self, name):
        self.left = name

class Visitor(ast.NodeVisitor):
    
    def __init__(self, filename, mir_node):
        self.filename = filename
        self.leftpart = False

        self._counter  = 0
        self._mir_node = mir_node

    def add_node(self, new_node):
        self._mir_node.next = new_node
        self._mir_node      = new_node

        try:
            if new_node.left == None:
                self._counter += 1
                new_node.left  = '@temp_' + str(self._counter)
        except AttributeError:
            return

    def visit_common_assign(self, target, value, level = None):
        new_node = None
        save_leftpart = self.leftpart
        self.leftpart = True
        if isinstance(target, ast.Name):
            name = target.id
        else:
            left_node = self.visit(target)
            name = left_node.left
        self.leftpart = save_leftpart
        if level == None:
            if isinstance(target, ast.Name):
                new_node = ti.mir.AssignMirNode(name, value)
            elif isinstance(target, ast.Attribute):
                new_node = ti.mir.AttrLMirNode(name, target.attr, value)
            elif isinstance(target, ast.Subscript):
                slice_node = self.visit(target.slice)
                if slice_node:
                    idx = slice_node.left
                else:
                    idx = None
                new_node = ti.mir.SubtLMirNode(name, idx, value)
        else:
            subt_node = ti.mir.LiteralMirNode(level)
            self.add_node(subt_node)
            temp_node = ti.mir.SubtRMirNode(value, subt_node.left)
            self.add_node(temp_node)
            new_node = ti.mir.AssignMirNode(name, temp_node.left)
        self.add_node(new_node)

    def visit_common_boolop(self, operation, operands):
        assert(len(operands) >= 2)
        args = []
        head_node = self.visit(operands[0])
        args.append(head_node.left)
        if len(operands) > 2:
            tail_node = self.visit_common_boolop(operation, operands[1:])
        else:
            tail_node = self.visit(operands[1])
        args.append(tail_node.left)
        new_node = ti.mir.BoolOpMirNode(operation, args)
        self.add_node(new_node)
        return new_node
    
    def visit_common_literal(self, value):
        new_node = ti.mir.LiteralMirNode(value)
        self.add_node(new_node)
        return new_node

    def visit_Assign(self, node):
        right_node = self.visit(node.value)
        value = right_node.left
        target = node.targets[0]
        if not isinstance(target, ast.Tuple):
            target = node.targets[0]
            self.visit_common_assign(target, value)
        else:
            index = 0
            for elem in target.elts:
                self.visit_common_assign(elem, value, index)
                index += 1

    def visit_Attribute(self, node):
        save_leftpart = self.leftpart
        self.leftpart = False
        left_node = self.visit(node.value)
        self.leftpart = save_leftpart
        if not self.leftpart:
            new_node = ti.mir.AttrRMirNode(left_node.left, node.attr)
            self.add_node(new_node)
            return new_node
        else:
            return left_node

    def visit_BinOp(self, node):
        args = []
        for arg in (node.left, node.right):
            arg_node = self.visit(arg)
            args.append(arg_node.left)
        new_node = ti.mir.BinOpMirNode(node.op, args)
        self.add_node(new_node)
        return new_node

    def visit_BoolOp(self, node):
        return self.visit_common_boolop(node.op, node.values)

    def visit_Call(self, node):
        func_node = self.visit(node.func)
        args = []
        for arg in node.args:
            arg_node = self.visit(arg)
            args.append(arg_node.left)
        pairs = {}
        for pair in node.keywords:
            value_node = self.visit(pair.value)
            pairs[pair.arg] = value_node.left
        if node.starargs:
            star = self.visit(node.starargs).left
        else:
            star = None
        if node.kwargs:
            kw = self.visit(node.kwargs).left
        else:
            kw = None
        new_node = ti.mir.CallMirNode(func_node.left, args, pairs, star, kw)
        self.add_node(new_node)
        return new_node

    def visit_ClassDef(self, node):
        self.add_node(ti.mir.ClassMirNode(node))

    def visit_Dict(self, node):
        elems = {}
        for index in range(len(node.keys)):
            key_node   = self.visit(node.keys  [index])
            value_node = self.visit(node.values[index])
            elems[key_node.left] = value_node.left
        new_node = ti.mir.DictMirNode(elems)
        self.add_node(new_node)
        return new_node

    def visit_FunctionDef(self, node):
        self.add_node(ti.mir.FuncMirNode(node))

    def visit_Global(self, node):
        config.data.currentScope.addGlobalNames(node.names)

    def visit_Import(self, node):
        importer = config.data.importer
        for alias in node.names:
            importer.importFile(self.filename, alias)

    def visit_ImportFrom(self, node):
        importer = config.data.importer
        importer.importFromFile(self.filename, node.module, node.names)

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_List(self, node):
        elems = []
        for elem in node.elts:
            elem_node = self.visit(elem)
            elems.append(elem_node.left)
        new_node = ti.mir.ListMirNode(elems)
        self.add_node(new_node)
        return new_node

    def visit_Name(self, node):
        if not self.leftpart:
            return QuasiName(node.id)
    
    def visit_Num(self, node):
        return self.visit_common_literal(node.n)

    def visit_Print(self, node):
        values = []
        for value in node.values:
            value_node = self.visit(value)
            values.append(value_node.left)
        new_node = ti.mir.PrintMirNode(values)
        self.add_node(new_node)

    def visit_Set(self, node):
        elems = []
        for elem in node.elts:
            elem_node = self.visit(elem)
            elems.append(elem_node.left)
        new_node = ti.mir.SetMirNode(elems)
        self.add_node(new_node)
        return new_node

    def visit_Str(self, node):
        return self.visit_common_literal(node.s)

    def visit_Subscript(self, node):
        save_leftpart = self.leftpart
        self.leftpart = False
        left_node = self.visit(node.value)
        self.leftpart = save_leftpart
        if not self.leftpart:
            slice_node = self.visit(node.slice)
            if slice_node:
                idx = slice_node.left
            else:
                idx = None
            new_node = ti.mir.SubtRMirNode(left_node.left, idx)
            self.add_node(new_node)
            return new_node
        else:
            return left_node

    def visit_Tuple(self, node):
        elems = []
        for elem in node.elts:
            elem_node = self.visit(elem)
            elems.append(elem_node.left)
        new_node = ti.mir.TupleMirNode(elems)
        self.add_node(new_node)
        return new_node

    def visit_UnaryOp(self, node):
        args = []
        for arg in (node.operand,):
            arg_node = self.visit(arg)
            args.append(arg_node.left)
        new_node = ti.mir.UnaryOpMirNode(node.op, args)
        self.add_node(new_node)
        return new_node
