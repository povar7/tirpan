'''
Created on 11.12.2011

@author: ramil
'''

from itertools    import product
from ast          import AugAssign, BinOp, UnaryOp, Call, Index, Num, Str
from copy         import deepcopy
from types        import NoneType

from classes      import copy_class_inst, find_inits_in_classes
from classes      import get_attributes, set_attributes
from classes      import get_subscripts, set_subscripts
from classes      import set_slices
from funccall     import *
from returns      import check_returns
from scope        import Scope
from typenodes    import *
from utils        import *

type_bool    = TypeBool()
type_str     = TypeStr()
type_unknown = TypeUnknown()

def smart_union(set1, set2):
    import __main__
    for elem in set2:
        if len(set1) >= __main__.types_number:
	    set1.discard(type_unknown)
            return set1
        try:
            set1.add(elem)
        except RuntimeError:
            pass
    if len(set1) > 1:
        set1.discard(type_unknown)
    return set1

def smart_deepcopy_union(set1, set2):
    import __main__
    if len(set1) >= __main__.types_number:
        return set1
    set2_copy = deepcopy(set2)
    for elem in set2_copy:
        if len(set1) >= __main__.types_number:
            set1.discard(type_unknown)
            return set1
        try:
            set1.add(elem)
        except RuntimeError:
            pass
    if len(set1) > 1:
        set1.discard(type_unknown)
    return set1

def smart_len(a_set):
    if type_unknown in a_set:
        return len(a_set) - 1
    else:
        return len(a_set)

class DependencyType(object):
    Assign       = 'assign'
    AssignElem   = 'assign_elem'
    Elem         = 'elem'
    Key          = 'key'
    Val          = 'val'
    Arg          = 'arg'
    AttrArg      = 'attrarg'
    KWArg        = 'kwarg'
    Func         = 'func'
    Base         = 'base'
    AttrObject   = 'attrobject'
    AssignObject = 'assignobject'
    AttrSlice    = 'attrslice'

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

    def addDependency(self, dep_type, dep, *args):
        if not dep_type in self.deps:
            self.deps[dep_type] = set()
        self.deps[dep_type].add((dep, args))
        self.walk_dependency(dep_type, dep, *args)

    def removeDependency(self, dep_type, dep):
        self.deps[dep_type].discard((dep, ()))
    
    def walk_dependency(self, dep_type, dep, *args):
        getattr(self, dep_type + '_dep')(dep, *args)

    def generic_dependency(self):
        for dep_type in self.deps:
            for dep, args in tuple(self.deps[dep_type]):
                self.walk_dependency(dep_type, dep, *args)

    def assign_dep(self, dep):
        try:
            if (self, ()) in dep.deps[DependencyType.Arg]:
                dep.removeDependency(DependencyType.Arg, self)
        except KeyError:
            pass
        if isinstance(dep, VarTypeGraphNode):
            try:
                if len(self.nodeType - dep.nodeType) > 0:
                    old_len = smart_len(dep.nodeType)
                    dep.nodeType = smart_union(dep.nodeType, self.nodeType)
                    if smart_len(dep.nodeType) > old_len:
                        dep.generic_dependency()
            except RuntimeError:
                pass
        elif isinstance(dep, (AttributeTypeGraphNode, SubscriptTypeGraphNode)):
            try:
                if len(self.nodeType - dep.values) > 0:
                    dep.values = smart_union(dep.values, self.nodeType)
                    dep.process()
                    dep.generic_dependency()
            except RuntimeError:
                pass
    
    def assign_elem_dep(self, dep, *args):
        try:
            index = args[0]
            new_types = self.elem_types_index(index)
        except IndexError:
            new_types = self.elem_types()
        if len(new_types - dep.nodeType) > 0:
            dep.nodeType = smart_union(dep.nodeType, new_types)
            dep.generic_dependency()
    
    def elem_dep(self, dep, *args):
        import __main__
        res = set()
        try:
            index = args[0]
        except IndexError:
            index = None 
        while len(dep.nodeType) > 0:
            tt1 = dep.nodeType.pop()
            if len(tt1.elems) >= __main__.types_number:
                continue 
            for tt2 in self.nodeType:
                if len(res) >= __main__.types_number:
                    break
                tmp = deepcopy(tt1)
                if index is None or not isinstance(tmp.elems, tuple):
                    tmp.add_elem(tt2)
                else:
                    elems_list = list(tmp.elems)
                    elems_list[index] = tt2
                    tmp.elems  = tuple(elems_list)
                res.add(tmp)
        dep.nodeType = res
        try:
            if (self, ()) in dep.deps[DependencyType.Assign]:
                dep.removeDependency(DependencyType.Assign, self)
        except KeyError:
            pass
        dep.generic_dependency()

    def key_dep(self, dep):
        import __main__
        res = set()
        while len(dep.nodeType) > 0:
            tt1 = dep.nodeType.pop()
            if len(tt1.keys) >= __main__.types_number:
                continue 
            for tt2 in self.nodeType:
                if len(res) >= __main__.types_number:
                    break
                tmp = deepcopy(tt1)
                tmp.add_key(tt2)
                res.add(tmp)
        dep.nodeType = res
        dep.generic_dependency()

    def val_dep(self, dep):
        import __main__
        res = set()
        while len(dep.nodeType) > 0:
            tt1 = dep.nodeType.pop()
            if len(tt1.vals) >= __main__.types_number:
                continue 
            for tt2 in self.nodeType:
                if len(res) >= __main__.types_number:
                    break
                tmp = deepcopy(tt1)
                tmp.add_val(tt2)
                res.add(tmp)
        dep.nodeType = res
        dep.generic_dependency()

    def arg_dep(self, dep):
        try:
            index  = dep.args.index(self)
            is_arg = True
        except ValueError:
            is_arg = False 
        nodeType = self.nodeType
        if is_arg:
            old_type = dep.argsTypes[index]
        else:
            old_type = dep.starargsTypes
        try:
            if old_type != nodeType:
                type_copy = deepcopy(nodeType)
                if is_arg:
                    dep.argsTypes[index] = type_copy
                else:
                    dep.starargsTypes    = type_copy
                dep.processCall()
                dep.generic_dependency()
        except RuntimeError:
            pass

    def attrarg_dep(self, dep):
        try:
            index  = dep.args.index(self)
            is_arg = True
        except ValueError:
            is_arg = False
        nodeType = self.objects
        if is_arg:
            old_type = dep.argsTypes[index]
        else:
            old_type = dep.starargsTypes
        if old_type != nodeType:
            type_copy = deepcopy(nodeType)
            if is_arg:
                dep.argsTypes[index] = type_copy
            else:
                dep.starargsTypes    = type_copy
            dep.processCall()
            dep.generic_dependency()

    def kwarg_dep(self, dep):
        try:
            index = dep.kwargsKeys[self]
        except KeyError:
            return
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
        classes = set([elem for elem in self.nodeType if isinstance(elem, ClassDefTypeGraphNode)])
        if len(classes) > len(dep.classes):
            dep.classes = classes
            if dep.args is not None:
                dep.processCall()
                dep.generic_dependency()

    def base_dep(self, dep):
        pass

    def attrobject_dep(self, dep):
        try:
            if len(self.nodeType - dep.objects) > 0:
                old_len = smart_len(dep.objects)
                dep.objects = smart_union(dep.objects, self.nodeType)
                if smart_len(dep.objects) > old_len:
                    dep.process()
                    dep.generic_dependency()
        except RuntimeError:
            pass

    def assignobject_dep(self, dep):
        try:
            if len(self.objects - dep.nodeType) > 0:
                old_len = smart_len(dep.nodeType)
                dep.nodeType = smart_deepcopy_union(dep.nodeType, self.objects)
                if isinstance(dep, (AttributeTypeGraphNode, SubscriptTypeGraphNode)): 
                    if len(dep.nodeType - dep.values) > 0:
                        dep.values = smart_union(dep.values, dep.nodeType)
                        dep.process()
                if smart_len(dep.nodeType) > old_len: 
                    dep.generic_dependency()
        except RuntimeError:
            pass

    def object_dep(self, dep):
        if isinstance(dep, FuncCallTypeGraphNode):
            if len(self.nodeType - dep.nodeType) > 0:
                dep.nodeType = smart_union(dep.nodeType, self.nodeType)
                dep.generic_dependency()

    def attrslice_dep(self, dep):
        keys_types = dep.getKeysTypes()
        if any([len(self.nodeType - key_type) > 0 for key_type in keys_types]):
            if dep.processSlice(self.nodeType):
                dep.generic_dependency()

    def elem_types(self):
        el_types = set()
        for tt in self.nodeType:
            el_types |= tt.elem_types()
        return el_types

    def elem_types_index(self, index):
        el_types = set()
        for tt in self.nodeType:
            if isinstance(tt, TypeTuple) and isinstance(tt.elems, tuple):
                try:
                    el_types.add(tt.elems[index])
                    continue
                except IndexError:
                    pass
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

    def setParent(self, parent):
        self.parent       = parent

class UsualVarTypeGraphNode(VarTypeGraphNode):
    def __init__(self, name):
        super(UsualVarTypeGraphNode, self).__init__(name)
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
            self.fno  = getFileNumber(node)

    def addBool(self):
        self.nodeType.add(type_bool)
        self.generic_dependency()

class ExternVarTypeGraphNode(VarTypeGraphNode):
    def __init__(self, name, var_type):
        super(ExternVarTypeGraphNode, self).__init__(name)
        self.nodeType = set([var_type])
                        
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
        tuple_type       = TypeTuple()
        tuple_type.elems = (None,) * len(node.elts)
        self.nodeType    = set([tuple_type])
        self.nodeValue   = None
        index = 0
        for elt in node.elts:
            link = elt.link
            link.addDependency(DependencyType.Elem, self, index)
            index += 1

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
    def __init__(self, name, parent_scope):
        super(ModuleTypeGraphNode, self).__init__()
        self.nodeType = set([self])
        self.name     = name
        self.scope    = Scope(parent_scope)

    def __deepcopy__(self, memo):
        return self

    def getScope(self):
        return self.scope

    def elem_types(self):
        return set()

class UsualModuleTypeGraphNode(ModuleTypeGraphNode):
    def __init__(self, ast, name, parent_scope):
        super(UsualModuleTypeGraphNode, self).__init__(name, parent_scope)
        self.ast      = ast

class ExternModuleTypeGraphNode(ModuleTypeGraphNode):
    def __init__(self, name, parent_scope):
        super(ExternModuleTypeGraphNode, self).__init__(name, parent_scope)
        self.isLoaded = False

class FuncDefTypeGraphNode(TypeGraphNode):
    def __init__(self, name, parent_scope):
        super(FuncDefTypeGraphNode, self).__init__()
        try:
            init_flag  = parent_scope.isClassScope() and \
                         name == '__init__'
        except AttributeError:
            init_flag  = False
        if init_flag:
            scope_flag = Scope.init_scope
        else:
            scope_flag = Scope.func_scope
        self.nodeType  = set([self])
        self.name      = name
        self.params    = Scope(parent_scope, scope_flag)
        self.scope     = Scope()
        self.templates = {}

    def __deepcopy__(self, memo):
        return self

    def getParams(self):
        return self.params 

    def getScope(self):
        return self.scope

    def getKWArgs(self, kwargs):
        return [None]

    def elem_types(self):
        return set()

class UsualFuncDefTypeGraphNode(FuncDefTypeGraphNode):
    def __init__(self, node, name, parent_scope):
        super(UsualFuncDefTypeGraphNode, self).__init__(name, parent_scope)
        self.ast       = node.body
        self.vararg    = node.args.vararg
        if self.vararg:
            var = UsualVarTypeGraphNode(self.vararg)
            var.setVarParam()
            self.params.add(var)
        self.kwarg     = node.args.kwarg
        if self.kwarg:
            var = UsualVarTypeGraphNode(self.kwarg)
            var.setKWParam()
            self.params.add(var)
        self.defReturn = not check_returns(self.ast)

    def getKWArgs(self, kwargs):
        if self.kwarg is None:
            return [None] 
        else:
            res = []
            tmp = []
            for item in kwargs.items():
                sub_list = []
                for sub_item in product((item[0],), deepcopy(item[1].nodeType)):
                    sub_list.append(sub_item)
                tmp.append(sub_list)
            for item in product(*tmp):
                res.append(dict(item))
            return res

class ExternFuncDefTypeGraphNode(FuncDefTypeGraphNode):
    def __init__(self, params_num, quasi, name, parent_scope, def_vals = {}):
        super(ExternFuncDefTypeGraphNode, self).__init__(name, parent_scope)
        for i in range(1, params_num + 1):
            param = self.params.addParam(i)
            if i in def_vals:
                def_type = def_vals[i]
                param.setDefaultParam()
                param.nodeType = set([def_type])
        self.quasi = quasi

class FuncCallTypeGraphNode(TypeGraphNode):
    def __init__(self, node, var = None):
        super(FuncCallTypeGraphNode, self).__init__()
        self.nodeType  = set()
        self.funcs     = set()
        self.classes   = set()
        self.line      = getLine(node)
        self.col       = getCol(node)
        self.fno       = getFileNumber(node)
        if var is None:
            var = node.func.link
        try:
            self.args  = None
            var.addDependency(DependencyType.Func, self)
        except AttributeError:
            import __main__
            from errorprinter import CallNotResolvedError
            __main__.error_printer.printError(CallNotResolvedError(node))
        self.args      = []
        self.argsTypes = []
        self.starargs      = None
        self.starargsTypes = None
        if isinstance(var, AttributeTypeGraphNode):
            nodeArgs = [node.func]
            self.attrCall = True
        else:
            nodeArgs = []
            self.attrCall = False
        if isinstance(node, AugAssign):
            nodeArgs += [node.target, node.value]
        elif isinstance(node, BinOp):
            nodeArgs += [node.left, node.right]
        elif isinstance(node, UnaryOp):
            nodeArgs += [node.operand]
        elif isinstance(node, Call):
            nodeArgs += node.args
        for arg in nodeArgs:
            link = arg.link
            if link is var and isinstance(link, AttributeTypeGraphNode):
                nodeType = link.objects
                dep      = DependencyType.AttrArg
            else:
                nodeType = link.nodeType
                dep      = DependencyType.Arg
            try:
                type_copy = deepcopy(nodeType)
            except RuntimeError:
                type_copy = nodeType
            self.args.append(link)
            self.argsTypes.append(type_copy)
            link.addDependency(dep, self)
        try:
            stararg = node.starargs
        except AttributeError:
            stararg = None
        if stararg is not None:
            link = stararg.link
            if link is var and isinstance(link, AttributeTypeGraphNode):
                nodeType = link.objects
                dep      = DependencyType.AttrArg
            else:
                nodeType = link.nodeType
                dep      = DependencyType.Arg
            type_copy = deepcopy(nodeType)
            self.starargs      = link
            self.starargsTypes = type_copy
            link.addDependency(dep, self)
        self.kwargs      = {}
        self.kwargsKeys  = {}
        self.kwargsTypes = []
        if not isinstance(node, Call):
            return
        kwarg_index = 0
        for kwarg in node.keywords:
            link = kwarg.value.link
            type_copy = deepcopy(link.nodeType)
            self.kwargs[kwarg.arg] = link
            self.kwargsKeys[link] = kwarg_index
            self.kwargsTypes.append(type_copy)
            link.addDependency(DependencyType.KWArg, self)
            kwarg_index += 1

    def processCall(self):
        funcs = [(None, func) for func in self.funcs]
        inits = find_inits_in_classes(self.classes)
        callables  = []
        callables += funcs
        callables += inits
        starargs   = []
        if self.starargsTypes is not None:
            for star_type in self.starargsTypes:
                if isinstance(star_type, TypeTuple) and \
                   isinstance(star_type.elems, tuple):
                    starargs.append(star_type.elems)
        if len(starargs) == 0:
            starargs.append(())
        for args_type_orig in product(*self.argsTypes):
            for elem in callables:
                if hasattr(self, 'kwargsTypes'):
                    _, func = elem
                    if self.attrCall and isinstance(args_type_orig[0], (ModuleTypeGraphNode, ClassDefTypeGraphNode, FuncDefTypeGraphNode)):
                        args_type = args_type_orig[1:]
                        args = self.args[1:]
                        attr_call = False
                    else:
                        args_type = args_type_orig
                        args = self.args
                        attr_call = self.attrCall
                    try:
                        kwargs = func.getKWArgs(self.kwargs)
                    except AttributeError:
                        kwargs = [None]
                    for starargs_type in starargs:
                        for kwargs_type in kwargs:
                            res = process_product_elem(elem, args, args_type, self.starargs, starargs_type, self.kwargs, kwargs_type, attr_call)
                            self.nodeType = smart_union(self.nodeType, res)
        if len(self.nodeType) == 0:
            self.nodeType.add(type_unknown)

class ClassDefTypeGraphNode(TypeGraphNode):
    def __init__(self, name, parent_scope):
        super(ClassDefTypeGraphNode, self).__init__()
        self.nodeType   = set([self])
        self.name       = name
        self.scope      = Scope(parent_scope, Scope.class_scope)
        self.instances  = []
        self.bases      = []
        self.basesTypes = []

    def __deepcopy__(self, memo):
        return self

    def getScope(self):
        return self.scope

    def addInstance(self, inst):
        self.instances.append(inst)

class UsualClassDefTypeGraphNode(ClassDefTypeGraphNode):
    def __init__(self, node, parent_scope):
        super(UsualClassDefTypeGraphNode, self).__init__(node.name, parent_scope)
        for base in node.bases:
            link = base.link
            type_copy = deepcopy(link.nodeType)
            self.bases.append(link)
            self.basesTypes.append(type_copy)
            link.addDependency(DependencyType.Base, self)

class ExternClassDefTypeGraphNode(ClassDefTypeGraphNode):
    def __init__(self, name, parent_scope):
        super(ExternClassDefTypeGraphNode, self).__init__(name, parent_scope)

class ClassInstanceTypeGraphNode(TypeGraphNode):
    def __init__(self, cls):
        super(ClassInstanceTypeGraphNode, self).__init__()
        self.cls      = cls
        self.scope    = Scope(None)
        self.nodeType = set([self])
        cls.addInstance(self)

    def __ne__(self, other):
        return not (self == other)

    def __eq__(self, other):
        if not isinstance(other, ClassInstanceTypeGraphNode):
            return False
        if self.cls != other.cls:
            return False
        return self.scope == other.scope
       
    def __hash__(self):
        return hash((self.__class__, self.instance_hash()))

    def instance_hash(self):
        return hash((self.cls, self.scope))

    def __deepcopy__(self, memo):
        return copy_class_inst(self)

    def getScope(self):
        return self.scope

    def elem_types(self):
        return set()

class AttributeTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(AttributeTypeGraphNode, self).__init__()
        self.attr     = node.attr
        self.objects  = set()
        self.values   = set()
        self.nodeType = set()

    def process(self):
        set_attributes(self.objects, self.attr, self.values)
        self.nodeType = get_attributes(self.objects, self.attr)

class SubscriptTypeGraphNode(TypeGraphNode):
    def __init__(self, is_index, index):
        super(SubscriptTypeGraphNode, self).__init__()
        self.objects  = set()
        self.values   = set()
        self.nodeType = set()
        self.is_index = is_index
        self.index    = index

    def getKeysTypes(self):
        from typenodes import TypeDict
        dicts = [elem for elem in self.objects if isinstance(elem, TypeDict)]
        res   = []
        for dictionary in dicts:
            res.append(dictionary.keys_types())
        return res

    def process(self):
        new_objects    = set_subscripts(self.objects, self.values, self.is_index, self.index)
        self.objects   = smart_union(self.objects, new_objects)
        self.nodeType  = get_subscripts(self.objects, self.is_index, self.index)

    def processSlice(self, slices_types):
        new_objects    = set_slices(self.objects, slices_types)
        old_len        = smart_len(self.objects)
        self.objects   = smart_union(self.objects, new_objects)
        return smart_len(self.objects) > old_len

class PrintTypeGraphNode(TypeGraphNode):
    def __init__(self):
        super(PrintTypeGraphNode, self).__init__()
        self.nodeType = set()

class UnknownTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(UnknownTypeGraphNode, self).__init__()
        self.nodeType  = set([type_unknown]) 
