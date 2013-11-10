'''
Created on 11.08.2013

@author: bronikkk
'''

import gtk
import types

from ti.lookup import *
from ti.sema   import *
from utils     import *

typeNone = LiteralSema(types.NoneType)

def findGtkModule():
    import config
    importer = config.data.importer
    return importer.importedFiles['gtk']

def findGtkName(name):
    module = findGtkModule()
    var = module.getScope().findName(name)
    assert len(var.nodeType) == 1
    return list(var.nodeType)[0]

def quasiActionGroup(params, **kwargs):
    obj = params[0]
    var = lookupVariable(obj, '_actions', True, True)
    if var:
        var.nodeType = {ListSema()}
    return {obj}

def quasiAddActions(params, **kwargs):
    obj = params[0]
    var = lookupVariable(obj, '_actions')
    if not var:
        return {typeNone}
    assert len(var.nodeType) == 1
    actions = list(var.nodeType)[0]
    for action in params[1].getElements():
        if isinstance(action, TupleSema):
            actions.addElementsAtIndex(None, {action})
    return {typeNone}

def quasiButton(params, **kwargs):
    obj = params[0]
    var = lookupVariable(obj, '_handlers', True, True)
    if var:
        var.nodeType = {ListSema()}
    return {obj}

def quasiConnect(params, **kwargs):
    obj = params[0]
    var = lookupVariable(obj, '_handlers')
    if not var:
        return {typeNone}
    assert len(var.nodeType) == 1
    handlers = list(var.nodeType)[0] 
    tupleType = TupleSema()
    tupleType.elems += [{params[1]}, {params[2]}]
    handlers.addElementsAtIndex(None, {tupleType})
    return {typeNone}

def quasiDialog(params, **kwargs):
    obj = params[0]
    var = lookupVariable(obj, '_buttons', True, True)
    if var:
        var.nodeType = {ListSema()}
    return {obj}

def quasiAddButton(params, **kwargs):
    obj = params[0]
    cls = findGtkName(getButtonClassName())
    if not cls:
        return {typeNone}

    button = cls.getClassInstance()
    
    var1 = lookupVariable(button, '_handlers', True, True)
    if not var1:
        return {button}
    var1.nodeType = {ListSema()}

    var2 = lookupVariable(obj, '_buttons')
    if not var2:
        return {button}
    assert len(var2.nodeType) == 1
    buttons = list(var2.nodeType)[0]
    buttons.addElementsAtIndex(None, {button})

    return {button}

def quasiGtkMain(params, **kwargs):
    from ti.tgnode import FunctionCallTGNode, VariableTGNode

    cls = findGtkName(getActionGroupClassName())
    if not cls:
        return {typeNone}

    funcTypes = set()

    origin = cls.origin
    for inst in origin.getInstances():
        var = lookupVariable(inst, '_actions')
        if not var:
            continue
        assert len(var.nodeType) == 1
        actions = list(var.nodeType)[0]
        for actionTuple in actions.getElements():
            if (isinstance(actionTuple, TupleSema) and
                actionTuple.getNumberOfElements() == 6):
                callbacks  = actionTuple.getElementsAtIndex(5)
                funcTypes |= callbacks

    func = QuasiNode(VariableTGNode('func', funcTypes))

    args = []
    argTypes = {typeNone}
    arg = VariableTGNode('arg1', argTypes)
    args.append(QuasiNode(arg))

    node = kwargs['NODE']
    quasiCall = QuasiCall(func, args, node)
    FunctionCallTGNode(quasiCall)

    return {typeNone}

def quasiRun(params, **kwargs):
    from ti.tgnode import FunctionCallTGNode, VariableTGNode

    obj = params[0]

    var1 = lookupVariable(obj, '_buttons')
    if not var1:
        return {typeNone}
    assert len(var1.nodeType) == 1
    buttons = list(var1.nodeType)[0]

    funcTypes = set()

    for button in buttons.getElements():
        var2 = lookupVariable(button, '_handlers')
        if not var2:
            continue
        assert len(var2.nodeType) == 1
        handlers = list(var2.nodeType)[0]
        for handler in handlers.getElements():
            callbacks = handler.getElementsAtIndex(1)
            funcTypes |= callbacks

    func = QuasiNode(VariableTGNode('func', funcTypes))

    args = []
    argTypes = {typeNone}
    arg = VariableTGNode('arg1', argTypes)
    args.append(QuasiNode(arg))

    node = kwargs['NODE']
    quasiCall = QuasiCall(func, args, node)
    FunctionCallTGNode(quasiCall)

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
