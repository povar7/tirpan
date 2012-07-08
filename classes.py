'''
Created on 01.07.2012

@author: bronikkk 
'''

from copy import copy as shallowcopy, deepcopy

def copy_class_inst(class_inst):
    res = shallowcopy(class_inst)
    res.nodeType = set([res])
    res.scope = deepcopy(class_inst.scope)
    res.cls.addInstance(res)
    return res

def find_name_in_class_def(class_def, name):
    return class_def.scope.findInScope(name)

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
    from typegraph import ClassDefTypeGraphNode, ClassInstanceTypeGraphNode
    if isinstance(elem, ClassInstanceTypeGraphNode):
        return find_name_in_class_inst(elem, attr)
    elif isinstance(elem, ClassDefTypeGraphNode):
        return find_name_in_class_def(elem, attr)
    else:
        return None

def get_attributes(objects, attr):
    res = set()
    for obj in objects:
        var = get_attribute(obj, attr)
        if var:
            res = res.union(var.nodeType)
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
        var.nodeType = var.nodeType.union(set([value]))

def set_attribute(obj, attr, value, var, init_flag):
    from typegraph import ClassInstanceTypeGraphNode
    if var and var.parent.isClassScope() and isinstance(obj, ClassInstanceTypeGraphNode):
        var = None
    if not var:
        var = obj.scope.addToScope(attr)
    var.nodeType = var.nodeType.union(set([value]))

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
