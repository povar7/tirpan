from ti.sema import ScopeSema

class Config(object):
    def __init__(self):
        self.globalScope  = ScopeSema(None)
        self.currentScope = self.globalScope

data = None

def initialize():
     global data
     data = Config()
