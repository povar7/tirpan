'''
Created on 11.08.2013

@author: bronikkk
'''

import types

from ti.lookup import *
from ti.sema   import *
from utils     import *

typeInt  = LiteralSema(int)
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

def quasi_cons(params, **kwargs):
    return {params[0]}

def quasi_none(params, **kwargs):
    return {typeNone}

def quasi_zero(params, **kwargs):
    return set()

def quasi_zero_var():
    return set()

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

def quasiGetActive(params, **kwargs):
    return {typeInt}

def quasiGtkMain(params, **kwargs):
    import config
    from ti.tgnode import FunctionCallTGNode, VariableTGNode

    cls = findGtkName(getActionGroupClassName())
    if not cls:
        return {typeNone}

    funcTypes = set()

    origin = cls.getOrigin()
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

    tgNode = kwargs['TGNODE']
    node = tgNode.node
    quasiCall = QuasiCall(func, args, node)
    link = FunctionCallTGNode(quasiCall)
    setLink(quasiCall, link)
    kwargs['CALLS'].append((config.data.currentScope, tgNode, quasiCall))

    return {typeNone}

def quasiNewText(params, **kwargs):
    cls = findGtkName(getComboBoxClassName())
    if not cls:
        return set()
    obj = cls.getClassInstance()
    return {obj}

def quasiRun(params, **kwargs):
    import config
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

    tgNode = kwargs['TGNODE']
    node = tgNode.node
    quasiCall = QuasiCall(func, args, node)
    link = FunctionCallTGNode(quasiCall)
    setLink(quasiCall, link)
    kwargs['CALLS'].append((config.data.currentScope, tgNode, quasiCall))

    return {typeNone}

def quasiResponseOk():
    return {typeInt}

def quasiStockOk():
    return {typeInt}

functions = [
                ['combo_box_new_text', quasiNewText, 0],
                ['main'              , quasiGtkMain, 0],
            ]

variables = [
                ['RESPONSE_OK', quasiResponseOk],
                ['STOCK_OK'   , quasiStockOk   ],
            ]

modules   = [
            ]

def getAboutDialogClassName():
    return 'AboutDialog'

aboutDialogClass = (
                       getAboutDialogClassName(),
                       [
                           ['__init__'              , quasi_cons, 2],
                           ['destroy'               , quasi_none, 1],
                           ['run'                   , quasi_none, 1],
                           ['set_authors'           , quasi_none, 2],
                           ['set_artists'           , quasi_none, 2],
                           ['set_comments'          , quasi_none, 2],
                           ['set_copyright'         , quasi_none, 2],
                           ['set_documenters'       , quasi_none, 2],
                           ['set_license'           , quasi_none, 2],
                           ['set_logo'              , quasi_none, 2],
                           ['set_modal'             , quasi_none, 2],
                           ['set_name'              , quasi_none, 2],
                           ['set_transient_for'     , quasi_none, 2],
                           ['set_translator_credits', quasi_none, 2],
                           ['set_version'           , quasi_none, 2],
                           ['set_website'           , quasi_none, 2],
                           ['set_website_label'     , quasi_none, 2],
                       ],
                       [
                       ]
                   )

def getActionGroupClassName():
    return 'ActionGroup'

actionGroupClass = (
                       getActionGroupClassName(),
                       [
                           ['__init__'   , quasiActionGroup, 2],
                           ['add_actions', quasiAddActions , 2],
                           ['set_visible', quasi_none      , 2],
                       ],
                       [
                       ],
                       True
                   )

def getAssistantClassName():
    return 'Assistant'

assistantClass = (
                     getAssistantClassName(),
                     [
                         ['__init__'             , quasi_cons, 2],
                         ['append_page'          , quasi_none, 2],
                         ['connect'              , quasi_none, 3],
                         ['destroy'              , quasi_none, 1],
                         ['set_forward_page_func', quasi_none, 3],
                         ['set_icon_from_file'   , quasi_none, 2],
                         ['set_page_complete'    , quasi_none, 3],
                         ['set_page_header_image', quasi_none, 3],
                         ['set_page_side_image'  , quasi_none, 3],
                         ['set_page_title'       , quasi_none, 3],
                         ['set_page_type'        , quasi_none, 3],
                         ['set_title'            , quasi_none, 2],
                         ['set_transient_for'    , quasi_none, 2],
                         ['show_all'             , quasi_none, 1],
                     ],
                     [
                     ]
                 )

def getButtonClassName():
    return 'Button'

buttonClass = (
                  getButtonClassName(),
                  [
                      ['__init__'     , quasiButton , 2],
                      ['add'          , quasi_none  , 2],
                      ['connect'      , quasiConnect, 3],
                      ['hide'         , quasi_none  , 1],
                      ['set_relief'   , quasi_none  , 2],
                      ['set_sensitive', quasi_none  , 2],
                      ['show'         , quasi_none  , 1],
                  ],
                  [
                  ]
              )

def getDialogClassName():
    return 'Dialog'

dialogClass = (
                  getDialogClassName(),
                  [
                      ['__init__'          , quasiDialog   , 2],
                      ['add_button'        , quasiAddButton, 3],
                      ['connect'           , quasi_none    , 3],
                      ['destroy'           , quasi_none    , 1],
                      ['get_size'          , quasi_zero    , 1],
                      ['run'               , quasiRun      , 1],
                      ['set_default_size'  , quasi_none    , 3],
                      ['set_has_separator' , quasi_none    , 2],
                      ['set_icon'          , quasi_none    , 2],
                      ['set_icon_from_file', quasi_none    , 2],
                      ['set_modal'         , quasi_none    , 2],
                      ['set_title'         , quasi_none    , 2],
                      ['set_transient_for' , quasi_none    , 2],
                      ['show_all'          , quasi_none    , 1],
                  ],
                  [
                      ['vbox', quasi_zero_var],
                  ]
              )

def getHBoxClassName():
    return 'HBox'

hboxClass = (
                getHBoxClassName(),
                [
                    ['__init__'       , quasi_cons, 1],
                    ['pack_end'       , quasi_none, 4],
                    ['pack_start'     , quasi_none, 4],
                    ['set_homogeneous', quasi_none, 2],
                    ['set_sensitive'  , quasi_none, 2],
                    ['set_spacing'    , quasi_none, 2],
                    ['show_all'       , quasi_none, 1],
                ],
                [
                ]
            )

def getComboBoxClassName():
    return 'ComboBox'

comboBoxClass = (
                    getComboBoxClassName(),
                    [
                        ['__init__'     , quasi_cons    , 1],
                        ['add_attribute', quasi_none    , 4],
                        ['connect'      , quasi_none    , 3],
                        ['get_active'   , quasiGetActive, 1],
                        ['pack_start'   , quasi_none    , 3],
                        ['set_active'   , quasi_none    , 2],
                        ['set_model'    , quasi_none    , 2],
                    ],
                    [
                    ]
                )

def getMessageDialogClassName():
    return 'MessageDialog'

messageDialogClass = (
                         getMessageDialogClassName(),
                         [
                             ['__init__'               , quasi_cons, 1],
                             ['destroy'                , quasi_none, 1],
                             ['format_secondary_markup', quasi_none, 2],
                             ['format_secondary_text'  , quasi_none, 2],
                             ['set_icon'               , quasi_none, 2],
                             ['set_icon_from_file'     , quasi_none, 2],
                             ['set_markup'             , quasi_none, 2],
                             ['set_title'              , quasi_none, 2],
                             ['show'                   , quasi_none, 1],
                             ['run'                    , quasi_none, 1],
                         ],
                         [
                         ]
                     )

def getNotebookClassName():
    return 'Notebook'

notebookClass = (
                    getNotebookClassName(),
                    [
                        ['__init__'        , quasi_cons, 1],
                        ['append_page'     , quasi_none, 3],
                        ['connect'         , quasi_none, 3],
                        ['destroy'         , quasi_none, 1],
                        ['get_current_page', quasi_zero, 1],
                        ['get_n_pages'     , quasi_zero, 1],
                        ['get_property'    , quasi_zero, 2],
                        ['insert_page'     , quasi_none, 4],
                        ['remove_page'     , quasi_none, 2],
                        ['set_border_width', quasi_none, 2],
                        ['set_current_page', quasi_none, 2],
                        ['set_group_id'    , quasi_none, 2],
                        ['set_scrollable'  , quasi_none, 2],
                        ['set_show_border' , quasi_none, 2],
                        ['set_show_tabs'   , quasi_none, 2],
                        ['show'            , quasi_none, 1],
                    ],
                    [
                    ]
                )

def getWindowClassName():
    return 'Window'

windowClass = (
                  getWindowClassName(),
                  [
                      ['__init__'          , quasi_cons, 1],
                      ['set_icon'          , quasi_none, 2],
                      ['set_icon_from_file', quasi_none, 2],
                      ['set_title'         , quasi_none, 2],
                  ],
                  [
                  ]
              )

classes = [
              aboutDialogClass,
              actionGroupClass,
              assistantClass,
              buttonClass,
              comboBoxClass,
              dialogClass,
              hboxClass,
              messageDialogClass,
              notebookClass,
              windowClass,
          ]

def getAll():
    return (functions, variables, modules, classes)
