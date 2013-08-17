import const

class PluginData(object):
    def __init__(self, id, version, fname, load_on_reg):
        self.id      = id
        self.version = version
        self.fname   = fname
        self.load_on_reg = load_on_reg

class PluginRegister(object):
    """ PluginRegister is a Singleton which holds plugin data
        .. attribute : stable_only
            Bool, include stable plugins only or not. Default True
    """
    __instance = None
    
    def get_instance():
        """ Use this function to get the instance of the PluginRegister """
        if PluginRegister.__instance is None:
            PluginRegister.__instance = 1 # Set to 1 for __init__()
            PluginRegister.__instance = PluginRegister()
        return PluginRegister.__instance
    get_instance = staticmethod(get_instance)
            
    def __init__(self):
        if PluginRegister.__instance is not 1:
            raise Exception("This class is a singleton. "
                            "Use the get_instance() method")
        self.__plugindata = []

    def add_plugindata(self, plugindata):
        self.__plugindata.append(plugindata)

    def filter_load_on_reg(self):
        """Return a list of PluginData that have load_on_reg == True
        """
        return [x.id for x in self.__plugindata if x.load_on_reg == True]

pgr1 = PluginRegister.get_instance()
pgd1 = PluginData(const.WEBSTUFF_PLUGIN_ID, '1.0',
                  const.WEBSTUFF_PYTHON_FN, True)
pgr1.add_plugindata(pgd1)
pgr2 = PluginRegister.get_instance()
pgd2 = PluginData(const.FANCHART_PLUGIN_ID, '1.0',
                  const.FANCHART_PYTHON_FN, True)
pgr2.add_plugindata(pgd2)

pgr = PluginRegister.get_instance()
x = pgr.filter_load_on_reg()
print x
