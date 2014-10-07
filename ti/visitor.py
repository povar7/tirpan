'''
Created on 19.01.2014

@author: bronikkk
'''

import ast

import config
import ti.mir

class Visitor(ast.NodeVisitor):
    
    def __init__(self, filename, mir_node):
        self.filename = filename
        self.leftpart = False

        self._counter  = 0
        self._mir_node = mir_node

    def add_node(self, new_node):
        self._mir_node.next = new_node
        new_node.prev = self._mir_node

        self._mir_node = new_node

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
            name = self.visit(target)
        self.leftpart = save_leftpart
        if level == None:
            if isinstance(target, ast.Name):
                new_node = ti.mir.AssignMirNode(name, value)
            elif isinstance(target, ast.Attribute):
                new_node = ti.mir.AttrLMirNode(name, target.attr, value)
            elif isinstance(target, ast.Subscript):
                idx = self.visit(target.slice)
                new_node = ti.mir.SubtLMirNode(name, idx, value)
        else:
            subt_node = ti.mir.LiteralMirNode(level)
            self.add_node(subt_node)
            temp_node = ti.mir.SubtRMirNode(value, subt_node.left)
            self.add_node(temp_node)
            new_node = ti.mir.AssignMirNode(name, temp_node.left)
        self.add_node(new_node)
        try:
            return new_node.left
        except AttributeError:
            return

    def visit_common_boolop(self, is_and, operands, true_goto, false_goto):
        # TODO implement non-branching use case
        assert(len(operands) >= 2)
        new_node = ti.mir.BeginMirNode()
        if len(operands) > 2:
            self.visit_common_boolop(is_and, operands[:-1],
                                     new_node   if is_and else true_goto,
                                     false_goto if is_and else  new_node)
        else:
            operands[0]. true_goto = new_node   if is_and else true_goto
            operands[0].false_goto = false_goto if is_and else  new_node
            head_value = self.visit(operands[0])
            if head_value:  # Then condition was not a boolean operator
                if_node = ti.mir.IfMirNode(operands[0], head_value,
                                           operands[0]. true_goto,
                                           operands[0].false_goto)
                self.add_node(if_node)

        self._mir_node = new_node
        operands[-1]. true_goto =  true_goto
        operands[-1].false_goto = false_goto
        tail_value = self.visit(operands[-1])
        if tail_value:  # Then condition was not a boolean operator
            if_node = ti.mir.IfMirNode(operands[-1], tail_value,
                                       true_goto, false_goto)
            self.add_node(if_node)

    def visit_common_literal(self, value):
        new_node = ti.mir.LiteralMirNode(value)
        self.add_node(new_node)
        return new_node.left

    def visit_Assign(self, node):
        value = self.visit(node.value)
        target = node.targets[0]
        if not isinstance(target, ast.Tuple):
            return self.visit_common_assign(target, value)
        else:
            index = 0
            for elem in target.elts:
                self.visit_common_assign(elem, value, index)
                index += 1

    def visit_Attribute(self, node):
        save_leftpart = self.leftpart
        self.leftpart = False
        left = self.visit(node.value)
        self.leftpart = save_leftpart
        if not self.leftpart:
            new_node = ti.mir.AttrRMirNode(left, node.attr)
            self.add_node(new_node)
            return new_node.left
        else:
            return left

    def visit_BinOp(self, node):
        args = [self.visit(arg) for arg in (node.left, node.right)]
        new_node = ti.mir.BinOpMirNode(node.op, args)
        self.add_node(new_node)
        return new_node.left

    def visit_BoolOp(self, node):
        return self.visit_common_boolop(isinstance(node.op, ast.And),
                                        node.values,
                                        getattr(node,  'true_goto', None),
                                        getattr(node, 'false_goto', None))

    def visit_Call(self, node):
        func = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        pairs = {pair.arg: self.visit(pair.value)
                 for pair in node.keywords}
        if node.starargs:
            star = self.visit(node.starargs)
        else:
            star = None
        if node.kwargs:
            kw = self.visit(node.kwargs)
        else:
            kw = None
        new_node = ti.mir.CallMirNode(func, args, pairs, star, kw)
        self.add_node(new_node)
        return new_node.left

    def visit_ClassDef(self, node):
        new_node = ti.mir.ClassMirNode(node)
        self.add_node(new_node)
        visitor = Visitor(self.filename, new_node.mir)
        for stmt in node.body:
            visitor.visit(stmt)

    def visit_Compare(self, node):
        return self.visit_common_literal(True)

    def visit_Dict(self, node):
        elems = {self.visit(node.keys  [index]): self.visit(node.values[index])
                 for index in range(len(node.keys))}
        new_node = ti.mir.DictMirNode(elems)
        self.add_node(new_node)
        return new_node.left

    def visit_FunctionDef(self, node):
        self.add_node(ti.mir.FuncMirNode(node))

    def visit_Global(self, node):
        config.data.currentScope.addGlobalNames(node.names)

    def visit_If(self, node):
        new_join = ti.mir.JoinMirNode()
        node.test.true_goto =\
            ti.mir.BeginMirNode() if node.body   else new_join
        node.test.false_goto =\
            ti.mir.BeginMirNode() if node.orelse else new_join
        cond_value = self.visit(node.test)
        if cond_value:  # Then condition was not a boolean operator
            new_node = ti.mir.IfMirNode(node.test, cond_value,
                                        node.test.true_goto,
                                        node.test.false_goto)
            self.add_node(new_node)
        if node.body:
            self._mir_node = node.test.true_goto
            for stmt in node.body:
                self.visit(stmt)
            self.add_node(new_join)
        if node.orelse:
            self._mir_node = node.test.false_goto
            for stmt in node.orelse:
                self.visit(stmt)
            self.add_node(new_join)
        self._mir_node = new_join
        del node.test.true_goto, node.test.false_goto  # Cleanup

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
        elems = [self.visit(elem) for elem in node.elts]
        new_node = ti.mir.ListMirNode(elems)
        self.add_node(new_node)
        return new_node.left

    def visit_Name(self, node):
        if node.id == 'None':
            return self.visit_common_literal(None)
        elif node.id == 'True':
            return self.visit_common_literal(True)
        elif node.id == 'False':
            return self.visit_common_literal(False)
        if not self.leftpart:
            return node.id
    
    def visit_Num(self, node):
        return self.visit_common_literal(node.n)

    def visit_Print(self, node):
        values = [self.visit(value) for value in node.values]
        new_node = ti.mir.PrintMirNode(values)
        self.add_node(new_node)

    def visit_Set(self, node):
        elems = [self.visit(elem) for elem in node.elts]
        new_node = ti.mir.SetMirNode(elems)
        self.add_node(new_node)
        return new_node.left

    def visit_Str(self, node):
        return self.visit_common_literal(node.s)

    def visit_Subscript(self, node):
        save_leftpart = self.leftpart
        self.leftpart = False
        left = self.visit(node.value)
        self.leftpart = save_leftpart
        if not self.leftpart:
            idx = self.visit(node.slice)
            new_node = ti.mir.SubtRMirNode(left, idx)
            self.add_node(new_node)
            return new_node.left
        else:
            return left

    def visit_Tuple(self, node):
        elems = [self.visit(elem) for elem in node.elts]
        new_node = ti.mir.TupleMirNode(elems)
        self.add_node(new_node)
        return new_node.left

    def visit_UnaryOp(self, node):
        args = [self.visit(arg) for arg in (node.operand,)]
        new_node = ti.mir.UnaryOpMirNode(node.op, args)
        self.add_node(new_node)
        return new_node.left
