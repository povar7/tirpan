_ = unicode

#-------------------------------------------------------------------------
#
# PluginData
#
#-------------------------------------------------------------------------

#a plugin is stable or unstable
STABLE   = 0
UNSTABLE = 1
#possible plugin types
REPORT  = 0
QUICKREPORT = 1 # deprecated
QUICKVIEW   = 1
TOOL        = 2
IMPORT      = 3
EXPORT      = 4
DOCGEN      = 5
GENERAL     = 6
MAPSERVICE  = 7
VIEW        = 8
RELCALC     = 9
GRAMPLET    = 10
SIDEBAR     = 11
PTYPE       = [REPORT , QUICKREPORT, TOOL, IMPORT, EXPORT, DOCGEN, GENERAL,
               MAPSERVICE, VIEW, RELCALC, GRAMPLET, SIDEBAR]

#possible report categories
CATEGORY_TEXT = 0

# Modes for generating reports
REPORT_MODE_GUI = 1    # Standalone report using GUI

#-------------------------------------------------------------------------
#
# Functions and classes
#
#-------------------------------------------------------------------------
def myint(s):
    """
    Protected version of int()
    """
    try:
        v = int(s)
    except:
        v = s
    return v

def version(sversion):
    """
    Return the tuple version of a string version.
    """
    return tuple([myint(x or "0") for x in (sversion + "..").split(".")])

class PluginData(object):
    def __init__(self):
        self.authors               = []
        self.authors_email         = []
        self._category             = None
        self.description           = None
        self.fname                 = None
        self.gramps_target_version = None
        self._id                   = None
        self.load_on_reg           = False
        self._name                 = None
        self.optionclass           = None
        self.process               = None
        self._ptype                = None
        self.reportclass           = None
        self.report_modes          = [REPORT_MODE_GUI]
        self.require_active        = True
        self.status                = UNSTABLE
        self.version               = None

    #REPORT or TOOL or QUICKREPORT or GENERAL attributes
    def _set_category(self, category):
        if self._ptype not in [REPORT, TOOL, QUICKREPORT, VIEW, GENERAL]:
            raise ValueError, 'category may only be set for ' \
                              'REPORT/TOOL/QUICKREPORT/VIEW/GENERAL plugins'
        self._category = category

    def _get_category(self):
        return self._category

    def _set_id(self, id):
        self._id = id

    def _get_id(self):
        return self._id

    def _set_name(self, name):
        self._name = name

    def _get_name(self):
        return self._name

    def _set_ptype(self, ptype):
        if ptype not in PTYPE:
            raise ValueError, 'Plugin type cannot be %s' % str(ptype)
        elif self._ptype is not None:
            raise ValueError, 'Plugin type may not be changed'
        self._ptype = ptype
        if self._ptype == REPORT:
            self._category = CATEGORY_TEXT
        elif self._ptype == TOOL:
            self._category = TOOL_UTILS
        elif self._ptype == QUICKREPORT:
            self._category = CATEGORY_QR_PERSON
        elif self._ptype == VIEW:
            self._category = ("Miscellaneous", _("Miscellaneous"))

    def _get_ptype(self):
        return self._ptype

    category = property(_get_category, _set_category)
    id = property(_get_id, _set_id)
    name = property(_get_name, _set_name)
    ptype = property(_get_ptype, _set_ptype)

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
        self.__plugindata = []

    def add_plugindata(self, plugindata):
        self.__plugindata.append(plugindata)

    def get_plugin(self, id):
        """Return the PluginData for the plugin with id"""
        matches = [x for x in self.__plugindata if x.id == id]
        matches.sort(key=lambda x: version(x.version))
        if len(matches) > 0:
            return matches[-1]
        return None

    def type_plugins(self, ptype):
        """Return a list of PluginData that are of type ptype
        """
        return [self.get_plugin(id) for id in
                set([x.id for x in self.__plugindata if x.ptype == ptype])]

    def report_plugins(self, gui=True):
        """Return a list of gui or cli PluginData that are of type REPORT
           :param gui: bool, if True then gui plugin, otherwise cli plugin
        """
        if gui:
            return [x for x in self.type_plugins(REPORT) if REPORT_MODE_GUI
                                        in x.report_modes]
        else:
            return [x for x in self.type_plugins(REPORT) if REPORT_MODE_CLI
                                        in x.report_modes]

def newplugin():
    """
    Function to create a new plugindata object, add it to list of 
    registered plugins
    :Returns: a newly created PluginData which is already part of the register
    """
    gpr = PluginRegister.get_instance()
    pgd = PluginData()
    gpr.add_plugindata(pgd)
    return pgd

def register(ptype, **kwargs):
    """
    Convenience function to register a new plugin using a dictionary as input.
    The register functions will call newplugin() function, and use the 
    dictionary kwargs to assign data to the PluginData newplugin() created, 
    as in: plugindata.key = data
    :param ptype: the plugin type, one of REPORT, TOOL, ...
    :param kwargs: dictionary with keys attributes of the plugin, and data 
        the value
    
    :Returns: a newly created PluginData which is already part of the register
        and which has kwargs assigned as attributes
    """
    plg = newplugin()
    plg.ptype = ptype
    for prop in kwargs:
        #check it is a valid attribute with getattr
        getattr(plg, prop)
        #set the value
        setattr(plg, prop, kwargs[prop])
    return plg

register(GENERAL,
id    = 'system webstuff',
category = "WEBSTUFF",
name  = _("Webstuff"),
description =  _("Provides a collection of resources for the web"),
version = '1.0',
gramps_target_version = '3.3',
fname = "webstuff.py",
load_on_reg = True,
process = "process_list",
status = STABLE
  )

register(REPORT,
    id   = 'FamilySheet',
    name = _('Family Sheet'),
    description = _("Produces a family sheet showing full information "
                    "about a person and his/her partners and children."),
    version = '3.3.7',
    gramps_target_version = '3.3',
    status = STABLE,
    fname = 'FamilySheet.py',
    authors = ["Reinhard Mueller"],
    authors_email = ["reinhard.mueller@igal.at"],
    category = CATEGORY_TEXT,
    reportclass = 'FamilySheet',
    optionclass = 'FamilySheetOptions',
    report_modes = [REPORT_MODE_GUI],
    require_active = True
    )

for plugin in PluginRegister.get_instance().report_plugins():
    x = plugin.name
    print x
    y = plugin.id
    print y
    z = plugin.category
    print z
