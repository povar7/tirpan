import gtk

class A(gtk.ComboBox):
    def __init__(self):
        gtk.ComboBox.__init__(self)
        self.set_active(0)
        self.data = [3.14]

    def get_data(self):
        return self.data[self.get_active()]

a = A()
x = a.get_data()
print x
