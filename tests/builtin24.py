import gtk

class A():
    def __init__(self):
        self.css_combo = gtk.combo_box_new_text()
        self.data = [3.14]
        self.set_combo()

    def set_combo(self):
        self.css_combo.set_active(0)

    def get_data(self):
        return self.data[self.css_combo.get_active()]

a = A()
x = a.get_data()
print x
