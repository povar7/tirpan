from scope import Scope
from ast import parse
from configuration import config

class Timodule:
    def __init__(self, name, path = None):
        self.name = name
        self.scope = Scope()
        self.path = path
        if self.path is None: self.load_path()
        self.ast = None

    def load_path(self):
        import imp
        search_path = None
        file = None
        path = None
        for mm in self.name.split('.'):
            (file, path, desc) = imp.find_module(mm, search_path)
            if file is not None: search_path = path
        if file is not None: self.path = path

    def load_ast(self):
        if self.is_buildin() or self.is_ast_loaded(): return
        with open(self.path) as f:
            try:
                self.ast = parse(f.read())
            except SyntaxError as ex:
                if config.verbose: print ex.offset
                raise ex


    def is_ast_loaded(self):
        return self.ast is not None

    def is_buildin(self):
        return self.path is None
