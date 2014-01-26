class X(object):
    def __init__(self, name):
        self.name = name

class A(object):
    def __init__(self):
        self.data = None

    def foo(self, flag):
        if flag:
            self.data = X('python')
        if flag:
            self.data = None

    def bar(self):
        return self.data.name

a = A()
a.foo(True)
print a.bar()
