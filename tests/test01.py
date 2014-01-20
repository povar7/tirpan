class X(object):
    def __init__(self, name):
        self.name = name

class A(object):
    def __init__(self):
        self.data = None

    def foo(self):
        self.data = X('python')

    def bar(self):
        return self.data.name

a = A()
a.foo()
print a.bar()
