'''
Created on 11.12.2011

@author: ramil
'''

from itertools    import product
from ast          import AugAssign, BinOp, UnaryOp, BoolOp, Call, List, Lambda, Name, Return
from copy         import deepcopy
from types        import NoneType

from classes      import copy_class_inst, find_inits_in_classes
from classes      import find_name_in_class_def, find_name_in_class_inst, find_name_in_class_inst_direct
from classes      import get_attributes, set_attributes
from classes      import get_subscripts, set_subscripts
from classes      import set_slices
from classes      import get_singletons_list
from funccall     import *
from returns      import check_returns
from scope        import Scope
from ticheckers   import *
from typenodes    import *
from utils        import *

type_none    = TypeNone()
type_unknown = TypeUnknown()

def check_args_for_dependence(args):
    if len(args) < 3:
        return None
    var_arg = args[1]
    sub_arg = args[2]
    if isinstance(var_arg, VarTypeGraphNode) and \
       isinstance(sub_arg, SubscriptTypeGraphNode) and \
       sub_arg.index is not None and \
       sub_arg.index.link is var_arg and \
       any([isinstance(elem, TypeDict) and elem._dict is not None for elem in sub_arg.objects]):
        return (1, 2, sub_arg.objects)
    else:
        return None

def need_to_skip(var_arg_type, sub_arg_type, objects):
    try:
        var_arg_name = var_arg_type.value
    except AttributeError:
        return False
    for obj in objects:
        try:
            dict_type = obj._dict[var_arg_name]
            if dict_type == sub_arg_type:
                return False
        except KeyError:
            pass
    return True

def smart_union(set1, set2, cond = None):
    import __main__
    from tivisitor import TIVisitor
    added_good_elements = 0
    if cond is not None:
        visitor = TIVisitor(None)
    for elem in set2:
        if len(set1) - added_good_elements >= __main__.types_number and \
           not isinstance(elem, (ModuleTypeGraphNode, TypeNone)):
	    set1.discard(type_unknown)
            return set1
        try:
            if cond is not None:
                try:
                    left_type  = get_attributes([elem], cond.left.attr)
                    ast_copy   = deepcopy(cond.comparators[0])
                    visitor.visit(ast_copy)
                    right_type = ast_copy.link.nodeType 
                    if not left_type.issuperset(right_type):
                        continue
                except:
                    pass
            set1.add(elem)
            if isinstance(elem, TypeBaseString) or \
               isinstance(elem, TypeList) and all([isinstance(atom, (TypeBaseString, TypeUnknown)) for atom in elem.elems]) or \
               isinstance(elem, TypeDict) and elem._dict or \
               isinstance(elem, ModuleTypeGraphNode):
                added_good_elements += 1
        except RuntimeError:
            pass
    if len(set1) > 1:
        set1.discard(type_unknown)
    return set1

def smart_union_dicts(set1, set2):
    for elem in set2:
        try:
            if isinstance(elem, TypeDict) and elem._dict:
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
    added_good_elements = 0
    set2_copy = deepcopy(set2)
    for elem in set2_copy:
        if len(set1) - added_good_elements >= __main__.types_number and \
           not isinstance(elem, (ModuleTypeGraphNode, TypeNone)):
            set1.discard(type_unknown)
            return set1
        try:
            set1.add(elem)
            if isinstance(elem, TypeBaseString) or \
               isinstance(elem, TypeList) and all([isinstance(atom, (TypeBaseString, TypeUnknown)) for atom in elem.elems]) or \
               isinstance(elem, TypeDict) and elem._dict or \
               isinstance(elem, ModuleTypeGraphNode):
                added_good_elements += 1
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


def filter_types(nodeType):
    false_types = set()
    true_types  = set()
    for elem in nodeType:
        if isinstance(elem, TypeNone) or \
           isinstance(elem, TypeListOrTuple) and len(elem.elems) == 0:
            false_types.add(elem)
        else:
            true_types.add(elem)
    return (true_types, false_types)

def filter_types_in_name(visitor, test, res):
    import __main__
    if isinstance(test, ast.Name):
        visitor.visit(test)
        if isinstance(test.link, VarTypeGraphNode):
            true_types, false_types = filter_types(test.link.nodeType)
            var = ExternVarTypeGraphNode(test.link.name, true_types)
            var.addDependency(DependencyType.Assign, test.link)
            __main__.current_scope.add(var)
            res.add((test.link, var))

def filter_types_in_condition(visitor, test):
    res = set()
    if isinstance(test, ast.BoolOp):
        if isinstance(test.op, ast.And):
            for value in test.values:
                check_basename_call(visitor, value)
                filter_types_in_name(visitor, value, res)
    else:
        check_basename_call(visitor, test)
        filter_types_in_name(visitor, test, res)
    return res

def unfilter_types_in_condition(var_pairs):
    import __main__
    for pair in var_pairs:
        link, var = pair
        __main__.current_scope.delete(var)
        try:
            if link.parent is __main__.current_scope:
                __main__.current_scope.add(link)
        except AttributeError:
            pass


class DependencyType(object):
    Assign       = 'assign'
    AssignElem   = 'assign_elem'
    AssignDouble = 'assign_double'
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

def common_elem_types(nodeType):
    el_types = set()
    for tt in nodeType:
        el_types |= tt.elem_types()
    return el_types

def common_elem_types_index(nodeType, index):
    el_types = set()
    for tt in nodeType:
        if isinstance(tt, TypeTuple) and isinstance(tt.elems, tuple):
            try:
                el_types.add(tt.elems[index])
                continue
            except IndexError:
                pass
        el_types |= tt.elem_types()
    return el_types

class TypeGraphNode(object):
    def __init__(self):
        self.deps = {}
        self.nodeType  = set()

    def get_atom_type_node(self, atom_type, value = None):
        if atom_type == int:
            return TypeInt(value)
        elif atom_type == long:
            return TypeLong()
        elif atom_type == complex:
            return TypeComplex()
        elif atom_type == float:
            return TypeFloat()
        elif atom_type == str:
            return TypeStr(value)
        elif atom_type == unicode:
            return TypeUnicode(value)
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
        index = args[0]
        try:
            cond = args[1]
        except IndexError:
            cond = None
        if index is not None:
            new_types = self.elem_types_index(index)
        else:
            new_types = self.elem_types()
        if len(new_types - dep.nodeType) > 0:
            dep.nodeType = smart_union(dep.nodeType, new_types, cond)
            dep.generic_dependency()

    def assign_double_dep(self, dep, *args):
        first_level = self.elem_types()
        try:
            index = args[0]
            new_types = common_elem_types_index(first_level, index)
        except IndexError:
            new_types = common_elem_types(first_level)
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
                res.add(tt1)
                continue
            elems_types = self.nodeType.copy()
            if len(elems_types) == 0 and \
               index is not None and \
               isinstance(tt1.elems, tuple):
                elems_types.add(type_unknown)
            for tt2 in elems_types:
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
                res.add(tt1)
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
                res.add(tt1)
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

    def attrobject_dep(self, dep, *args):
        try:
            is_string = args[0]
        except IndexError:
            is_string = False
        try:
            if len(self.nodeType - dep.objects) > 0:
                old_len = smart_len(dep.objects)
                if is_string:
                    dep.objects = smart_union_dicts(dep.objects, self.nodeType)
                else:
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
                #dep.nodeType = smart_deepcopy_union(dep.nodeType, self.objects)
                dep.nodeType = smart_union(dep.nodeType, self.objects)
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
        return common_elem_types(self.nodeType)

    def elem_types_index(self, index):
        return common_elem_types_index(self.nodeType, index)

    def __repr__(self):
        return '?'
   
class ConstTypeGraphNode(TypeGraphNode):
    def __init__(self, value, save = False):
        super(ConstTypeGraphNode, self).__init__()
        tp = self.get_atom_type_node(value.__class__, value if save else None)
        self.nodeType = set([tp])

class VarTypeGraphNode(TypeGraphNode):
    def __init__(self, name):
        super(VarTypeGraphNode, self).__init__()
        self.name         = name
        self.parent       = None
        self.line         = None
        self.col          = None

    def setParent(self, parent):
        self.parent       = parent

class UsualVarTypeGraphNode(VarTypeGraphNode):
    def __init__(self, name):
        super(UsualVarTypeGraphNode, self).__init__(name)
        self.paramNumber  = None
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

class ExternVarTypeGraphNode(VarTypeGraphNode):
    def __init__(self, name, var_type):
        super(ExternVarTypeGraphNode, self).__init__(name)
        if isinstance(var_type, set):
            self.nodeType = var_type
        else:
            self.nodeType = set([var_type])
                        
class ListTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(ListTypeGraphNode, self).__init__()
        self.nodeType  = set([TypeList()])
        if isinstance(node, List):
            elts = node.elts
        else:
            elts = [node.elt]
        for elt in elts:
            link = elt.link
            link.addDependency(DependencyType.Elem, self)
    
class TupleTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(TupleTypeGraphNode, self).__init__()
        tuple_type       = TypeTuple()
        tuple_type.elems = (type_none,) * len(node.elts)
        self.nodeType    = set([tuple_type])
        index = 0
        for elt in node.elts:
            link = elt.link
            link.addDependency(DependencyType.Elem, self, index)
            index += 1

class DictTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(DictTypeGraphNode, self).__init__()
        self.nodeType  = set([TypeDict()])
        for i in range(len(node.keys)):
            keyLink   = node.keys[i].link
            valueLink = node.values[i].link
            keyLink  .addDependency(DependencyType.Key, self)
            valueLink.addDependency(DependencyType.Val, self)
            index = None
            if isinstance(node.keys[i], ast.Num):
                index = node.keys[i].n
            elif isinstance(node.keys[i], ast.Str):
                index = node.keys[i].s
            if index is not None and len(valueLink.nodeType) == 1:
                for dict_type in self.nodeType:
                    if not isinstance(dict_type, TypeDict):
                        continue
                    if dict_type._dict is None:
                        dict_type._dict = {}
                    dict_type._dict[index] = list(valueLink.nodeType)[0]

class ModuleTypeGraphNode(TypeGraphNode):
    def __init__(self, name, parent_scope, inherited_scope):
        super(ModuleTypeGraphNode, self).__init__()
        self.nodeType = set([self])
        self.name     = name
        if inherited_scope is None:
            self.inherited = False
            self.scope     = Scope(parent_scope)
        else:
            self.inherited = True
            self.scope     = inherited_scope

    def __deepcopy__(self, memo):
        return self

    def getScope(self):
        return self.scope

    def isInherited(self):
        return self.inherited 

    def elem_types(self):
        return set()

class UsualModuleTypeGraphNode(ModuleTypeGraphNode):
    def __init__(self, ast, name, parent_scope, inherited_scope = None):
        super(UsualModuleTypeGraphNode, self).__init__(name, parent_scope, inherited_scope)
        self.ast      = ast

class ExternModuleTypeGraphNode(ModuleTypeGraphNode):
    def __init__(self, name, parent_scope):
        super(ExternModuleTypeGraphNode, self).__init__(name, parent_scope, None)
        self.isLoaded = False

class FuncDefTypeGraphNode(TypeGraphNode):
    MAX_LOAD           = 64
    EXTERNAL_FUNCTIONS = ['abspath', 'add_actions', 'append', 'basename', 'compile', 'dirname', 'encode', 'extend', 'getattr', 'insert', 'iter', 'join', 'listdir', 'match', 'set', 'setattr', 'str', 'unicode', 'walk']

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
        self.load      = 0

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

    def isLoadTooBig(self, cls):
        if self.name in FuncDefTypeGraphNode.EXTERNAL_FUNCTIONS:
            return False
        if cls and cls.name in ClassDefTypeGraphNode.EXTERNAL_CLASSES:
            return False
        return self.load > FuncDefTypeGraphNode.MAX_LOAD

    def increaseLoad(self, types_tuple):
        self.load += 1
        return True
    
    def decreaseLoad(self):
        if self.load > 0:
            self.load -= 1

class UsualFuncDefTypeGraphNode(FuncDefTypeGraphNode):
    def __init__(self, node, name, parent_scope):
        super(UsualFuncDefTypeGraphNode, self).__init__(name, parent_scope)
        if isinstance(node, Lambda):
            self.ast   = [node.body]
        else:
            self.ast   = node.body
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
        if self.name:
            self.defReturn = not check_returns(self.ast)
        else:
            self.defReturn = False

    def getKWArgs(self, kwargs):
        if self.kwarg is None and kwargs == {}:
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

    def mustBeExternal(self):
        return self.name in FuncDefTypeGraphNode.EXTERNAL_FUNCTIONS

class ExternFuncDefTypeGraphNode(FuncDefTypeGraphNode):
    def __init__(self, params_num, quasi, name, parent_scope, def_vals = {}, vararg = False):
        super(ExternFuncDefTypeGraphNode, self).__init__(name, parent_scope)
        for i in range(1, params_num + 1):
            param = self.params.addParam(i)
            if i in def_vals:
                def_type = def_vals[i]
                param.setDefaultParam()
                param.nodeType = set([def_type])
        if vararg:
            param = UsualVarTypeGraphNode('args')
            param.setVarParam()
            self.params.add(param)
        self.quasi = quasi

    def mustBeExternal(self):
        return False

class FuncCallTypeGraphNode(TypeGraphNode):
    def __init__(self, node, var = None):
        super(FuncCallTypeGraphNode, self).__init__()
        self.name      = None
        self.nodeType  = set()
        self.funcs     = set()
        self.classes   = set()
        self.line      = getLine(node)
        self.col       = getCol(node)
        self.fno       = getFileNumber(node)
        if var is None:
            try:
                var = node.func.link
            except AttributeError:
                var = None
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
            self.name     = var.attr
            nodeArgs      = [node.func]
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
        elif isinstance(node, BoolOp):
            nodeArgs += node.values
        elif isinstance(node, Call):
            nodeArgs += node.args
        try:
            func_flag = any([isinstance(atom, FuncDefTypeGraphNode) for atom in var.nodeType])
        except AttributeError:
            func_flag = False
        for arg in nodeArgs:
            link = arg.link
            if func_flag and (link is var) and isinstance(link, AttributeTypeGraphNode):

                correct_objects = True
                for obj in link.objects:
                    if isinstance(obj, (TypeInt, TypeNone)):
                        continue
                    if not isinstance(obj, ClassInstanceTypeGraphNode) or \
                       find_name_in_class_inst_direct(obj, var.attr):
                        correct_objects = True
                        break
                    correct_objects = False

                if not correct_objects:
                    new_objects     = set()
                    attr_string     = get_new_string(var.attr)
                    class_instances = [obj for obj in link.objects if isinstance(obj, ClassInstanceTypeGraphNode)]
                    for obj in class_instances:
                        get_attr_call = find_name_in_class_def(obj.cls, '__getattr__')
                        if get_attr_call:
                            template_elem  = (obj, attr_string) 
                            for get_attr_func in get_attr_call.nodeType:
                                try:
                                    template_ast = get_attr_func.templates[template_elem].ast
                                    if isinstance(template_ast, list) and \
                                       len(template_ast) == 1:
                                        return_stmt = template_ast[0]
                                        if isinstance(return_stmt, Return) and \
                                           isinstance(return_stmt.value, Call) and \
                                           isinstance(return_stmt.value.func, Name) and \
                                           return_stmt.value.func.id == 'getattr' and \
                                           len(return_stmt.value.args) == 2:
                                            get_attr_objects = return_stmt.value.args[0].link.nodeType 
                                            new_objects = new_objects.union(get_attr_objects)
                                except AttributeError:
                                    continue
                                except KeyError:
                                    continue
                    if len(new_objects) > 0 and \
                       all([isinstance(obj, (ClassInstanceTypeGraphNode, TypeInt, TypeNone)) for obj in new_objects]):
                        link.objects = new_objects

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
        if not hasattr(self, 'kwargsTypes'):
            if len(self.nodeType) == 0:
                self.nodeType.add(type_unknown)
            return
        import __main__
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
        dependent_args = check_args_for_dependence(self.args)
        for args_type_orig in product(*self.argsTypes):
            if dependent_args:
                var_number = dependent_args[0]
                sub_number = dependent_args[1]
                if need_to_skip(args_type_orig[var_number], args_type_orig[sub_number], dependent_args[2]):
                    continue

            if self.attrCall and \
               isinstance(args_type_orig[0], (ModuleTypeGraphNode, ClassDefTypeGraphNode, FuncDefTypeGraphNode, TypeAtom)) and not isinstance(args_type_orig[0], TypeBaseString):
                args_type = args_type_orig[1:]
                args = self.args[1:]
                attr_call = False
            else:
                args_type = args_type_orig
                args = self.args
                attr_call = self.attrCall

            if attr_call and isinstance(args_type[0], ClassInstanceTypeGraphNode) and \
               self.name and not find_name_in_class_inst(args_type[0], self.name):
                skip_flag = True
            else:
                skip_flag = False                 

            for elem in callables:
                _, func = elem
                if skip_flag and func.name == self.name:
                    continue
                try:
                    kwargs = func.getKWArgs(self.kwargs)
                except AttributeError:
                    kwargs = [None]
                for starargs_type in starargs:
                    for kwargs_type in kwargs:
                        if must_be_skipped(func):
                            res = set([type_none])
                        else:
                            res = process_product_elem(elem, \
                                                       args, args_type, \
                                                       self.starargs, starargs_type, \
                                                       self.kwargs, kwargs_type, \
                                                       attr_call, self.fno)
                        self.nodeType = smart_union(self.nodeType, res)

        if len(self.nodeType) == 0:
            self.nodeType.add(type_unknown)

class ClassDefTypeGraphNode(TypeGraphNode):
    EXTERNAL_CLASSES = ['ActionGroup']
 
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

    def __ne__(self, other):
        return not (self == other)

    def __eq__(self, other):
        if not isinstance(other, ClassDefTypeGraphNode):
            return False
        return self.instance_hash() == other.instance_hash()
       
    def __hash__(self):
        return hash((self.__class__, self.instance_hash()))

    def instance_hash(self):
        return hash(id(self))

    def getScope(self):
        return self.scope

    def addInstance(self, inst):
        self.instances.append(inst)

    def getInstances(self):
        return self.instances

    def __repr__(self):
        return '<class \'' + self.name + '\'>' 

class UsualClassDefTypeGraphNode(ClassDefTypeGraphNode):
    def __init__(self, node, parent_scope):
        super(UsualClassDefTypeGraphNode, self).__init__(node.name, parent_scope)
        for base in node.bases:
            link = base.link
            #type_copy = deepcopy(link.nodeType)
            type_copy = link.nodeType
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
        if self.cls.name in get_singletons_list(): 
            return True
        return self.instance_hash() == other.instance_hash()
       
    def __hash__(self):
        return hash((self.__class__, self.instance_hash()))

    def instance_hash(self):
        if self.cls.name in get_singletons_list():
            return hash((self.cls))
        return hash((self.cls, id(self)))

    def __deepcopy__(self, memo):
        return self

    def getScope(self):
        return self.scope

    def elem_types(self):
        return set()

    def __repr__(self):
        try:
            return '<%s object>' % self.cls.name
        except AttributeError:
            return '<? object>' 

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
        self.objects   = set()
        self.values    = set()
        self.nodeType  = set()
        self.is_index  = is_index
        self.index     = index

    def getKeysTypes(self):
        from typenodes import TypeDict
        dicts = [elem for elem in self.objects if isinstance(elem, TypeDict)]
        res   = []
        for dictionary in dicts:
            res.append(dictionary.keys_types())
        return res

    def process(self):
        index = None
        if index is None:
            try:
                index = self.index.n
            except AttributeError:
                pass
        if index is None:
            try:
                index = self.index.s
            except AttributeError:
                pass
        if index is None and isinstance(self.index, ast.Subscript):
            try:
                var = self.index.link
                if len(var.objects) == 1 and \
                   isinstance(list(var.objects)[0], TypeTuple) and \
                   isinstance(var.index, ast.Num) and \
                   len(var.nodeType) == 1:
                    index = list(var.nodeType)[0].value 
            except AttributeError:
                pass
        new_objects   = set_subscripts(self.objects, self.values, self.is_index, index)
        self.objects  = smart_union(self.objects, new_objects)
        self.nodeType = get_subscripts(self.objects, self.is_index, index)

    def processSlice(self, slices_types):
        new_objects   = set_slices(self.objects, slices_types)
        old_len       = smart_len(self.objects)
        self.objects  = smart_union(self.objects, new_objects)
        return smart_len(self.objects) > old_len

class PrintTypeGraphNode(TypeGraphNode):
    def __init__(self):
        super(PrintTypeGraphNode, self).__init__()
        self.nodeType = set()

class UnknownTypeGraphNode(TypeGraphNode):
    def __init__(self, node):
        super(UnknownTypeGraphNode, self).__init__()
        self.nodeType  = set([type_unknown]) 
