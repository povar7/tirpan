class X(object):
    def __init__(self, name):
        self.name = name

class A(object):
    def __init__(self):
        self.data = None

    def foo(self, flag):
        if flag:
            self.data = X('python')

a = A()
a.foo(True)
flag = True
if flag:
    print a.data.name
