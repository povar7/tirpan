class X(object):

    def setName(self, name):
        self.name = name

class Y(object):

    def setName(self, name):
        pass

flag = True
if flag:
    a = X()
else:
    a = Y()
a.setName('abc')
print a.name
