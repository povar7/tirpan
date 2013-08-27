import const

GENERAL = 6
VIEW    = 8

class PluginData(object):
    pass

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
        plugins = self.__plugindata
        plugins.append(plugindata)

    def filter_load_on_reg(self):
        """Return a list of PluginData that have load_on_reg == True
        """
        return [x.id for x in self.__plugindata if x.load_on_reg == True]

def newplugin():
    gpr = PluginRegister.get_instance()
    pgd = PluginData()
    gpr.add_plugindata(pgd)
    return pgd

def register(ptype, **kwargs):
    plg = newplugin()
    plg.ptype = ptype
    for prop in kwargs:
        setattr(plg, prop, kwargs[prop])
    return plg

register(GENERAL,
         id=const.WEBSTUFF_PLUGIN_ID, version='1.0',
         fname=const.WEBSTUFF_PYTHON_FN, load_on_reg=True)
register(VIEW,
         id=const.FANCHART_PLUGIN_ID, version='1.0',
         fname=const.FANCHART_PYTHON_FN, load_on_reg=False)

pgr = PluginRegister.get_instance()
x = pgr.filter_load_on_reg()
print x
