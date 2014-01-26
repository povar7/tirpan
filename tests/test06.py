class X(object):
    def __init__(self, name):
        self.name = name

class A(object):
    def __init__(self):
        self.data = None

    def foo(self, flag1, flag2, flag3):
        if flag1:
            if flag2:
                self.data = X('python')
        if flag3:
            self.data = X('ruby')

    def bar(self):
        return self.data.name

a = A()
a.foo(True, False, True)
print a.bar()
