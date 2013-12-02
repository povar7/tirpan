'''
Created on 02.12.2013

@author: bronikkk
'''

def quasiTimeoutAdd():
    import config
    importer = config.data.importer
    module = None
    res = set()
    try:
        module = importer.importedFiles['glib']
    except KeyError:
        pass
    try:
        var = module.getScope().findName('timeout_add')
        res |= var.nodeType
    except AttributeError:
        pass
    return res

functions = [
            ]

variables = [
                ['timeout_add', quasiTimeoutAdd], 
            ]

modules   = [
            ]

classes   = [
            ]

def getAll():
    return (functions, variables, modules, classes)
