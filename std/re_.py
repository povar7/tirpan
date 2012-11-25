import re

from typenodes import *

type_unknown = TypeUnknown()

def find_re_module():
    from typegraph import ModuleTypeGraphNode
    import __main__
    var = __main__.current_scope.find('re')
    try:
        for elem in var.nodeType:
            if isinstance(elem, ModuleTypeGraphNode):
                return elem
    except AttributeError:
        pass
    return None 

def find_re_class(name):
    from typegraph import ClassDefTypeGraphNode
    module = find_re_module()
    try:
        var = module.getScope().find(name)
        for elem in var.nodeType:
            if isinstance(elem, ClassDefTypeGraphNode):
                return elem
    except AttributeError:
        pass
    return None

def quasi_compile(scope):
    from typegraph import ClassInstanceTypeGraphNode
    type1 = list(scope.findParam(1).nodeType)[0]
    try:
        pattern   = re.compile(type1.value)
        quasi_cls = find_re_class(get_quasi_pattern_name())
        if not quasi_cls:
            return set([type_unknown])
        quasi_res = ClassInstanceTypeGraphNode(quasi_cls)
        quasi_res.data = pattern
        return set([quasi_res])
    except:
        return set([type_unknown])

def quasi_match(scope):
    from typegraph import ClassInstanceTypeGraphNode
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    try:
        match     = type1.data.match(type2.value) 
        quasi_cls = find_re_class(get_quasi_match_name())
        if not quasi_cls:
            return set([type_unknown])
        quasi_res = ClassInstanceTypeGraphNode(quasi_cls)
        quasi_res.data = match
        return set([quasi_res])
    except:
        return set([type_unknown])

def quasi_groups(scope):
    from typenodes import get_new_string
    type1 = list(scope.findParam(1).nodeType)[0]
    try:
        groups    = type1.data.groups()
        res       = TypeTuple()
        tmp_list  = []
        for elem in groups:
            tmp   = get_new_string(elem)
            tmp_list.append(tmp)
        res.elems = tuple(tmp_list)
        return set([res])
    except:
        return set([type_unknown])

functions = [                                                \
                ['compile', quasi_compile, 1],               \
            ]

stubs     = [                                                \
            ]

variables = [                                                \
            ]

modules   = [                                                \
            ]

def get_quasi_pattern_name():
    return 'SRE_Pattern'

quasi_pattern_object = (                                     \
                           get_quasi_pattern_name(),         \
                           [                                 \
                               ['match', quasi_match, 2]     \
                           ],                                \
                           [                                 \
                           ]
                       )

def get_quasi_match_name():
    return 'SRE_Match'

quasi_match_object = (                                       \
                         get_quasi_match_name(),             \
                         [                                   \
                             ['groups', quasi_groups, 1]     \
                         ],                                  \
                         [                                   \
                         ]
                     )

objects   = [                                                \
                quasi_pattern_object,                        \
                quasi_match_object                           \
            ]

def get_all():
    return (functions, stubs, variables, modules, objects)
