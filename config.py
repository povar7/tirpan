import ti.builtin
import ti.importer
import ti.sema

class Config(object):

    def __init__(self, filename, imports):
        self.globalScope  = ti.sema.ScopeSema(None)
        self.currentScope = self.globalScope

        self.imports  = imports
        self.importer = ti.importer.Importer(filename, self)

data = None

def initialize(filename, imports):
    global data
    data = Config(filename, imports)
    importer = data.importer
    globalScope = data.globalScope
    ti.builtin.initBuiltins(importer, globalScope)
    importer.importMain(filename, data)
