class X(object):

    def __init__(self):
        self.data = Z('abc')

    def bar(self):
        return self.data.name

class Y(object):

    def __init__(self):
        self.data = None

class Z(object):
    
    def __init__(self, name):
        self.name = name

flag1 = True
if flag1:
    a = X()
else:
    a = Y()
flag2 = True
if flag2:
    print a.data.name
