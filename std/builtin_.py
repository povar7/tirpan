'''
Created on 01.04.2012

@author: bronikkk
'''

import ast

from copy import copy as shallowcopy

from typenodes import *

type_int     = TypeInt()
type_none    = TypeNone()
type_str     = TypeStr()
type_str0    = TypeStr('')
type_type    = TypeType()
type_unicode = TypeUnicode()

type_list    = TypeList()

def quasi_append(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    if not isinstance(type1, TypeList):
        return set([type_none])
    type1.add_elem(type2)
    return set([type_none])

def quasi_extend(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    if not isinstance(type1, TypeList):
        return set([type_none])
    if not isinstance(type2, TypeListOrTuple):
        return set([type_none])
    for elem in type2.elems:
        type1.add_elem(elem)
    return set([type_none])

def quasi_execfile(scope, **kwargs):
    type1 = list(scope.findParam(1).nodeType)[0]
    try:
        if type1.value is not None:
            from tiparser  import TIParser
            from typegraph import UsualModuleTypeGraphNode
            import __main__
            parser        = TIParser(type1.value)
            imported_tree = parser.ast
            old_fileno    = kwargs['FILE_NUMBER']
            old_scope     = __main__.importer.get_ident(old_fileno).scope 
            module        = UsualModuleTypeGraphNode(imported_tree, type1.value, None, old_scope)
            new_fileno    = __main__.importer.put_ident(module)
            imported_tree.link = module
            for node in ast.walk(imported_tree):
                node.fileno = new_fileno
            parser.walk(False)
    except:
        pass
    return set([type_none])

def quasi_getattr(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    try:
        value = type2.value
        if value is not None:
            from classes import get_attributes
            return get_attributes(set([type1]), value)
    except AttributeError:
        pass
    return set() 

def quasi_import(scope, **kwargs):
    type1 = list(scope.findParam(1).nodeType)[0]
    try:
        value = type1.value
    except AttributeError:
        return set()
    if value is not None:
        import __main__
        from tiimporter import QuasiAlias
        fileno   = kwargs['FILE_NUMBER']
        filename = __main__.importer.get_ident(fileno).name
        res = __main__.importer.import_files(filename, [QuasiAlias(type1.value, QuasiAlias.NONAME)])
        return set([res])
    return set()

def quasi_iter(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    if not isinstance(type1, TypeListOrTuple):
        return set([type_none])
    res = shallowcopy(type1)
    return set([res])

def quasi_len(scope):
    return set([type_int])

def quasi_set(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    res   = shallowcopy(type1)
    return set([res])

def quasi_setattr(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    type3 = list(scope.findParam(3).nodeType)[0]
    try:
        value = type2.value
        if value is not None:
            from classes import set_attributes
            set_attributes(set([type1]), value, set([type3]))
    except AttributeError:
        pass
    return set([type_none]) 

def quasi_range1(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    if type1 == type_int:
        type_list = TypeList()
        type_list.add_elem(type_int)
        return set([type_list])
    else:
        return set()

def quasi_range3(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    type3 = list(scope.findParam(3).nodeType)[0]
    if type1 == type_int and type2 == type_int and type3 == type_int:
        type_list = TypeList()
        type_list.add_elem(type_int)
        return set([type_list])
    else:
        return set()

def quasi_str(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    try:
        res = TypeStr(str(type1.value))
        return set([res])
    except:
        return set([type_str])

def quasi_type1(scope):
    return set([type_type])

def quasi_type_var():
    return type_type

def quasi_unicode(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    if not isinstance(type1, TypeStr) or type1.value is None:
        return set([type_unicode])
    else:
        res = TypeUnicode(unicode(type1.value))
        return set([res])

def quasi_encode(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    res   = shallowcopy(type1)
    return set([res])

def quasi_insert(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type3 = list(scope.findParam(3).nodeType)[0]
    if not isinstance(type1, TypeList):
        return set([type_none])
    if isinstance(type1.elems, list):
        if type3 not in type1.elems:
            type1.elems.insert(0, type3)
    else:
        type1.add_elem(type3)
    return set([type_none])

def get_quasi_list_name():
    return '#list#'

def get_quasi_str_name():
    return '#str#'

def get_quasi_unicode_name():
    return '#unicode#'

functions = [
                ['execfile'  , quasi_execfile, 3 , {2 : type_none, 3 : type_none}], \
                ['getattr'   , quasi_getattr , 2],                                  \
                ['__import__', quasi_import  , 1],                                  \
                ['iter'      , quasi_iter    , 1],                                  \
                ['len'       , quasi_len     , 1],                                  \
                ['range'     , quasi_range1  , 1],                                  \
                ['range'     , quasi_range3  , 3 , {3 : type_int}],                 \
                ['set'       , quasi_set     , 1 , {1 : type_list}],                \
                ['str'       , quasi_str     , 1 , {1 : type_str0}],                \
                ['setattr'   , quasi_setattr , 3],                                  \
                ['type'      , quasi_type1   , 1],                                  \
                ['xrange'    , quasi_range1  , 1],                                  \
                ['xrange'    , quasi_range3  , 3 , {3 : type_int}],                 \
                ['unicode'   , quasi_unicode , 3 , {2 : type_str, 3 : type_str}]    \
            ]

stubs     = [                                                \
            ]

variables = [                                                \
                ['type'     , quasi_type_var],               \
                ['object'   , quasi_type_var],               \
                ['int'      , quasi_type_var],               \
                ['long'     , quasi_type_var],               \
                ['float'    , quasi_type_var],               \
                ['bool'     , quasi_type_var],               \
                ['complex'  , quasi_type_var],               \
                ['str'      , quasi_type_var],               \
                ['unicode'  , quasi_type_var],               \
                ['buffer'   , quasi_type_var],               \
                ['tuple'    , quasi_type_var],               \
                ['list'     , quasi_type_var],               \
                ['dict'     , quasi_type_var],               \
                ['file'     , quasi_type_var],               \
                ['slice'    , quasi_type_var],               \
                ['NameError', quasi_type_var]                \
            ]

modules   = [                                                \
                ['sys'],                                     \
                ['_glib']                                    \
            ]

quasi_list_object = (                                        \
                        get_quasi_list_name(),               \
                        [                                    \
                            ['append', quasi_append, 2],     \
                            ['extend', quasi_extend, 2],     \
                            ['insert', quasi_insert, 3]      \
                        ],                                   \
                        [                                    \
                        ]
                    )

quasi_str_object  = (                                        \
                        get_quasi_str_name(),                \
                        [                                    \
                            ['encode', quasi_encode, 2]      \
                        ],                                   \
                        [                                    \
                        ]
                    )

quasi_unicode_object  = (                                    \
                            get_quasi_unicode_name(),        \
                            [                                \
                                ['encode', quasi_encode, 2]  \
                            ],                               \
                            [                                \
                            ]
                        )

objects   = [                                                \
                quasi_list_object   ,                        \
                quasi_str_object    ,                        \
                quasi_unicode_object                         \
            ]

def get_all():
    return (functions, stubs, variables, modules, objects)
