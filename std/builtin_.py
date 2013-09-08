'''
Created on 05.06.2013

@author: bronikkk
'''

import ast
import copy
import itertools
import sys
import types
import utils

import config

from ti.function import makeSet, Flags
from ti.lookup   import *
from ti.sema     import *

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
        if params[1] is None:
            return {typeNone}
        params[0].addElementsAtIndex(None, {params[1]})
        flags = kwargs['FLAGS']
        flags.setDestructive()
    return {typeNone}

def quasiExtend(params, **kwargs):
    if (isinstance(params[0], ListSema) and
        isinstance(params[1], ListSema)):
        elements = params[1].getElements()
        params[0].addElementsAtIndex(None, elements)
        flags = kwargs['FLAGS']
        flags.setDestructive()
    return {typeNone}

def quasiInsert(params, **kwargs):
    if isinstance(params[0], ListSema):
        if params[2] is None:
            return {typeNone}
        params[0].addElementsAtIndex(None, {params[2]})
        flags = kwargs['FLAGS']
        flags.setDestructive()
    return {typeNone}

def quasiEncode(params, **kwargs):
    res = params[0]
    return {res}

class ExecutedFiles(object):

    def __init__(self):
        self._files = set()

    def addFile(self, filename, node):
        key = (unicode(filename), node)
        self._files.add(key)

    def hasFile(self, filename, node):
        key = (unicode(filename), node)
        return key in self._files

executedFiles = ExecutedFiles()

def quasiExecfile(params, **kwargs):
    filename = getattr(params[0], 'value', None)
    if filename is not None:
        import config
        from ti.parser import Parser
        from ti.tgnode import VariableTGNode, UsualModuleTGNode
        node = kwargs['NODE']
        if executedFiles.hasFile(filename, node):
            return {typeNone}
        else:
            executedFiles.addFile(filename, node)
        try:
            parser = Parser(filename)
            tree   = parser.getAST()
        except IOError:
            return {typeNone}
        importer  = config.data.importer
        oldNumber = node.fileno
        oldScope  = importer.getFileScope(oldNumber) 
        module    = UsualModuleTGNode(tree, filename, None, oldScope)
        newNumber = importer.putIdent(module)
        if config.data.imports:
            print >> sys.stderr, '%d\t%s' % (newNumber, module.name)
        tree.link = module
        ourGlobals = params[1]
        save = config.data.currentScope
        newScope = ScopeSema(save)
        config.data.currentScope = newScope
        if isinstance(ourGlobals, DictSema):
            for key, value in ourGlobals.elems.items():
                if (isinstance(key, LiteralValueSema) and
                    isinstance(key.value, str)):
                    valueCopy = value.copy()
                    var = VariableTGNode(key.value, valueCopy)
                    newScope.addVariable(var)
        for node in ast.walk(tree):
            node.fileno = newNumber
        parser.walk()
        config.data.currentScope = save
    return {typeNone}

def quasiImport(params, **kwargs):
    filename = getattr(params[0], 'value', None)
    node = kwargs['NODE']
    origin = utils.getFileName(node)
    if filename is not None and origin is not None:
        try:
            importer = config.data.importer
            quasiAlias = QuasiAlias(filename)
            module = importer.importFile(origin, quasiAlias)
            res = module.getScope()
            return {res}
        except:
            pass
    return set()

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
    except TypeError:
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
    return makeSet(param)

def quasiStrip(params, **kwargs):
    param = params[0]
    res   = None
    try:
        res = LiteralValueSema(param.value.strip())
    except:
        pass
    return makeSet(res)

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

def quasiUpdate(params, **kwargs):
    if (isinstance(params[0], DictSema) and
        isinstance(params[1], DictSema)):
        for key, values in params[1].elems.items():
            params[0].addElementsAtKey(key, values)
        flags = kwargs['FLAGS']
        flags.setDestructive()
    return {typeNone}

def quasiObjectClassBases():
    res = TupleSema()
    return {res}

baseStringClassName = str(basestring)

def getBaseStringClassName():
    return baseStringClassName

baseStringClass = (
                      baseStringClassName,
                      [
                          ['encode', quasiEncode, 2],
                          ['strip' , quasiStrip , 1],
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

dictClassName = str(type({}))

def getDictClassName():
    return dictClassName

dictClass = (
                dictClassName,
                [
                    ['update', quasiUpdate, 2],
                ],
                [
                ]
            )

objectClassName = 'object'

def getObjectClassName():
    return objectClassName

objectClass = (
                  objectClassName,
                  [
                  ],
                  [
                      ['__bases__', quasiObjectClassBases],
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
            added = None

            try:
                tmp   = tuple([elem.value for elem in atom])
                part  = left.value % tmp
                added = LiteralValueSema(part) 
            except:
                pass

            if added:
                res.add(added)
                continue

            try:
                part  = left.value % ()
                added = LiteralValueSema(part)
            except:
                pass

            if added:
                res.add(added)
                continue
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
    if isinstance(oper, LiteralSema) and oper.ltype == int:
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

                ['__import__', quasiImport  , 1                     ],

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

                ['copy'     ],
                ['getopt'   ],
                ['gettext'  ],
                ['glib'     ],
                ['glob'     ],
                ['gtk'      ],
                ['logging'  ],
                ['os'       ],
                ['pickle'   ],
                ['re'       ],
                ['sys'      ],
                ['urllib'   ],

                ['ConfigParser'],
            ]

classes   = [
                baseStringClass,
                listClass,
                dictClass,
                objectClass,
            ]

def getAll():
    return (functions, variables, modules, classes)
