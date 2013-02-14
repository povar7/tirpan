from scope import Scope

class Configure():
    def __init__(self):
        self.load_defaults()

    def load_defaults(self):
        self.global_scope   = Scope(None)
        self.current_scope  = self.global_scope
        self.current_res    = None
        self.importer       = None
        self.verbose        = False
        self.test_results   = False
        self.test_precision = False
        self.print_imports  = False
        self.types_number   = 15

config = Configure()