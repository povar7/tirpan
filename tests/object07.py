class A:
    def __init__(self):
        self.data = None

class B:
    def __init__(self):
        pass

def foo(d = 1, **kwargs):
    kwargs['key1'].data = d

a1 = A()
b1 = B()
b1 = A()
foo(key1=a1, key2=b1)
x = a1.data
print x
a2 = A()
foo(3.14, key1=a2)
y = a2.data
print y
z = b1.data
print z
