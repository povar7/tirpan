class A(object):
    def __init__(self, x, y):
        self.__data = (x, y)

    def get_data(self):
        return self.__data

class B(object):
    def __init__(self):
        self.format = A
        self.doc    = None

    def foo(self, x, y):
        self.doc    = self.format(x, y)
        return self.doc.get_data()

b = B()
x = b.foo(1, 3.14)
print x
