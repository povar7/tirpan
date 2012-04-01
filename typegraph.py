'''
Created on 11.12.2011

@author: ramil
'''

from itertools    import product
from ast          import BinOp, UnaryOp, Call
from types        import NoneType

from funccall     import *
from safecopy     import deepcopy
from scope        import Scope
from typenodes    import *
from utils        import *

type_str = TypeStr()

class DependencyType(object):
    Assign     = "assign"
    AssignElem = "assign_elem"
    Elem       = "elem"
    Key        = "key"
    Val        = "val"
    Arg        = "arg"
    KWArg      = "kwarg"
    Func       = "func"

class TypeGraphNode(object):
    def __init__(self):
        self.deps = {}
        self.nodeValue = None
        self.nodeType  = set()

    def get_atom_type_node(self, atom_type):
        if atom_type == int:
            return TypeInt()
        elif atom_type == long:
            return TypeLong()
        elif atom_type == complex:
            return TypeComplex()
        elif atom_type == float:
            return TypeFloat()
        elif atom_type == str:
            return TypeStr()
        elif atom_type == unicode:
            return TypeUnicode()
        elif atom_type == bool:
            return TypeBool()
        elif atom_type == NoneType:
            return TypeNone()
        return None

    def addDependency(self, dep_type, dep):
        if not dep_type in self.deps:
            self.deps[dep_type] = set()     
        self.deps[dep_type].add(dep)
        self.walk_dependency(dep_type, dep)            
    
    def walk_dependency(self, dep_type, dep):
        getattr(self, dep_type + '_dep')(dep)

    def generic_dependency(self):
        for dep_type in self.deps:
            for dep in self.deps[dep_type]:
                self.walk_dependency(dep_type, dep)

    def assign_dep(self, dep):
        if len(self.nodeType - dep.nodeType) != 0:
            dep.nodeType = dep.nodeType.union(self.nodeType)
            dep.generic_dependency()
    
    def assign_elem_dep(self, dep):
        new_types = self.elem_types()
        if len(new_types - dep.nodeType) > 0:
            dep.nodeType = dep.nodeType.union(new_types)
            dep.generic_dependency()
    
    def elem_dep(self, dep):
        res = set()
        while (len(dep.nodeType) > 0):
            tt1 = dep.nodeType.pop()
            for tt2 in self.nodeType:
                tmp = deepcopy(tt1)
                tmp.add_elem(tt2)
                res.add(tmp)
        dep.nodeType = res

    def key_dep(self, dep): 
        res = set()
        while (len(dep.nodeType) > 0):
            tt1 = dep.nodeType.pop()
            for tt2 in self.nodeType:
                tmp = deepcopy(tt1)
                tmp.add_key(tt2)
                res.add(tmp)
        dep.nodeType = res

    def val_dep(self, dep):
        res = set()
        while (len(dep.nodeType) > 0):
            tt1 = dep.nodeType.pop()
            for tt2 in self.nodeType:
                tmp = deepcopy(tt1)
                tmp.add_val(tt2)
                res.add(tmp)
        dep.nodeType = res

    def arg_dep(self, dep):
        index = dep.args.index(self)
        if dep.argsTypes[index] != self.nodeType:
            dep.argsTypes[index] = deepcopy(self.nodeType)
            dep.processCall()
            dep.generic_dependency()

    def kwarg_dep(self, dep):
        index = dep.kwargs.index(self)
        if dep.kwargsTypes[index] != self.nodeType:
            dep.kwargsTypes[index] = deepcopy(self.nodeType)
            dep.processCall()
            dep.generic_dependency()

    def func_dep(self, dep):
        funcs = set([elem for elem in self.nodeType if isinstance(elem, FuncDefTypeGraphNode)])
        if len(funcs) > len(dep.funcs):
            dep.funcs = funcs
            if dep.args is not None:
                dep.processCall()
                dep.generic_dependency()

    def elem_types(self):
        el_types = set()
        for tt in self.nodeType:
            el_types |= tt.elem_types()
        return el_types
   
class ConstTypeGraphNode(TypeGraphNode):
    def __init__(self, value):
        super(ConstTypeGraphNode, self).__init__()
        tp = self.get_atom_type_node(value.__class__)
        self.nodeType  = set([tp])
        self.nodeValue = value    
            
class VarTypeGraphNode(TypeGraphNode):
    def __init__(self, name):
        super(VarTypeGraphNode, self).__init__()
        self.nodeValue    = set()
        self.name         = name
        self.parent       = None
        self.paramNumber  = None
        self.line         = None
        self.col          = None
        self.defaultParam = False
        self.varParam     = False
        self.kwParam      = False
    
    def setParamNumber(self, paramNumber):
        self.paramNumber  = paramNumber
 
    def setDefaultParam(self):
        self.defaultParam = True

    def setVarParam(self):
        self.varParam = True

    def setKWParam(self):
        self.kwParam = True
 
    def setPos(self, node):
        if not self.line:
            self.line = getLine(node)
            self.col  = getCol (node)
                        
class ListTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(ListTypeGraphNode, self).__init__()
        self.nodeType  = set([TypeList()])
        self.nodeValue = None
        for elt in node.elts:
            link = elt.link
            link.addDependency(DependencyType.Elem, self)
    
class TupleTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(TupleTypeGraphNode, self).__init__()
        self.nodeType  = set([TypeTuple()])
        self.nodeValue = None
        for elt in node.elts:
            link = elt.link
            link.addDependency(DependencyType.Elem, self)

class DictTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(DictTypeGraphNode, self).__init__()
        self.nodeType  = set([TypeDict()])
        self.nodeValue = {}
        for i in range(len(node.keys)):
            keyLink   = node.keys[i].link
            valueLink = node.values[i].link
            keyLink  .addDependency(DependencyType.Key, self)
            valueLink.addDependency(DependencyType.Val, self)
            self.nodeValue[keyLink] = valueLink

class ModuleTypeGraphNode(TypeGraphNode):
    def __init__(self, ast, name, parent_scope):
        super(ModuleTypeGraphNode, self).__init__()
        self.nodeType = set([self])
        self.ast      = ast
        self.name     = name
        self.scope    = Scope(parent_scope)

    def getScope(self):
        return self.scope 

class FuncDefTypeGraphNode(TypeGraphNode):
    def __init__(self, parent_scope):
        super(FuncDefTypeGraphNode, self).__init__()
        self.nodeType  = set([self])
        self.params    = Scope(parent_scope, True)
        self.templates = {}

    def getParams(self):
        return self.params 

    def getScope(self):
        return self.scope

    def getKWArgs(self, kwargsTypes):
        return [None]

class UsualFuncDefTypeGraphNode(FuncDefTypeGraphNode):
    def __init__(self, node, parent_scope):
        super(UsualFuncDefTypeGraphNode, self).__init__(parent_scope)
        self.ast       = node.body
        self.vararg    = node.args.vararg
        if self.vararg:
            var = VarTypeGraphNode(self.vararg)
            var.setVarParam()
            self.params.add(var)
        self.kwarg     = node.args.kwarg
        if self.kwarg:
            var = VarTypeGraphNode(self.kwarg)
            var.setKWParam()
            self.params.add(var)

    def getKWArgs(self, kwargsTypes):
        if self.kwarg is None:
            return [None] 
        else:
            res = []
            for item in product(*kwargsTypes):
                type_dict = TypeDict()
                type_dict.add_key(type_str)
                for elem in item:
                    type_dict.add_val(elem) 
                res.append(type_dict)
            return res

class ExternFuncDefTypeGraphNode(FuncDefTypeGraphNode):
    def __init__(self, params_num, quasi, parent_scope, def_vals = {}):
        super(ExternFuncDefTypeGraphNode, self).__init__(parent_scope)
        for i in range(1, params_num + 1):
            param = self.params.addParam(i)
            if i in def_vals:
                def_type = def_vals[i]
                param.setDefaultParam()
                param.nodeType = set([def_type])
        self.quasi = quasi

class FuncCallTypeGraphNode(TypeGraphNode):
    def __init__(self, node, var):
        super(FuncCallTypeGraphNode, self).__init__()
        self.nodeType  = set()
        self.funcs     = set()
        try:
            self.args  = None
            var.addDependency(DependencyType.Func, self)
        except AttributeError:
            import __main__
            from errorprinter import CallNotResolvedError
            __main__.error_printer.printError(CallNotResolvedError(node))
        self.args      = []
        self.argsTypes = []
        if isinstance(node, BinOp):
            nodeArgs = [node.left, node.right]
	elif isinstance(node, UnaryOp):
            nodeArgs = [node.operand]
        elif isinstance(node, Call):
            nodeArgs = node.args
        for arg in nodeArgs:
            link = arg.link
            type_copy = deepcopy(link.nodeType)
            self.args.append(link)
            self.argsTypes.append(type_copy)
            link.addDependency(DependencyType.Arg, self)
        self.kwargs      = []
        self.kwargsTypes = []
        if not isinstance(node, Call):
            return
        for kwarg in node.keywords:
            link = kwarg.value.link
            type_copy = deepcopy(link.nodeType)
            self.kwargs.append(link)
            self.kwargsTypes.append(type_copy)
            link.addDependency(DependencyType.KWArg, self)

    def processCall(self):
        for arg in product(*self.argsTypes):
            for func in self.funcs:
                for kwarg in func.getKWArgs(self.kwargsTypes): 
                    self.nodeType = self.nodeType.union(process_product_elem(func, arg, kwarg))
