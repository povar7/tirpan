import ti.builtin
import ti.importer
import ti.sema

class Config(object):

    def __init__(self, filename, **params):
        self.filename = filename  # File name is required

        # Defaults
        self.print_mir = False
        self.mir_only = False
        self.verbose = False
        self.print_imports = False

        # Passed parameters
        for name, value in params.items():
            setattr(self, name, value)

        # Process passed
        if self.verbose:
            self.print_mir = self.print_imports = True
        if self.mir_only:
            self.print_mir = True

        # Other initialization
        self.globalScope  = ti.sema.ScopeSema(None)
        self.currentScope = self.globalScope

        self.importer = ti.importer.Importer(filename, self)

data = None

def initialize(filename, **params):
    global data
    data = Config(filename, **params)
    importer = data.importer
    globalScope = data.globalScope
    ti.builtin.initBuiltins(importer, globalScope)
    importer.importMain(filename, data)
