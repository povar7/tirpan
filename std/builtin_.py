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
type_type    = TypeType()
type_unicode = TypeUnicode()

def quasi_append(scope):
    type1 = list(scope.findParam(1).nodeType)[0]
    type2 = list(scope.findParam(2).nodeType)[0]
    if not isinstance(type1, TypeList):
        return set([type_none])
    type1.add_elem(type2)
    return set([type_none])

def quasi_execfile(scope, **kwargs):
    type1 = list(scope.findParam(1).nodeType)[0]
    try:
        fileno = kwargs['FILE_NUMBER']
    except KeyError:
        fileno = None
    try:
        from tiparser  import TIParser
        if type1.value is not None:
            parser = TIParser(type1.value)
            imported_tree = parser.ast
            for node in ast.walk(imported_tree):
                node.fileno = fileno
            for stmt in imported_tree.body:
                parser.visitor.visit(stmt)
    except:
        pass
    return set([type_none])

def quasi_len(scope):
    return set([type_int])

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
    res = shallowcopy(type1)
    return set([res])

def get_quasi_list_name():
    return '#list#'

def get_quasi_str_name():
    return '#str#'

def get_quasi_unicode_name():
    return '#unicode#'

functions = [
                ['execfile', quasi_execfile, 3 , {2 : type_none, 3 : type_none}], \
                ['len'     , quasi_len     , 1],                                  \
                ['range'   , quasi_range1  , 1],                                  \
                ['range'   , quasi_range3  , 3 , {3 : type_int}],                 \
                ['type'    , quasi_type1   , 1],                                  \
                ['xrange'  , quasi_range1  , 1],                                  \
                ['xrange'  , quasi_range3  , 3 , {3 : type_int}],                 \
                ['unicode' , quasi_unicode , 3 , {3 : type_str}]                  \
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
                            ['append', quasi_append, 2]      \
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
