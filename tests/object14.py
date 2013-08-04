class A(object):
    def __init__(self):
        self.__data__ = []

    def foo(self, x):
        return x

    def bar(self, x):
        self.__data__.append(x)

    def get_data(self):
        return self.__data__

class B(object):
    def __init__(self):
        self.base = A()

    def __getattr__(self, name):
        return getattr(self.base, name)

b = B()
x = b.foo(1)
print x
b.bar(3.14)
y = b.get_data()
print y
