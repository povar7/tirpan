import ti.builtin
import ti.importer
import ti.sema

class Config(object):

    def __init__(self, filename, imports, verbose):
        self.globalScope  = ti.sema.ScopeSema(None)
        self.currentScope = self.globalScope

        self.imports  = imports
        self.importer = ti.importer.Importer(filename, self)

        self.verbose  = verbose

data = None

def initialize(filename, imports, verbose):
    global data
    data = Config(filename, imports, verbose)
    importer = data.importer
    globalScope = data.globalScope
    ti.builtin.initBuiltins(importer, globalScope)
    importer.importMain(filename, data)
