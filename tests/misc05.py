class A:
    def __init__(self):
        self.link = None

class B:
    def __init__(self, a):
        self.link = a
        a.link = self

def foo(x):
    return x

a = A()
b = B(a)
c = foo(b)
d = 1

