import gtk

INFO_ICON = gtk.STOCK_INFO

class WarnButton(gtk.Button):
    def __init__(self):
        gtk.Button.__init__(self)

        image = gtk.Image()
        image.set_from_stock(INFO_ICON, gtk.ICON_SIZE_MENU)
        image.show()
        self.add(image)

        self.set_relief(gtk.RELIEF_NONE)
        self.show()
        self.func = None
        self.hide()

        self.connect('button-press-event', self._button_press)

    def _button_press(self, obj, event):
        pass

warnbtn = WarnButton()
a = 1
