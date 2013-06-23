class A:
    def __init__(self):
        self.data = None

def foo(x, y):
    x.data = y

a1 = A()
a2 = A()
a3 = A()
b  = 1
b  = 3.14
c  = 'str'
foo(a1, b)
foo(a2, b)
foo(a3, c)
d1 = a1.data
d2 = a2.data
d3 = a3.data
