import const

class A:
    def __init__(self, x):
        setattr(self, const.X, x)

    def foo(self):
        return self.x

a1 = A(1)
x  = a1.foo()
a2 = A(3.14)
y  = a2.foo()
print x
print y
