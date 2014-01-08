import gtk

import const

class Dialog(gtk.Dialog):
    def __init__(self):
        gtk.Dialog.__init__(self)
        self.connect('delete-event', self.close)
        self.set_default_size(600, -1)
        self.set_modal(True)
        self.set_has_separator(False)
        self.get_size()
        self.set_transient_for(None)
        self.set_icon(None)
        self.set_icon_from_file(const.ICON)
        self.set_title('abc')
        vbox = self.vbox
        self.show_all()
        self.destroy()

    def close(self):
        pass

class ErrorDialog(gtk.MessageDialog):
    def __init__(self):
        gtk.MessageDialog.__init__(self)
        self.set_icon(None)
        self.set_icon_from_file(const.ICON)
        self.set_markup('')
        self.set_title('abc')
        self.format_secondary_markup('')
        self.format_secondary_text('')
        self.show()
        self.run()
        self.destroy()

class GrampsAboutDialog(gtk.AboutDialog):
    def __init__(self):
        gtk.AboutDialog.__init__(self)
        self.set_artists([])
        self.set_authors([])
        self.set_comments('')
        self.set_copyright('')
        self.set_documenters([])
        self.set_license('')
        self.set_logo(None)
        self.set_modal(True)
        self.set_name('')
        self.set_transient_for(None)
        self.set_translator_credits('')
        self.set_version('')
        self.set_website('')
        self.set_website_label('')
        self.run()
        self.destroy()

class FileEntry(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self)
        self.set_sensitive(True)
        self.set_spacing(6)
        self.set_homogeneous(False)
        button1 = gtk.Button()
        button2 = gtk.Button()
        self.pack_start(button1, True, True)
        self.pack_end(button2, False, False)
        self.show_all()

class Tooltip(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_icon(None)
        self.set_icon_from_file(const.ICON)
        self.set_title('abc')

class GrampsBar(gtk.Notebook):
    def __init__(self):
        gtk.Notebook.__init__(self)
        self.set_group_id(1)
        self.set_show_border(False)
        self.set_show_tabs(False)
        self.set_scrollable(True)
        self.connect('button-press-event', self.__button_press)
        self.get_property('visible')
        self.set_current_page(0)
        widget1 = gtk.VBox()
        widget2 = gtk.VBox()
        self.append_page(widget1, None)
        self.insert_page(widget2, None, 0)
        self.remove_page(0)
        self.set_border_width(6)
        self.get_n_pages()
        self.get_current_page()
        self.show()
        self.destroy()

    def __button_press(self, widget, event):
        pass

class PaperComboBox(gtk.ComboBox):
    def __init__(self):
        gtk.ComboBox.__init__(self)
        cell = gtk.CellRendererText()
        self.connect('changed', self.size_changed)
        self.set_active(0)
        self.set_model(None)
        self.pack_start(cell, True)
        self.add_attribute(cell, 'text', 0)

    def size_changed(self, obj):
        pass

class ManagedWindow(object):
    pass

class ExportAssistant(gtk.Assistant, ManagedWindow):
    def __init__(self):
        gtk.Assistant.__init__(self)
        page = gtk.Label()
        self.append_page(page)
        self.connect('delete-event', self.close)
        self.set_forward_page_func(self.forward_func, None)
        self.set_icon_from_file(const.ICON)
        self.set_page_complete(page, True)
        self.set_page_header_image(page, None)
        self.set_page_side_image(page, None)
        self.set_page_title(page, '')
        self.set_page_type(page, gtk.ASSISTANT_PAGE_INTRO)
        self.set_title('')
        self.set_transient_for(None)
        self.show_all()
        self.destroy()

    def forward_func(self, pagenumber, data):
        return pagenumber + 1

    def close(self):
        pass

class Foo1(gtk.ActionGroup):
    def __init__(self):
        gtk.ActionGroup.__init__(self, 'foo1')
        self.add_toggle_actions([])
        self.set_visible(True)
        self.set_sensitive(True)
        self.get_action('ConfigView')

class WarnButton(gtk.Button):
    def __init__(self):
        gtk.Button.__init__(self)
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_INFO, gtk.ICON_SIZE_MENU)
        image.show()
        self.add(image)
        self.set_relief(gtk.RELIEF_NONE)
        self.set_sensitive(True)
        self.show()
        self.hide()

class ScratchPadListModel(gtk.ListStore):
    def __init__(self):
        gtk.ListStore.__init__(self, int)
        self.connect('row-inserted', self.row_inserted)
        self.clear()

    def row_inserted(self):
        pass

dialog1 = Dialog()
dialog2 = ErrorDialog()
dialog3 = GrampsAboutDialog()
entry   = FileEntry()
lmodel  = ScratchPadListModel()
tooltip = Tooltip()
pcbox   = PaperComboBox()
bar     = GrampsBar()
export  = ExportAssistant()
wbutton = WarnButton()
foo1    = Foo1()
