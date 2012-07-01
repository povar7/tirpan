'''
Created on 01.07.2012

@author: bronikkk 
'''

def find_name_in_class(cls, name):
    return cls.scope.findInScope(name)

def find_inits_in_classes(classes):
    from typegraph import FuncDefTypeGraphNode
    res = []
    for cls in classes:
        var  = find_name_in_class(cls, '__init__')
        res += [(cls, init) for init in var.nodeType if isinstance(init, FuncDefTypeGraphNode)]
    return res 

def make_new_instance(cls):
    from typegraph import ClassInstanceTypeGraphNode
    if cls is None:
        return None
    else:
        return ClassInstanceTypeGraphNode(cls)    
