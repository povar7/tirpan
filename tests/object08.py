class A:
    def __init__(self):
        self.data = None

def foo(x, y):
    x.data = y

class B:
    def __init__(self, bar):
        self.bar = bar

a = A()
b = B(a)
c = 1
foo(b.bar, c)
x = b.bar.data
print x
