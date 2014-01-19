class A(object):
    def __init__(self, data):
        self.data = data

class B(object):
    def __init__(self, inner):
        self.inner = inner

a = A(1)
b = B(a)
x = b.inner.data
print x
