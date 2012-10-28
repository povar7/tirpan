class CLIManager:
    data = True
    def __init__(self, data1):
        self.data1 = data1

class ViewManager(CLIManager):
    def __init__(self, data1, data2):
        CLIManager.__init__(self, data1)
        self.data2 = data2

a = 1
b = 3.14
c = ViewManager(a, b)
x = c.data1
print x
y = c.data2
print y
z = c.data
print z

