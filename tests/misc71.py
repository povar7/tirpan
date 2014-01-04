import gtk

import const

class Dialog(gtk.Dialog):
    def __init__(self):
        gtk.Dialog.__init__(self)
        self.set_icon(None)
        self.set_icon_from_file(const.ICON)
        self.set_title('abc')

class ErrorDialog(gtk.MessageDialog):
    def __init__(self):
        gtk.MessageDialog.__init__(self)
        self.set_icon(None)
        self.set_icon_from_file(const.ICON)
        self.set_markup('')
        self.set_title('abc')

class Tooltip(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_icon(None)
        self.set_icon_from_file(const.ICON)
        self.set_title('abc')

dialog1 = Dialog()
dialog2 = ErrorDialog()
tooltip = Tooltip()
