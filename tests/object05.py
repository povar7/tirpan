class A:
    def __init__(self):
        self.data = None

def foo(x, y):
    x.data = y

a1 = A()
a  = (a1,)
b  = 1
b  = 3.14
foo(a[0], b)
x  = a[0].data
print x

