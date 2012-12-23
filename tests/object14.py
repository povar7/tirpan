class A(object):
    def foo(self, x):
        return x

class B(object):
    def __init__(self):
        self.base = A()

    def __getattr__(self, name):
        return getattr(self.base, name)

b = B()
x = b.foo(3)
print x
