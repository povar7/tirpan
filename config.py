from ti.btrace   import BackTrace
from ti.builtin  import initBuiltins
from ti.checkers import *
from ti.importer import Importer
from ti.sema     import ScopeSema

class Config(object):

    def __init__(self, filename, imports):
        self.defectsHandler = DefectsHandler()
        self.globalScope    = ScopeSema(None)
        self.currentScope   = self.globalScope
        self.backTrace      = BackTrace() 
        self.imports        = imports
        self.importer       = Importer(filename, self)

data = None

def initialize(filename, imports):
    global data
    data = Config(filename, imports)
    importer = data.importer
    globalScope = data.globalScope
    initBuiltins(importer, globalScope)
    importer.importMain(filename, data)
