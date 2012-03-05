'''
Created on 11.12.2011

@author: ramil
'''

from scope import Scope
from binops import *
from typenodes import *
import copy

class DependencyType(object):
    Assign = "assign"
    AssignElem = "assign_elem"
    Elem = "elem"
    Key = "key"
    Module = "module"
    BinOpLElem = "binop_lelem"
    BinOpRElem = "binop_relem"


class TypeGraphNode(object):
    def __init__(self):
        self.deps = {}
        self.rdeps = {}
        self.nodeValue = None
        self.nodeType  = set()

    def get_atom_type_node(self, str):
        if str == 'int':
            return TypeInt()
        elif str == 'float':
            return TypeFloat()
        elif str == 'str':
            return TypeStr()
        elif str == 'unicode':
            return TypeUnicode()
        elif str == 'bool':
            return TypeBool()
        else:
            print str
            exit(1)


    def addDependency(self, dep_type, dep):
        if not dep_type in self.deps:
            self.deps[dep_type] = set()     
        if not dep_type in dep.rdeps:
            dep.rdeps[dep_type] = set()
        self.deps[dep_type].add(dep)
        dep.rdeps[dep_type].add(self)
        self.walk_dependency(dep_type, dep)            
    
    def walk_dependency(self, dep_type, dep):
        getattr(self, dep_type + '_dep')(dep)

    def generic_dependency(self):
        for dep_type in self.deps:
            for dep in self.deps[dep_type]:
                dep.walk_dependency(dep_type, self)

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
        while(len(dep.nodeType) > 0):
            tt1 = dep.nodeType.pop()
            for tt2 in self.nodeType:
                tmp = copy.deepcopy(tt1)
                tmp.add_elem(tt2)
                res.add(tmp)
        dep.nodeType = res

    def key_dep(self, dep): 
        res = set()
        while(len(dep.nodeType) > 0):
            tt1 = dep.nodeType.pop()
            for tt2 in self.nodeType:
                tmp = copy.deepcopy(tt1)
                tmp.add_key(tt2)
                res.add(tmp)
        dep.nodeType = res

    def elem_types(self):
        el_types = set()
        for tt in self.nodeType:
            el_types |= tt.elem_types()
        return el_types
    
    def binop_lelem_dep(self, dep): dep.binop_dep()
    
    def binop_relem_dep(self, dep): dep.binop_dep()
    
class ConstTypeGraphNode(TypeGraphNode):
    def __init__(self, value):
        super(ConstTypeGraphNode, self).__init__()
        tp = self.get_atom_type_node(value.__class__.__name__)
        self.nodeType  = set([tp])
        self.nodeValue = value    
            
class VarTypeGraphNode(TypeGraphNode):
    def __init__(self, name):
        super(VarTypeGraphNode, self).__init__()
        self.nodeValue = set()
        self.name      = name
        self.parent    = None
    
    def addValue(self, value):
        self.nodeValue = self.nodeValue.union(set([value]))
                        

class BinOpTypeGraphNode(TypeGraphNode):
    binop = BinOps()
    def __init__(self, op):
        super(BinOpTypeGraphNode, self).__init__()
        self.op = op
    
    def operants_exist(self):
        return DependencyType.BinOpLElem in self.rdeps and DependencyType.BinOpRElem in self.rdeps
    
    def binop_dep(self):
        if self.operants_exist():
            op1 = list(self.rdeps[DependencyType.BinOpLElem])[0]
            op2 = list(self.rdeps[DependencyType.BinOpRElem])[0]
            getattr(self.binop, self.op)(self, op1, op2) 
            self.generic_dependency()

class ListTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(ListTypeGraphNode, self).__init__()
        self.nodeType  = set([TypeList()])
        self.nodeValue = None
        for elt in node.elts:
            link = elt.link
            link.addDependency(DependencyType.Elem, self)
            
        
    
class TupleTypeGraphNode(ListTypeGraphNode):
    pass;


class DictTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(DictTypeGraphNode, self).__init__()
        self.nodeType  = set([TypeDict()])
        self.nodeValue = {}
        for i in range(len(node.keys)):
            keyLink   = node.keys[i].link
            valueLink = node.values[i].link
            keyLink.addDependency(DependencyType.Key, self)
            valueLink.addDependency(DependencyType.Elem, self)
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
        self.nodeType  = None
        self.ast       = ast
        self.scope     = None
        self.params    = Scope(parent_scope)
        self.templates = []
    def getParams(self):
        return self.params 
    def getScope(self):
        return self.scope 

class CallTypeGraphNode(TypeGraphNode):
    def __init__(self):
        super(CallTypeGraphNode, self).__init__()
        self.nodeType = None
