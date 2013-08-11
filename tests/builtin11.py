import gtk

import const

class PluginData(object):
    def __init__(self, id):
        self.id = id

pdata = PluginData(const.REPORT_KEY)

z = []

def run_plugin(pdata):
    z.append(pdata.id)
    print pdata.id

def make_plugin_callback(pdata):
    """
    Makes a callback for a report/tool menu item
    """
    return lambda x: run_plugin(pdata)

window = gtk.Window()
window.connect('destroy', lambda w: gtk.main_quit())
window.set_title('Gramps')
window.set_size_request(200, -1)

actions = []
actions.append((const.REPORT_KEY,
                gtk.STOCK_SAVE,
                const.REPORT_MENU_NAME,
                None,
                None,
                make_plugin_callback(pdata)))

reportactions = gtk.ActionGroup('ReportWindow')
reportactions.add_actions(actions)
report_toolitem = reportactions.get_action(const.REPORT_KEY).create_tool_item()

toolbar = gtk.Toolbar()
toolbar.insert(report_toolitem, 0)

window.add(toolbar)
window.show_all()

print z
