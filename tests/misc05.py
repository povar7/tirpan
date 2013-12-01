class A:
    def __init__(self):
        self.ref = None

class B:
    def __init__(self, a):
        self.ref = a
        a.ref = self

def foo(x):
    return x

a = A()
b = B(a)
c = foo(b)
d = 1
