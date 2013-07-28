import const

class PluginData(object):
    def __init__(self, id, version, fname, load_on_reg):
        self.id      = id
        self.version = version
        self.fname   = fname
        self.load_on_reg = load_on_reg

class PluginRegister(object):
    def __init__(self):
        self.__plugindata = []

    def add_plugindata(self, plugindata):
        self.__plugindata.append(plugindata)

    def filter_load_on_reg(self):
        """Return a list of PluginData that have load_on_reg == True
        """
        return [x.id for x in self.__plugindata if x.load_on_reg == True]

pgr = PluginRegister()
pgd = PluginData(const.WEBSTUFF_PLUGIN_ID, '1.0', 'webstuff.py', True)
pgr.add_plugindata(pgd)
y = pgr.filter_load_on_reg()
print y
