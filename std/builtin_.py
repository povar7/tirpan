'''
Created on 05.06.2013

@author: bronikkk
'''

import ast
import types

from ti.sema import *

typeInt     = LiteralSema(int)
typeNone    = LiteralSema(types.NoneType)
typeType    = LiteralSema(type)
typeStr     = LiteralSema(str)
typeUnicode = LiteralSema(unicode)

def quasiAppend(params, **kwargs):
    if isinstance(params[0], ListSema):
        params[0].addElementsAtIndex(None, {params[1]})
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

def quasiRange1(params, **kwargs):
    return quasiRange3(params + [typeInt, typeInt])

def quasiRange3(params, **kwargs):
    if params[0] == typeInt and params[1] == typeInt and params[2] == typeInt:
        listType = ListSema(0)
        listType.addElementsAtIndex(None, {typeInt})
        return {listType}
    else:
        return set()

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
                ],
                [
                ]
            )

functions = [
                ['execfile'  , quasiExecfile, 3, {'2' : {typeNone},
                                                  '3' : {typeNone} }],
                ['range'     , quasiRange1  , 1                     ],
                ['range'     , quasiRange3  , 3, {'3' : {typeInt}}  ],
                ['type'      , quasiType    , 1                     ],
                ['unicode'   , quasiUnicode , 3, {'2' : {typeStr },
                                                  '3' : {typeStr }  }],
            ]

variables = [
                ['int'       , quasiTypeVar    ],
                ['type'      , quasiTypeVar    ],
            ]

modules   = [
                ['posixpath'],
                ['os'       ],
                ['sys'      ],
            ]

classes   = [
                baseStringClass,
                listClass,
            ]

def getAll():
    return (functions, variables, modules, classes)
