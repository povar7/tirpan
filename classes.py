'''
Created on 01.07.2012

@author: bronikkk 
'''

from builtin import get_quasi_list, get_quasi_str, get_quasi_unicode
from copy    import copy as shallowcopy, deepcopy

def get_singletons_list():
    return ['GuiPluginManager', 'BasePluginManager', 'PluginRegister']

def copy_class_inst(class_inst):
    try:
        if class_inst.cls.name in get_singletons_list():
            return class_inst
    except AttributeError:
        pass
    save = class_inst.scope
    class_inst.scope = None
    res  = shallowcopy(class_inst)
    class_inst.scope = save
    res.nodeType = set([res])
    save = class_inst.scope.variables
    class_inst.scope.variables = None 
    res.scope = shallowcopy(class_inst.scope)
    class_inst.scope.variables = save
    res.scope.variables = {}
    try:
        for pair in class_inst.scope.variables.items():
            name, var = pair
            save = var.nodeType
            var.nodeType = None
            var_copy = shallowcopy(var)
            var.nodeType = save
            try:
                var_copy.nodeType = shallowcopy(var.nodeType)
            except RuntimeError:
                var_copy.nodeType = var.nodeType
            var_copy.parent = res.scope
            res.scope.variables[name] = var_copy 
    except AttributeError:
        pass
    res.cls.addInstance(res)
    return res

def find_name_in_class_def(class_def, name):
    from typegraph import ClassDefTypeGraphNode
    res = class_def.scope.findInScope(name)
    if res is not None:
        return res
    for baseType in class_def.basesTypes:
        base_class_defs = set([elem for elem in baseType if isinstance(elem, ClassDefTypeGraphNode)])
        for elem in base_class_defs:
            res = elem.scope.findInScope(name)
            if res is not None:
                return res
    return None

def find_name_in_module(module, name):
    return module.scope.findInScope(name)

def find_name_in_class_inst(class_inst, name):
    res = class_inst.scope.findInScope(name)
    if res:
        return res
    else:
        return find_name_in_class_def(class_inst.cls, name)

def find_inits_in_classes(classes):
    from typegraph import FuncDefTypeGraphNode
    res = []
    for cls in classes:
        var  = find_name_in_class_def(cls, '__init__')
        try:
            res += [(cls, init) for init in var.nodeType if isinstance(init, FuncDefTypeGraphNode)]
        except AttributeError:
            res += [(cls, None)]
    return res 

def get_attribute(elem, attr):
    from typegraph import ClassDefTypeGraphNode, ClassInstanceTypeGraphNode, ModuleTypeGraphNode
    from typenodes import TypeList, TypeStr, TypeUnicode
    if isinstance(elem, ModuleTypeGraphNode):
        return find_name_in_module(elem, attr)
    elif isinstance(elem, ClassInstanceTypeGraphNode):
        return find_name_in_class_inst(elem, attr)
    elif isinstance(elem, ClassDefTypeGraphNode):
        return find_name_in_class_def(elem, attr)
    elif isinstance(elem, (TypeList, TypeStr, TypeUnicode)):
        if isinstance(elem, TypeList):
            elem = get_quasi_list()
        elif isinstance(elem, TypeStr):
            elem = get_quasi_str()
        elif isinstance(elem, TypeUnicode):
            elem = get_quasi_unicode()
        return find_name_in_class_def(elem, attr)
    else:
        return None

def get_attributes(objects, attr):
    res = set()
    for obj in objects:
        var = get_attribute(obj, attr)
        if var:
            try:
                res = res.union(var.nodeType)
            except RuntimeError:
                pass
    return res

def make_new_instance(cls):
    from typegraph import ClassInstanceTypeGraphNode
    if cls is None:
        return None
    else:
        return ClassInstanceTypeGraphNode(cls)

def avoid_loop(obj, attr, value):
    siblings = [elem for elem in obj.cls.instances if elem.deps is obj.deps]
    for sibling in siblings:
        sibling_attr = sibling.scope.findInScope(attr)
        try:
            if value in sibling_attr.nodeType:
                return True
        except AttributeError:
            pass
    return False

def set_attribute_smart(obj, attr, value, var, init_flag):
    from typegraph import ClassDefTypeGraphNode, ClassInstanceTypeGraphNode
    if var and var.parent.isClassScope() and isinstance(obj, ClassInstanceTypeGraphNode):
        var = None
    if not var or not var.parent.isClassScope():
        if avoid_loop(obj, attr, value):
            return
        if not var and (init_flag or isinstance(obj, ClassDefTypeGraphNode)):
            res = obj
        else:
            res = copy_class_inst(obj)
        var = res.scope.addToScope(attr)
        var.nodeType = set([value])
        res.generic_dependency()
    else:
        var.nodeType.add(value)

def set_attribute(obj, attr, value, var, init_flag):
    from typegraph import ClassInstanceTypeGraphNode
    if var and var.parent.isClassScope() and isinstance(obj, ClassInstanceTypeGraphNode):
        var = None
    if not var:
        try:
            var = obj.scope.addToScope(attr)
        except AttributeError:
            var = None
    if var:
        try:
            var.nodeType.add(value)
        except RuntimeError:
            pass

def set_attributes(objects, attr, values):
    import __main__
    from typegraph import FuncDefTypeGraphNode
    try:
        init_flag = __main__.current_scope.parent.isInitScope()
    except AttributeError:
        init_flag = False 
    for obj in objects:
        if isinstance(obj, FuncDefTypeGraphNode):
            continue
        var = get_attribute(obj, attr)
        for value in values:  
            set_attribute(obj, attr, value, var, init_flag)

def set_subscript(collection, values, is_index, index):
    from typenodes import TypeList, TypeTuple, TypeDict
    res = set()
    if not isinstance(collection, (TypeList, TypeTuple, TypeDict)):
        return res
    if isinstance(collection, TypeDict) and \
        collection._dict is None and \
        len(collection.keys) == 0:
        return res
    for value in values:
        if is_index:
            if value not in collection.elem_types():
                if isinstance(collection, TypeDict) and \
                   collection._dict is None and \
                   len(collection.vals) == 0:
                    collection_copy = collection
                else:
                    collection_copy = deepcopy(collection)
                if index is not None and \
                   isinstance(collection_copy, TypeTuple) and \
                   isinstance(collection_copy.elems, tuple):
                    try:
                        elems_list = list(collection_copy.elems)
                        elems_list[index] = value
                        collection_copy.elems = tuple(elems_list)
                    except IndexError:
                        collection_copy.add_elem(value)
                else:
                    collection_copy.add_elem(value)
                res.add(collection_copy)
        else:
            if not isinstance(value, (TypeList, TypeTuple)):
                continue
            if len(value.elem_types() - collection.elem_types()) != 0:
                collection_copy = deepcopy(collection)
                for elem_type in value.elem_types():
                    collection_copy.add_elem(elem_type)
                res.add(collection_copy)
    return res

def set_subscripts(objects, values, is_index, index):
    res = set()
    for obj in objects:
        res = res.union(set_subscript(obj, values, is_index, index))
    return res

def get_subscript(collection, index):
    from typenodes import TypeListOrTuple, TypeDict
    if isinstance(collection, TypeListOrTuple):
        if index is not None and isinstance(collection.elems, tuple):
            try:
                return set([collection.elems[index]])
            except IndexError:
                pass
        return collection.elem_types()
    elif isinstance(collection, TypeDict):
        if index is not None and isinstance(collection._dict, dict):
            try:
                return set([collection._dict[index]])
            except KeyError:
                pass        
        return collection.vals
    else:
        return set()

def get_subscripts(objects, is_index, index):
    res = set()
    for obj in objects:
        if is_index:
            types = get_subscript(obj, index)
        else:
            types = set([obj])
        res = res.union(types)
    return res

def set_slice(dictionary, slices_types):
    from typegraph import ClassInstanceTypeGraphNode
    res = set()
    keys = dictionary.keys_types()
    for slice_type in slices_types:
        if slice_type not in keys:
            if isinstance(slice_type, ClassInstanceTypeGraphNode) and \
               any([isinstance(key, ClassInstanceTypeGraphNode) and key.cls == slice_type.cls for key in keys]):
                continue
            dictionary_copy = deepcopy(dictionary)
            dictionary_copy.add_key(slice_type)
            res.add(dictionary_copy)
    return res

def set_slices(objects, slices_types):
    from typenodes import TypeDict
    dicts = [elem for elem in objects if isinstance(elem, TypeDict)]
    res   = set()
    for dictionary in dicts:
        res = res.union(set_slice(dictionary, slices_types))
    return res
