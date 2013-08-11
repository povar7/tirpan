'''
Created on 11.08.2013

@author: bronikkk
'''

import gtk
import types

from ti.sema import *
from utils   import *

typeNone = LiteralSema(types.NoneType)

def findGtkModule():
    import config
    importer = config.data.importer
    return importer.importedFiles['gtk']

def findGtkClass(name):
    module = findGtkModule()
    var = module.getScope().findName(name)
    assert(len(var.nodeType) == 1)
    return list(var.nodeType)[0]

def quasiActionGroup(params, **kwargs):
    obj  = params[0]
    name = params[1] 
    if not hasattr(obj, '_actions'):
        obj._actions = ListSema()
    if not hasattr(obj, '_name'):
        try:
            obj._name = str(name.value)
        except AttributeError:
            obj._name = None
    return {obj}

def quasiAddActions(params, **kwargs):
    obj     = params[0]
    actions = params[1]
    for action in actions.getElements():
        if isinstance(action, TupleSema):
            obj._actions.addElementsAtIndex(None, {action})
    return {typeNone}

def quasiButton(params, **kwargs):
    obj   = params[0]
    label = params[1]
    if not hasattr(obj, '_handlers'):
        obj._handlers = ListSema()
    if not hasattr(obj, '_label'):
        try:
            obj._label = str(label.value)
        except AttributeError:
            obj._label = None
    return {obj}

def quasiConnect(scope, **kwargs):
    type1 = params[0]
    type2 = params[1]
    type3 = params[3]
    tupleType = TupleSema()
    tupleType.elems += [{type2}, {type3}]
    type1._handlers.addElementsAtIndex(None, {tupleType})
    return {typeNone}

def quasiDialog(params, **kwargs):
    obj   = params[0]
    title = params[1]
    if not hasattr(obj, '_buttons'):
        obj._buttons = ListSema()
    if not hasattr(obj, '_title'):
        try:
            obj._title = str(title.value)
        except AttributeError:
            obj._title = None
    return {obj}

def quasiAddButton(params, **kwargs):
    type1 = params[0]
    cls = findGtkClass(getButtonClassName())
    if not cls:
        return {typeNone}

    button = cls.getClassInstance()
    button._handlers = ListSema()
    button._label    = None

    type1._buttons.addElementsAtIndex(None, {button})

    return {button}

def quasiGtkMain(params, **kwargs):
    from ti.tgnode import FunctionCallTGNode, VariableTGNode

    cls = findGtkClass(getActionGroupClassName())
    if not cls:
        return {typeNone}

    funcTypes = set()
    origin = cls.origin
    for inst in origin.getInstances():
        for actionTuple in inst._actions.getElements():
            if (isinstance(actionTuple, TupleSema) and
                actionTuple.getNumberOfElements() == 6):
                actions = actionTuple.getElementsAtIndex(5)
                funcTypes |= actions

    func = QuasiNode(VariableTGNode('func', funcTypes))

    args = []
    argTypes = {typeNone}
    arg = VariableTGNode('arg1', argTypes)
    args.append(QuasiNode(arg))

    quasiCall = QuasiCall(func, args)
    FunctionCallTGNode(quasiCall)

    return {typeNone}

def quasiRun(params, **kwargs):
    return {typeNone}

def quasiResponseOk():
    return {LiteralValueSema(gtk.RESPONSE_OK)}

def quasiStockOk():
    return {LiteralValueSema(gtk.STOCK_OK)}

functions = [
                ['main', quasiGtkMain, 0],
            ]

variables = [
                ['RESPONSE_OK', quasiResponseOk],
                ['STOCK_OK'   , quasiStockOk   ],
            ]

modules   = [
            ]

def getActionGroupClassName():
    return 'ActionGroup'

actionGroupClass = (
                       getActionGroupClassName(),
                       [
                           ['__init__'   , quasiActionGroup, 2],
                           ['add_actions', quasiAddActions , 2],
                       ],
                       [
                       ],
                       True
                   )

def getButtonClassName():
    return 'Button'

buttonClass = (
                  getButtonClassName(),
                  [
                      ['__init__', quasiButton , 2],
                      ['connect' , quasiConnect, 3],
                  ],
                  [
                  ]
              )

def getDialogClassName():
    return 'Dialog'

dialogClass = (
                  getDialogClassName(),
                  [
                      ['__init__'  , quasiDialog   , 2],
                      ['add_button', quasiAddButton, 3],
                      ['run'       , quasiRun      , 1],
                  ],
                  [
                  ]
              )

classes = [
              actionGroupClass,
              buttonClass,
              dialogClass
          ]

def getAll():
    return (functions, variables, modules, classes)
