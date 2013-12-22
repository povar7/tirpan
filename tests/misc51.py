import os

def foo(filename):
    os.path.basename(filename)

class A:
    def __init__(self):
        self.open = None

    def bar(self):
        self.open = 'abc'
        if self.open:
            foo(self.open)

a = A()
a.bar()
