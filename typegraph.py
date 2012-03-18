'''
Created on 11.12.2011

@author: ramil
'''

from copy import deepcopy
from itertools import product

from funccall import *
from scope import Scope
from typenodes import *

class DependencyType(object):
    Assign     = "assign"
    AssignElem = "assign_elem"
    Elem       = "elem"
    Key        = "key"
    Val        = "val"
    Arg        = "arg"
    Module     = "module"

class TypeGraphNode(object):
    def __init__(self):
        self.deps = {}
        self.nodeValue = None
        self.nodeType  = set()

    def get_atom_type_node(self, atom_type):
        if atom_type == int:
            return TypeInt()
        elif atom_type == float:
            return TypeFloat()
        elif atom_type == str:
            return TypeStr()
        elif atom_type == unicode:
            return TypeUnicode()
        elif atom_type == bool:
            return TypeBool()
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
    
    def addValue(self, value):
        self.nodeValue = self.nodeValue.union(set([value]))
 
    def setParamNumber(self, paramNumber):
        self.paramNumber = paramNumber
                        
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
        self.nodeType = None
        self.ast      = ast
        self.name     = name
        self.scope    = Scope(parent_scope)

    def getScope(self):
        return self.scope 
    
    def module_dep(self, dep):
        pass

class FuncDefTypeGraphNode(TypeGraphNode):
    def __init__(self, ast, parent_scope):
        super(FuncDefTypeGraphNode, self).__init__()
        self.nodeType  = set()
        self.ast       = ast
        self.params    = Scope(parent_scope)
        self.templates = {}

    def getParams(self):
        return self.params 

    def getScope(self):
        return self.scope 

class FuncCallTypeGraphNode(TypeGraphNode):
    def __init__(self, node, funcs):
        super(FuncCallTypeGraphNode, self).__init__()
        self.nodeType  = set()
        self.args      = []
        self.argsTypes = []
        self.funcs     = funcs
        for arg in node.args:
            link = arg.link
            type_copy = deepcopy(link.nodeType)
            self.args.append(link)
            self.argsTypes.append(type_copy)
            link.addDependency(DependencyType.Arg, self)

    def processCall(self):
        for elem in product(*self.argsTypes):
            for func in self.funcs:
               self.nodeType = self.nodeType.union(process_product_elem(func, elem))
