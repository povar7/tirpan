'''
Created on 28.08.2013

@author: bronikkk
'''

from ti.sema import *

typeNone = LiteralSema(types.NoneType)

def findGettextModule():
    import config
    importer = config.data.importer
    return importer.importedFiles['gettext']

def findGettextName(name):
    module = findGettextModule()
    var = module.getScope().findName(name)
    assert len(var.nodeType) == 1
    return list(var.nodeType)[0]

def quasiGettext(params, **kwargs):
    res = params[0]
    return {res}

def quasiGettextMethod(params, **kwargs):
    return quasiGettext(params[1:], **kwargs)

def quasiTranslation(params, **kwargs):
    return set()

nullTranslationsClassName = 'NullTranslations'

def getNullTranslationsClassName():
    return nullTranslationsClassName

nullTranslationsClass = (
                            nullTranslationsClassName,
                            [
                                ['gettext', quasiGettextMethod, 2],
                            ],
                            [
                            ]
                        )

functions = [
                ['gettext'    , quasiGettext    , 1],
                ['translation', quasiTranslation, 6, {'2' : {typeNone},
                                                      '3' : {typeNone},
                                                      '4' : {typeNone},
                                                      '5' : {typeNone},
                                                      '6' : {typeNone} }],
            ]

variables = [
            ]

modules   = [
            ]

classes   = [
                nullTranslationsClass,
            ]

def getAll():
    return (functions, variables, modules, classes)
