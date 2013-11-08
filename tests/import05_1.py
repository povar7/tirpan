import import05_2 as locale

locale.foo()

class A:
    def __init__(self):
        self.data = None

    def foo(self, data):
        self.data = data

if True:
    locale = A()
locale.foo(6.28)
x = locale.data
print x
