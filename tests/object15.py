class A(object):
    def __init__(self):
        self.data = 1

class B(object):
    def __init__(self):
        self.data = 3.14

    def foo(self):
        return self.data

a = A()
b = B()
c = a
c = b
x = c.foo()
print x
