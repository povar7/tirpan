from ti.builtin  import initBuiltins
from ti.importer import Importer
from ti.sema     import ScopeSema

class Config(object):

    def __init__(self, filename):
        self.globalScope  = ScopeSema(None)
        self.currentScope = self.globalScope

        self.importer = Importer(filename, self)

        initBuiltins(None, self.globalScope)

data = None

def initialize(filename):
    global data
    data = Config(filename)
    importer = data.importer
    importer.importMain(filename, data)
