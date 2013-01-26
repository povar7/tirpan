from scope import Scope

class Timodule:
    def __init__(self, name, scope = None, path = None):
        self.name = name
        self.scope = Scope(scope)
        self.path = path
        if self.path == None:
            self.load_path()

    def load_path(self):
        import imp
        search_path = None
        file = None
        for mm in self.name.split('.'):
            (file, path, desc) = imp.find_module(mm, search_path)
            if file != None:
                search_path = path
        if file != None:
            self.path = path

    def is_buildin(self):
        return self.path == None
