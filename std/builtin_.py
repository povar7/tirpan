'''
Created on 05.06.2013

@author: bronikkk
'''

import ast
import copy
import itertools
import types

from ti.lookup import *
from ti.sema   import *

typeBool    = LiteralSema(bool)
typeComplex = LiteralSema(complex)
typeFloat   = LiteralSema(float)
typeInt     = LiteralSema(int)
typeLong    = LiteralSema(long)
typeNone    = LiteralSema(types.NoneType)
typeType    = LiteralSema(type)
typeStr     = LiteralSema(str)
typeUnicode = LiteralSema(unicode)

def quasiAppend(params, **kwargs):
    if isinstance(params[0], ListSema):
        params[0].addElementsAtIndex(None, {params[1]})
    return {typeNone}

def quasiExtend(params, **kwargs):
    if (isinstance(params[0], ListSema) and
        isinstance(params[1], ListSema)):
        elements = params[1].getElements()
        params[0].addElementsAtIndex(None, elements)
    return {typeNone}

def quasiInsert(params, **kwargs):
    if isinstance(params[0], ListSema):
        params[0].addElementsAtIndex(None, {params[2]})
    return {typeNone}

def quasiEncode(params, **kwargs):
    res = params[0]
    return {res}

def quasiExecfile(params, **kwargs):
    filename = params[0].value
    if filename is not None:
        import config
        from ti.parser import Parser
        from ti.tgnode import UsualModuleTGNode
        try:
            parser = Parser(filename)
            tree   = parser.getAST()
        except IOError:
            return {typeNone}
        importer  = config.data.importer
        oldNumber = kwargs['FILE_NUMBER']
        oldScope  = importer.getFileScope(oldNumber) 
        module    = UsualModuleTGNode(tree, filename, None, oldScope)
        newNumber = importer.putIdent(module)
        tree.link = module
        for node in ast.walk(tree):
            node.fileno = newNumber
        parser.walk()
    return {typeNone}

def quasiIter(params, **kwargs):
    param = params[0]
    try:
        return param.getElements()
    except AttributeError:
        return set()

def quasiLen(params, **kwargs):
    try:
        return {LiteralValueSema(len(params[0].value))}
    except AttributeError:
        return {typeInt}

def quasiRange1(params, **kwargs):
    return quasiRange3(params + [typeInt, typeInt])

def quasiRange3(params, **kwargs):
    if (not isinstance(params[0], LiteralSema) or
        params[0].ltype not in (int, long)):
        return set()
    if (not isinstance(params[1], LiteralSema) or
        params[1].ltype not in (int, long)):
        return set()
    listType = ListSema(0)
    if params[0].ltype == long or params[1].ltype == long:
        listType.addElementsAtIndex(None, {typeInt, typeLong})
    else:
        listType.addElementsAtIndex(None, {typeInt})
    return {listType}

def quasiSet(params, **kwargs):
    param = params[0]
    return {param}

def quasiGetattr(params, **kwargs):
    obj  = params[0]
    attr = params[1]
    try:
        name = str(attr.value)
        return lookupTypes(obj, name)
    except:
        return set()

def quasiSetattr(params, **kwargs):
    obj   = params[0]
    attr  = params[1]
    value = params[2]
    try:
        name   = str(attr.value)
        values = {value}
        setTypes(obj, name, values)
    except:
        pass
    return {typeNone}

def quasiType(params, **kwargs):
    return {typeType}

def quasiTypeVar():
    return {typeType}

def quasiUnicode(params, **kwargs):
    try:
        res = LiteralValueSema(unicode(params[0].value))
        return {res}
    except AttributeError:
        return {typeUnicode}

baseStringClassName = str(basestring)

def getBaseStringClassName():
    return baseStringClassName

baseStringClass = (
                      baseStringClassName,
                      [
                          ['encode', quasiEncode, 2],
                      ],
                      [
                      ]
                  )

listClassName = str(type([]))

def getListClassName():
    return listClassName

listClass = (
                listClassName,
                [
                    ['append', quasiAppend, 2],
                    ['extend', quasiExtend, 2],
                    ['insert', quasiInsert, 3],
                ],
                [
                ]
            )

def quasiAdd(params, **kwargs):
    left  = params[0]
    right = params[1]

    if isinstance(left, ListSema) and isinstance(right, ListSema):
        res = ListSema()
        res.elems = copy.copy(left.elems)
        res.addElementsAtKey(None, right.getElements())
        return {res}

    if isinstance(left, TupleSema) and isinstance(right, TupleSema):
        res = TupleSema()
        res.elems = copy.copy(left.elems)
        res.addElementsAtKey(None, right.getElements())
        return {res}

    if not isinstance(left , LiteralSema):
        return set()
    if not isinstance(right, LiteralSema):
        return set()

    if (left.ltype  in (str, unicode) and
        right.ltype in (str, unicode)):
        try:
            res = LiteralValueSema(left.value + right.value)
        except AttributeError:
            if left.ltype == unicode and right.ltype == unicode:
                res = typeUnicode
            else:
                res = typeStr
        return {res}

    if left.ltype == complex or  right.ltype == complex:
        return {typeComplex}
    if left.ltype == float   or  right.ltype == float:
        return {typeFloat}
    if left.ltype == long    or  right.ltype == long:
        return {typeLong}
    if left.ltype == bool    and right.ltype == bool:
        return {typeInt}

    return {typeInt, typeLong}

def quasiBitand(params, **kwargs):
    left  = params[0]
    right = params[1]

    if (not isinstance(left, LiteralSema) or
        left.ltype not in (bool, int, long)):
        return set()
    if (not isinstance(right, LiteralSema) or
        right.ltype not in (bool, int, long)):
        return set()

    if left.ltype == long or right.ltype == long:
        return {typeLong}
    if left.ltype == int  or right.ltype == int:
        return {typeInt}

    return {typeBool}

def quasiBitor(params, **kwargs):
    return quasiBitand(params, **kwargs)

def quasiDiv(params, **kwargs):
    left  = params[0]
    right = params[1]

    if (not isinstance(left, LiteralSema) or
        left.ltype in (str, unicode)):
        return set()
    if (not isinstance(right, LiteralSema) or
        right.ltype in (str, unicode)):
        return set()

    if left.ltype == complex or right.ltype == complex:
        return {typeComplex}
    if left.ltype == float   or right.ltype == float:
        return {typeFloat}
    if left.ltype == long    or right.ltype == long:
        return {typeLong}

    return {typeInt}

def quasiFloordiv(params, **kwargs):
    return quasiDiv(params, **kwargs)

def quasiMult(params, **kwargs):
    left  = params[0]
    right = params[1]

    if (isinstance(left,  LiteralSema) and left.ltype  in (str, unicode) and
        isinstance(right, LiteralSema) and right.ltype in (bool, int, long)):
        if left.ltype == str:
            return {typeStr}
        if left.ltype == unicode:
            return {typeUnicode}

    if (isinstance(right, LiteralSema) and right.ltype in (str, unicode) and
        isinstance(left,  LiteralSema) and left.ltype  in (bool, int, long)):
        if right.ltype == str:
            return {typeStr}
        if right.ltype == unicode:
            return {typeUnicode}

    if (isinstance(left, (ListSema, TupleSema)) and
        isinstance(right, LiteralSema) and right.ltype in (bool, int, long)):
        return {left}

    if (isinstance(right, (ListSema, TupleSema)) and
        isinstance(left,   LiteralSema) and left.ltype in (bool, int, long)):
        return {right}

    if (isinstance(left, LiteralSema) and left.ltype == int and
        isinstance(right, LiteralSema) and right.ltype == int):
        return {typeInt, typeLong}

    return quasiDiv(params, **kwargs)

def quasiSub(params, **kwargs):
    left  = params[0]
    right = params[1]

    if (isinstance(left, (ListSema, TupleSema)) or
        isinstance(left, LiteralSema) and left.ltype in (str, unicode)):
        return set()
    if (isinstance(right, (ListSema, TupleSema)) or
        isinstance(right, LiteralSema) and right.ltype in (str, unicode)):
        return set()

    return quasiAdd(params, **kwargs)

def quasiLShift(params, **kwargs):
    left  = params[0]
    right = params[1]

    if (not isinstance(left, LiteralSema) or
        left.ltype not in (bool, int, long)):
        return set()
    if (not isinstance(right, LiteralSema) or
        right.ltype not in (bool, int, long)):
        return set()

    if left.ltype == bool:
        left = typeInt
    if right.ltype == bool:
        return {left}
    if left.ltype == long or right.ltype == long:
        return {typeLong}

    return {typeInt, typeLong}

def quasiRShift(params, **kwargs):
    left  = params[0]
    right = params[1]

    if (not isinstance(left, LiteralSema) or
        left.ltype not in (bool, int, long)):
        return set()
    if (not isinstance(right, LiteralSema) or
        right.ltype not in (bool, int, long)):
        return set()

    if left.ltype == bool:
        left = typeInt
    if right.ltype == bool:
        return {left}
    if left.ltype == long or right.ltype == long:
        return {typeLong}

    return {typeInt}

def quasiMod(params, **kwargs):
    left  = params[0]
    right = params[1]

    if isinstance(left, LiteralSema) and left.ltype in (str, unicode):
        res = set()
        if isinstance(right, TupleSema):
            elems = right.elems[1:]
        else:
            elems = [{right}]
        for atom in itertools.product(*elems):
            try:
                tmp  = tuple([elem.value for elem in atom])
                part = left.value % tmp
                res.add(LiteralValueSema(part))
            except:
                if left.ltype == str:
                    res.add(typeStr)
                elif left.ltype == unicode:
                    res.add(typeUnicode)
        return res

    return quasiDiv(params, **kwargs)

def quasiPow(params, **kwargs):
    left  = params[0]
    right = params[1]

    if isinstance(left, (ListSema, TupleSema)):
        return set()
    if isinstance(left,  LiteralSema) and left.ltype in (str, unicode):
        return set()

    if isinstance(right, (ListSema, TupleSema)):
        return set()
    if isinstance(right,  LiteralSema) and right.ltype in (str, unicode):
        return set()

    if (isinstance(left, LiteralSema) and left.ltype == int and
        isinstance(right, LiteralSema) and right.ltype == int):
        return {typeInt, typeLong}

    return quasiDiv(params, **kwargs)

def quasiUplus(params, **kwargs):
    oper = params[0]
    if (not isinstance(oper, LiteralSema) or
        oper.ltype in (str, unicode)):
        return set()
    if oper.ltype == bool:
        oper = typeInt
    return {oper}

def quasiUminus(params, **kwargs):
    oper = params[0]
    try:
        return {LiteralValueSema(-oper.value)}
    except:
        pass
    if oper.ltype == int:
        return {typeInt, typeLong}
    return quasiUplus(params, **kwargs)

def quasiInvert(params, **kwargs):
    oper = params[0]
    if (not isinstance(oper, LiteralSema) or
        oper.ltype not in (bool, int, long)):
        return set()
    if oper.ltype == long:
        return {typeLong}
    return {typeInt}

def quasiNot(params, **kwargs):
    return {typeBool}

functions = [
                ['+'         , quasiAdd     , 2                     ],
                ['-'         , quasiSub     , 2                     ],
                ['*'         , quasiMult    , 2                     ],
                ['/'         , quasiDiv     , 2                     ],
                ['//'        , quasiFloordiv, 2                     ],
                ['&'         , quasiBitand  , 2                     ],
                ['|'         , quasiBitor   , 2                     ],
                ['<<'        , quasiLShift  , 2                     ],
                ['>>'        , quasiRShift  , 2                     ],
                ['%'         , quasiMod     , 2                     ],
                ['**'        , quasiPow     , 2                     ],

                ['+'         , quasiUplus   , 1                     ],
                ['-'         , quasiUminus  , 1                     ],
                ['~'         , quasiInvert  , 1                     ],
                ['!'         , quasiNot     , 1                     ],

                ['execfile'  , quasiExecfile, 3, {'2' : {typeNone},
                                                  '3' : {typeNone} }],

                ['unicode'   , quasiUnicode , 3, {'2' : {typeStr },
                                                  '3' : {typeStr } }],

                ['iter'      , quasiIter    , 1                     ],
                ['len'       , quasiLen     , 1                     ],
                ['range'     , quasiRange1  , 1                     ],
                ['range'     , quasiRange3  , 3, {'3' : {typeInt}}  ],
                ['set'       , quasiSet     , 1                     ],
                ['type'      , quasiType    , 1                     ],

                ['getattr'   , quasiGetattr , 2                     ],
                ['setattr'   , quasiSetattr , 3                     ],
            ]

variables = [
                ['int'       , quasiTypeVar    ],
                ['type'      , quasiTypeVar    ],
            ]

modules   = [
                ['posixpath', 'os.path'],

                ['getopt'   ],
                ['glib'     ],
                ['gtk'      ],
                ['logging'  ],
                ['os'       ],
                ['re'       ],
                ['sys'      ],
            ]

classes   = [
                baseStringClass,
                listClass,
            ]

def getAll():
    return (functions, variables, modules, classes)
