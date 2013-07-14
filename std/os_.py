'''
Created on 06.07.2013

@author: bronikkk
'''

def quasiPath():
    import config
    importer = config.data.importer
    res = set()
    try:
        module = importer.importedFiles['posixpath']
    except KeyError:
        return res
    res |= module.nodeType
    return res

functions = [ 
            ]

variables = [
                ['path', quasiPath], 
            ]

modules   = [
            ]

objects   = [
            ]

def getAll():
    return (functions, variables, modules, objects)
