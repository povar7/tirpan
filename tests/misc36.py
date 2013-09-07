import gettext
import os
import re
import sys

from const import VERSION as GRAMPSVERSION, IMAGE_DIR, PLUGINS_DIR

_ = gettext.gettext

#a plugin is stable or unstable
STABLE   = 0
UNSTABLE = 1
STATUS   = [STABLE, UNSTABLE]
STATUSTEXT = {STABLE: _('Stable'), UNSTABLE: _('Unstable')}
#possible plugin types
REPORT      = 0
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
PTYPE_STR   = {
        REPORT: _('Report') , 
        QUICKREPORT: _('Quickreport'), 
        TOOL: _('Tool'), 
        IMPORT: _('Importer'),
        EXPORT: _('Exporter'), 
        DOCGEN: _('Doc creator'), 
        GENERAL: _('Plugin lib'), 
        MAPSERVICE: _('Map service'), 
        VIEW: _('Gramps View'), 
        RELCALC: _('Relationships'), 
        GRAMPLET: _('Gramplet'),
        SIDEBAR: _('Sidebar'),
        }

#possible report categories
CATEGORY_TEXT       = 0
CATEGORY_DRAW       = 1
CATEGORY_CODE       = 2
CATEGORY_WEB        = 3
CATEGORY_BOOK       = 4
CATEGORY_GRAPHVIZ   = 5
REPORT_CAT          = [ CATEGORY_TEXT, CATEGORY_DRAW, CATEGORY_CODE,
                        CATEGORY_WEB, CATEGORY_BOOK, CATEGORY_GRAPHVIZ]
#possible tool categories
TOOL_DEBUG  = -1
TOOL_ANAL   = 0
TOOL_DBPROC = 1
TOOL_DBFIX  = 2
TOOL_REVCTL = 3
TOOL_UTILS  = 4
TOOL_CAT    = [ TOOL_DEBUG, TOOL_ANAL, TOOL_DBPROC, TOOL_DBFIX, TOOL_REVCTL,
                TOOL_UTILS]

#possible quickreport categories
CATEGORY_QR_MISC       = -1
CATEGORY_QR_PERSON     = 0
CATEGORY_QR_FAMILY     = 1
CATEGORY_QR_EVENT      = 2
CATEGORY_QR_SOURCE     = 3
CATEGORY_QR_PLACE      = 4
CATEGORY_QR_REPOSITORY = 5
CATEGORY_QR_NOTE       = 6
CATEGORY_QR_DATE       = 7
CATEGORY_QR_MEDIA      = 8

# Modes for generating reports
REPORT_MODE_GUI = 1    # Standalone report using GUI
REPORT_MODE_BKI = 2    # Book Item interface using GUI
REPORT_MODE_CLI = 4    # Command line interface (CLI)
REPORT_MODES    = [REPORT_MODE_GUI, REPORT_MODE_BKI, REPORT_MODE_CLI]
    
# Modes for running tools
TOOL_MODE_GUI = 1    # Standard tool using GUI
TOOL_MODE_CLI = 2    # Command line interface (CLI)
TOOL_MODES    = [TOOL_MODE_GUI, TOOL_MODE_CLI]

# possible view orders
START = 1
END   = 2

def get_addon_translator(filename):
    return gettext.translation(filename, None, None, None, True)

class PluginData(object):

    def __init__(self):
        #read/write attribute
        self.directory = None
        #base attributes
        self._id = None
        self._name = None
        self._name_accell = None
        self._version = None
        self._gramps_target_version = None
        self._description = None
        self._status = UNSTABLE
        self._fname = None
        self._fpath = None
        self._ptype = None
        self._authors = []
        self._authors_email = []
        self._supported = True
        self._load_on_reg = False
        self._icons = []
        self._icondir = None
        self._depends_on = []
        #derived var
        self.mod_name = None
        #RELCALC attr
        self._relcalcclass = None
        self._lang_list = None
        #REPORT attr
        self._reportclass = None
        self._require_active = True
        self._report_modes = [REPORT_MODE_GUI]
        #REPORT and TOOL and GENERAL attr
        self._category = None
        #REPORT and TOOL attr
        self._optionclass = None
        #TOOL attr
        self._toolclass = None
        self._tool_modes = [TOOL_MODE_GUI]
        #DOCGEN attr
        self._basedocclass = None
        self._paper = True
        self._style = True  
        self._extension = ''
        #QUICKREPORT attr
        self._runfunc = None
        #MAPSERVICE attr
        self._mapservice = None
        #EXPORT attr
        self._export_function = None
        self._export_options = None
        self._export_options_title = ''
        #IMPORT attr
        self._import_function = None
        #GRAMPLET attr
        self._gramplet = None
        self._height = 200
        self._detached_height = 300
        self._detached_width = 400
        self._expand = False
        self._gramplet_title = _('Gramplet')
        self._navtypes = []
        self._orientation = None
        self._help_url = None
        #VIEW attr
        self._viewclass = None
        self._stock_icon = None
        #SIDEBAR attr
        self._sidebarclass = None
        self._menu_label = ''
        #VIEW and SIDEBAR attr
        self._order = END
        #GENERAL attr
        self._data = []
        self._process = None
    
    def _set_id(self, id):
       self._id = id

    def _get_id(self):
        return self._id

    def _set_name(self, name):
        self._name = name

    def _get_name(self):
        return self._name
    
    def _set_name_accell(self, name):
        self._name_accell = name

    def _get_name_accell(self):
        if self._name_accell is None:
            return self._name
        else:
            return self._name_accell

    def _set_description(self, description):
        self._description = description

    def _get_description(self):
        return self._description

    def _set_version(self, version):
       self._version = version

    def _get_version(self):
        return self._version

    def _set_gramps_target_version(self, version):
       self._gramps_target_version = version

    def _get_gramps_target_version(self):
        return self._gramps_target_version

    def _set_status(self, status):
        if status not in STATUS:
            raise ValueError, 'plugin status cannot be %s' % str(status)
        self._status = status

    def _get_status(self):
        return self._status
    
    def _set_fname(self, fname):
        self._fname = fname

    def _get_fname(self):
        return self._fname
    
    def _set_fpath(self, fpath):
        self._fpath = fpath

    def _get_fpath(self):
        return self._fpath
    
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

    def _set_authors(self, authors):
        if not authors or not isinstance(authors, list):
            return
        self._authors = authors

    def _get_authors(self):
        return self._authors

    def _set_authors_email(self, authors_email):
        if not authors_email or not isinstance(authors_email, list):
            return
        self._authors_email = authors_email

    def _get_authors_email(self):
        return self._authors_email
    
    def _set_supported(self, supported):
        if not isinstance(supported, bool):
            raise ValueError, 'Plugin must have supported=True or False'
        self._supported = supported
    
    def _get_supported(self):
        return self._supported

    def _set_load_on_reg(self, load_on_reg):
        if not isinstance(load_on_reg, bool):
            raise ValueError, 'Plugin must have load_on_reg=True or False'
        self._load_on_reg = load_on_reg

    def _get_load_on_reg(self):
        return self._load_on_reg

    def _get_icons(self):
        return self._icons

    def _set_icons(self, icons):
        if not isinstance(icons, list):
            raise ValueError, 'Plugin must have icons as a list'
        self._icons = icons

    def _get_icondir(self):
        return self._icondir

    def _set_icondir(self, icondir):
        self._icondir = icondir

    def _get_depends_on(self):
        return self._depends_on

    def _set_depends_on(self, depends):
        if not isinstance(depends, list):
            raise ValueError, 'Plugin must have depends_on as a list'
        self._depends_on = depends

    id = property(_get_id, _set_id)
    name = property(_get_name, _set_name)
    name_accell = property(_get_name_accell, _set_name_accell)
    description = property(_get_description, _set_description) 
    version = property(_get_version, _set_version) 
    gramps_target_version = property(_get_gramps_target_version, 
                                     _set_gramps_target_version) 
    status = property(_get_status, _set_status)
    fname = property(_get_fname, _set_fname)
    fpath = property(_get_fpath, _set_fpath)
    ptype = property(_get_ptype, _set_ptype)
    authors = property(_get_authors, _set_authors)
    authors_email = property(_get_authors_email, _set_authors_email)
    supported = property(_get_supported, _set_supported)
    load_on_reg = property(_get_load_on_reg, _set_load_on_reg)
    icons = property(_get_icons, _set_icons)
    icondir = property(_get_icondir, _set_icondir)
    depends_on = property(_get_depends_on, _set_depends_on)

    def statustext(self):
        return STATUSTEXT[self.status]
    
    #type specific plugin attributes
    
    #RELCALC attributes
    def _set_relcalcclass(self, relcalcclass):
        if not self._ptype == RELCALC:
            raise ValueError, 'relclcclass may only be set for RELCALC plugins'
        self._relcalcclass = relcalcclass

    def _get_relcalcclass(self):
        return self._relcalcclass
    
    def _set_lang_list(self, lang_list):
        if not self._ptype == RELCALC:
            raise ValueError, 'lang_list may only be set for RELCALC plugins'
        self._lang_list = lang_list

    def _get_lang_list(self):
        return self._lang_list

    relcalcclass = property(_get_relcalcclass, _set_relcalcclass)
    lang_list = property(_get_lang_list, _set_lang_list)
    
    #REPORT attributes
    def _set_require_active(self, require_active):
        if not self._ptype == REPORT:
            raise ValueError, 'require_act may only be set for REPORT plugins'
        if not isinstance(require_active, bool):
            raise ValueError, 'Report must have require_active=True or False'
        self._require_active = require_active

    def _get_require_active(self):
        return self._require_active

    def _set_reportclass(self, reportclass):
        if not self._ptype == REPORT:
            raise ValueError, 'reportclass may only be set for REPORT plugins'
        self._reportclass = reportclass

    def _get_reportclass(self):
        return self._reportclass

    def _set_report_modes(self, report_modes):
        if not self._ptype == REPORT:
            raise ValueError, 'report_modes may only be set for REPORT plugins'
        if not isinstance(report_modes, list):
            raise ValueError, 'report_modes must be a list'
        self._report_modes = [x for x in report_modes if x in REPORT_MODES]
        if not self._report_modes:
            raise ValueError, 'report_modes not a valid list of modes'

    def _get_report_modes(self):
        return self._report_modes

    #REPORT or TOOL or QUICKREPORT or GENERAL attributes
    def _set_category(self, category):
        if self._ptype not in [REPORT, TOOL, QUICKREPORT, VIEW, GENERAL]:
            raise ValueError, 'category may only be set for ' \
                              'REPORT/TOOL/QUICKREPORT/VIEW/GENERAL plugins'
        self._category = category

    def _get_category(self):
        return self._category

    #REPORT OR TOOL attributes
    def _set_optionclass(self, optionclass):
        if not (self._ptype == REPORT or self.ptype == TOOL):
            raise ValueError, 'optcls may only be set for REPORT/TOOL plugins'
        self._optionclass = optionclass

    def _get_optionclass(self):
        return self._optionclass

    #TOOL attributes
    def _set_toolclass(self, toolclass):
        if not self._ptype == TOOL:
            raise ValueError, 'toolclass may only be set for TOOL plugins'
        self._toolclass = toolclass
    
    def _get_toolclass(self):
        return self._toolclass

    def _set_tool_modes(self, tool_modes):
        if not self._ptype == TOOL:
            raise ValueError, 'tool_modes may only be set for TOOL plugins'
        if not isinstance(tool_modes, list):
            raise ValueError, 'tool_modes must be a list'
        self._tool_modes = [x for x in tool_modes if x in TOOL_MODES]
        if not self._tool_modes:
            raise ValueError, 'tool_modes not a valid list of modes'

    def _get_tool_modes(self):
        return self._tool_modes
    
    require_active = property(_get_require_active, _set_require_active)
    reportclass = property(_get_reportclass, _set_reportclass)
    report_modes = property(_get_report_modes, _set_report_modes)
    category = property(_get_category, _set_category)
    optionclass = property(_get_optionclass, _set_optionclass)
    toolclass = property(_get_toolclass, _set_toolclass)
    tool_modes = property(_get_tool_modes, _set_tool_modes)

    #DOCGEN attributes
    def _set_basedocclass(self, basedocclass):
        if not self._ptype == DOCGEN:
            raise ValueError, 'basedocclass may only be set for DOCGEN plugins'
        self._basedocclass = basedocclass
    
    def _get_basedocclass(self):
        return self._basedocclass
    
    def _set_paper(self, paper):
        if not self._ptype == DOCGEN:
            raise ValueError, 'paper may only be set for DOCGEN plugins'
        if not isinstance(paper, bool):
            raise ValueError, 'Plugin must have paper=True or False'
        self._paper = paper
    
    def _get_paper(self):
        return self._paper
    
    def _set_style(self, style):
        if not self._ptype == DOCGEN:
            raise ValueError, 'style may only be set for DOCGEN plugins'
        if not isinstance(style, bool):
            raise ValueError, 'Plugin must have style=True or False'
        self._style = style
    
    def _get_style(self):
        return self._style
    
    def _set_extension(self, extension):
        if not (self._ptype == DOCGEN or self._ptype == EXPORT 
                or self._ptype == IMPORT):
            raise ValueError, 'extension may only be set for DOCGEN/EXPORT/'\
                              'IMPORT plugins'
        self._extension = extension
    
    def _get_extension(self):
        return self._extension
    
    basedocclass = property(_get_basedocclass, _set_basedocclass)
    paper = property(_get_paper, _set_paper)
    style = property(_get_style, _set_style)    
    extension = property(_get_extension, _set_extension)
    
    #QUICKREPORT attributes
    def _set_runfunc(self, runfunc):
        if not self._ptype == QUICKREPORT:
            raise ValueError, 'runfunc may only be set for QUICKREPORT plugins'
        self._runfunc = runfunc
    
    def _get_runfunc(self):
        return self._runfunc
    
    runfunc = property(_get_runfunc, _set_runfunc)
    
    #MAPSERVICE attributes
    def _set_mapservice(self, mapservice):
        if not self._ptype == MAPSERVICE:
            raise ValueError, 'mapserv may only be set for MAPSERVICE plugins'
        self._mapservice = mapservice
    
    def _get_mapservice(self):
        return self._mapservice
    
    mapservice = property(_get_mapservice, _set_mapservice)

    #EXPORT attributes
    def _set_export_function(self, export_function):
        if not self._ptype == EXPORT:
            raise ValueError, 'export_func may only be set for EXPORT plugins'
        self._export_function = export_function
    
    def _get_export_function(self):
        return self._export_function
    
    def _set_export_options(self, export_options):
        if not self._ptype == EXPORT:
            raise ValueError, 'exp_opts may only be set for EXPORT plugins'
        self._export_options = export_options
    
    def _get_export_options(self):
        return self._export_options
    
    def _set_export_options_title(self, export_options_title):
        if not self._ptype == EXPORT:
            raise ValueError, 'exp_opts_ttl may only be set for EXPORT plugins'
        self._export_options_title = export_options_title
    
    def _get_export_options_title(self):
        return self._export_options_title

    export_function = property(_get_export_function, _set_export_function)
    export_options = property(_get_export_options, _set_export_options)
    export_options_title = property(_get_export_options_title, 
                                    _set_export_options_title)
    
    #IMPORT attributes
    def _set_import_function(self, import_function):
        if not self._ptype == IMPORT:
            raise ValueError, 'import_func may only be set for IMPORT plugins'
        self._import_function = import_function
    
    def _get_import_function(self):
        return self._import_function
    
    import_function = property(_get_import_function, _set_import_function)

    #GRAMPLET attributes
    def _set_gramplet(self, gramplet):
        if not self._ptype == GRAMPLET:
            raise ValueError, 'gramplet may only be set for GRAMPLET plugins'
        self._gramplet = gramplet
    
    def _get_gramplet(self):
        return self._gramplet
    
    def _set_height(self, height):
        if not self._ptype == GRAMPLET:
            raise ValueError, 'height may only be set for GRAMPLET plugins'
        if not isinstance(height, int):
            raise ValueError, 'Plugin must have height an integer'
        self._height = height
    
    def _get_height(self):
        return self._height
    
    def _set_detached_height(self, detached_height):
        if not self._ptype == GRAMPLET:
            raise ValueError, 'detached_h may only be set for GRAMPLET plugins'
        if not isinstance(detached_height, int):
            raise ValueError, 'Plugin must have detached_height an integer'
        self._detached_height = detached_height
    
    def _get_detached_height(self):
        return self._detached_height
    
    def _set_detached_width(self, detached_width):
        if not self._ptype == GRAMPLET:
            raise ValueError, 'detached_w may only be set for GRAMPLET plugins'
        if not isinstance(detached_width, int):
            raise ValueError, 'Plugin must have detached_width an integer'
        self._detached_width = detached_width
    
    def _get_detached_width(self):
        return self._detached_width

    def _set_expand(self, expand):
        if not self._ptype == GRAMPLET:
            raise ValueError, 'expand may only be set for GRAMPLET plugins'
        if not isinstance(expand, bool):
            raise ValueError, 'Plugin must have expand as a bool'
        self._expand = expand
    
    def _get_expand(self):
        return self._expand
    
    def _set_gramplet_title(self, gramplet_title):
        if not self._ptype == GRAMPLET:
            raise ValueError, 'glet_title may only be set for GRAMPLET plugins'
        if not isinstance(gramplet_title, str):
            raise ValueError, 'Plugin must have a string as gramplet_title'
        self._gramplet_title = gramplet_title
    
    def _get_gramplet_title(self):
        return self._gramplet_title

    def _set_help_url(self, help_url):
        if not self._ptype == GRAMPLET:
            raise ValueError, 'help_url may only be set for GRAMPLET plugins'
        self._help_url = help_url

    def _get_help_url(self):
        return self._help_url

    def _set_navtypes(self, navtypes):
        if not self._ptype == GRAMPLET:
            raise ValueError, 'navtypes may only be set for GRAMPLET plugins'
        self._navtypes = navtypes

    def _get_navtypes(self):
        return self._navtypes
    
    def _set_orientation(self, orientation):
        if not self._ptype == GRAMPLET:
            raise ValueError, 'orient may only be set for GRAMPLET plugins'
        self._orientation = orientation

    def _get_orientation(self):
        return self._orientation
    
    gramplet = property(_get_gramplet, _set_gramplet)
    height = property(_get_height, _set_height)
    detached_height = property(_get_detached_height, _set_detached_height)
    detached_width = property(_get_detached_width, _set_detached_width)
    expand = property(_get_expand, _set_expand)
    gramplet_title = property(_get_gramplet_title, _set_gramplet_title)
    navtypes = property(_get_navtypes, _set_navtypes)
    orientation = property(_get_orientation, _set_orientation)
    help_url = property(_get_help_url, _set_help_url)

    def _set_viewclass(self, viewclass):
        if not self._ptype == VIEW:
            raise ValueError, 'viewclass may only be set for VIEW plugins'
        self._viewclass = viewclass

    def _get_viewclass(self):
        return self._viewclass
  
    def _set_stock_icon(self, stock_icon):
        if not self._ptype == VIEW:
            raise ValueError, 'stock_icon may only be set for VIEW plugins'
        self._stock_icon = stock_icon

    def _get_stock_icon(self):
        return self._stock_icon
       
    viewclass = property(_get_viewclass, _set_viewclass)
    stock_icon = property(_get_stock_icon, _set_stock_icon)

    #SIDEBAR attributes
    def _set_sidebarclass(self, sidebarclass):
        if not self._ptype == SIDEBAR:
            raise ValueError, 'sidebarcls may only be set for SIDEBAR plugins'
        self._sidebarclass = sidebarclass

    def _get_sidebarclass(self):
        return self._sidebarclass
        
    def _set_menu_label(self, menu_label):
        if not self._ptype == SIDEBAR:
            raise ValueError, 'menu_label may only be set for SIDEBAR plugins'
        self._menu_label = menu_label

    def _get_menu_label(self):
        return self._menu_label

    sidebarclass = property(_get_sidebarclass, _set_sidebarclass)
    menu_label   = property(_get_menu_label, _set_menu_label)

    #VIEW and SIDEBAR attributes
    def _set_order(self, order):
        if not self._ptype in (VIEW, SIDEBAR):
            raise ValueError, 'ord may only be set for VIEW & SIDEBAR plugins'
        self._order = order

    def _get_order(self):
        return self._order

    order = property(_get_order, _set_order)
  
    #GENERAL attr
    def _set_data(self, data):
        if not self._ptype in (GENERAL,):
            raise ValueError, 'data may only be set for GENERAL plugins'
        self._data = data

    def _get_data(self):
        return self._data

    def _set_process(self, process):
        if not self._ptype in (GENERAL,):
            raise ValueError, 'process may only be set for GENERAL plugins'
        self._process = process

    def _get_process(self):
        return self._process

    data = property(_get_data, _set_data)
    process = property(_get_process, _set_process)

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

def make_environment(**kwargs):
    env = {
        'newplugin': newplugin,
        'register': register,
        'STABLE': STABLE,
        'UNSTABLE': UNSTABLE,
        'REPORT': REPORT,
        'QUICKREPORT': QUICKREPORT,
        'TOOL': TOOL,
        'IMPORT': IMPORT,
        'EXPORT': EXPORT,
        'DOCGEN': DOCGEN,
        'GENERAL': GENERAL,
        'MAPSERVICE': MAPSERVICE,
        'VIEW': VIEW,
        'RELCALC': RELCALC,
        'GRAMPLET': GRAMPLET,
        'SIDEBAR': SIDEBAR,
        'CATEGORY_TEXT': CATEGORY_TEXT,
        'CATEGORY_DRAW': CATEGORY_DRAW,
        'CATEGORY_CODE': CATEGORY_CODE,
        'CATEGORY_WEB': CATEGORY_WEB,
        'CATEGORY_BOOK': CATEGORY_BOOK,
        'CATEGORY_GRAPHVIZ': CATEGORY_GRAPHVIZ,
        'TOOL_DEBUG': TOOL_DEBUG,
        'TOOL_ANAL': TOOL_ANAL,
        'TOOL_DBPROC': TOOL_DBPROC,
        'TOOL_DBFIX': TOOL_DBFIX,
        'TOOL_REVCTL': TOOL_REVCTL,
        'TOOL_UTILS': TOOL_UTILS,
        'CATEGORY_QR_MISC': CATEGORY_QR_MISC,
        'CATEGORY_QR_PERSON': CATEGORY_QR_PERSON,
        'CATEGORY_QR_FAMILY': CATEGORY_QR_FAMILY,
        'CATEGORY_QR_EVENT': CATEGORY_QR_EVENT,
        'CATEGORY_QR_SOURCE': CATEGORY_QR_SOURCE,
        'CATEGORY_QR_PLACE': CATEGORY_QR_PLACE,
        'CATEGORY_QR_MEDIA': CATEGORY_QR_MEDIA,
        'CATEGORY_QR_REPOSITORY': CATEGORY_QR_REPOSITORY,
        'CATEGORY_QR_NOTE': CATEGORY_QR_NOTE,
        'CATEGORY_QR_DATE': CATEGORY_QR_DATE,
        'REPORT_MODE_GUI': REPORT_MODE_GUI, 
        'REPORT_MODE_BKI': REPORT_MODE_BKI, 
        'REPORT_MODE_CLI': REPORT_MODE_CLI,
        'TOOL_MODE_GUI': TOOL_MODE_GUI, 
        'TOOL_MODE_CLI': TOOL_MODE_CLI,
        'GRAMPSVERSION': GRAMPSVERSION,
        'START': START,
        'END': END,
        'IMAGE_DIR': IMAGE_DIR,
        }
    env.update(kwargs)
    return env

def newplugin():
    gpr = PluginRegister.get_instance()
    pgd = PluginData()
    gpr.add_plugindata(pgd)
    return pgd

def register(ptype, **kwargs):
    plg = newplugin()
    plg.ptype = ptype
    for prop in kwargs:
        #check it is a valid attribute with getattr
        getattr(plg, prop)
        #set the value
        setattr(plg, prop, kwargs[prop])
    return plg

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
        """ This function should only be run once by get_instance() """
        if PluginRegister.__instance is not 1:
            raise Exception("This class is a singleton. "
                            "Use the get_instance() method")
        self.stable_only = True
        if __debug__:
            self.stable_only = False
        self.__plugindata  = []

    def add_plugindata(self, plugindata):
        self.__plugindata.append(plugindata)
        
    def scan_dir(self, dir):
        """
        The dir name will be scanned for plugin registration code, which will
        be loaded in PluginData objects if they satisfy some checks.
        
        :Returns: A list with PluginData objects
        """
        # if the directory does not exist, do nothing
        if not (os.path.isdir(dir) or os.path.islink(dir)):
            return []
        
        ext = r".gpr.py"
        extlen = -len(ext)
        pymod = re.compile(r"^(.*)\.py$")
        
        for filename in os.listdir(dir):
            name = os.path.split(filename)[1]
            if not name[extlen:] == ext:
                continue
            lenpd = len(self.__plugindata)
            full_filename = os.path.join(dir, filename)
            local_gettext = get_addon_translator(full_filename).gettext
            try:
                execfile(full_filename.encode(sys.getfilesystemencoding()),
                         make_environment(_=local_gettext),
                         {})
            except ValueError, msg:
                self.__plugindata = self.__plugindata[:lenpd]
            except:
                self.__plugindata = self.__plugindata[:lenpd]
            for plugin in self.__plugindata[lenpd:]:
                plugin.directory = dir
                if plugin.fname is None:
                    continue
                match = pymod.match(plugin.fname)
                if not match:
                    continue
                if not os.path.isfile(os.path.join(dir, plugin.fname)):
                    continue
                module = match.groups()[0]
                plugin.mod_name = module
                plugin.fpath = dir

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

    def general_plugins(self, category=None):
        """Return a list of PluginData that are of type GENERAL
        """
        plugins = self.type_plugins(GENERAL)
        if category:
            return [plugin for plugin in plugins 
                    if plugin.category == category]
        return plugins

    def filter_load_on_reg(self):
        """Return a list of PluginData that have load_on_reg == True
        """
        return [self.get_plugin(id) for id in 
                set([x.id for x in self.__plugindata 
                     if x.load_on_reg == True])]

class BasePluginManager(object):
    """ unique singleton storage class for a PluginManager. """

    __instance = None
    
    def get_instance():
        """ Use this function to get the instance of the PluginManager """
        if BasePluginManager.__instance is None:
            BasePluginManager.__instance = 1 # Set to 1 for __init__()
            BasePluginManager.__instance = BasePluginManager()
        return BasePluginManager.__instance
    get_instance = staticmethod(get_instance)
    
    def __init__(self):
        """ This function should only be run once by get_instance() """
        if BasePluginManager.__instance is not 1:
            raise Exception("This class is a singleton. "
                            "Use the get_instance() method")

        self.__pgr = PluginRegister.get_instance()
        self.__loaded_plugins = {}

    def reg_plugins(self, direct, dbstate=None, uistate=None, 
                    append=True, load_on_reg=False):
        for (dirpath, dirnames, filenames) in os.walk(direct):
            self.__pgr.scan_dir(dirpath)

        if load_on_reg:
            plugins_to_load = []
            for plugin in self.__pgr.filter_load_on_reg():
                plugins_to_load.append(plugin)
            plugins_sorted = []
            for plugin in plugins_to_load[:]: # copy of list
                if plugin not in plugins_sorted:
                    plugins_sorted.append(plugin)
            # now load them:
            for plugin in plugins_sorted:
                mod = self.load_plugin(plugin)
                if hasattr(mod, "load_on_reg"):
                    results = mod.load_on_reg()
                    try:
                        iter(results)
                        plugin.data += results
                    except:
                        plugin.data  = results

    def is_loaded(self, pdata_id):
        """
        return True if plugin is already loaded
        """
        if pdata_id in self.__loaded_plugins:
            return True
        return False

    def load_plugin(self, pdata):
        """
        Load a PluginData object. This means import of the python module.
        Plugin directories are added to sys path, so files are found
        """
        if pdata.id in self.__loaded_plugins:
            return self.__loaded_plugins[pdata.id]
        try: 
            _module = self.import_plugin(pdata)
            return _module
        except:
            return None

    def import_plugin(self, pdata):
        """
        Rather than just __import__(id), this will add the pdata.fpath
        to sys.path first (if needed), import, and then reset path.
        """
        module = None
        if isinstance(pdata, basestring):
            pdata = self.get_plugin(pdata)
        if not pdata:
            return None
        if pdata.fpath not in sys.path:
            if pdata.mod_name:
                sys.path.insert(0, pdata.fpath)
                module = __import__(pdata.mod_name)
                sys.path.pop(0)
            else:
                print "WARNING: module cannot be loaded"
        else:
            module = __import__(pdata.mod_name)
        return module
       
    def get_plugin(self, id):
        """ 
        Returns a plugin object from PluginRegister by id.
        """
        return self.__pgr.get_plugin(id)

    def load_plugin_category(self, category):
        """
        Make sure all plugins of a type are loaded.
        """
        for plugin in self.__pgr.general_plugins(category):
            if not self.is_loaded(plugin):
                self.load_plugin(plugin)

    def get_plugin_data(self, category):
        """
        Gets all of the data from general plugins of type category.
        plugin.data maybe a single item, an iterable, or a callable.

        >>> PLUGMAN.get_plugin_data('CSS')
        <a list of raw data items>
        """
        retval = []
        data = None
        for plugin in self.__pgr.general_plugins(category):
            data = plugin.data
            try:
                iter(data)
                retval.extend(data)
            except:
                retval.append(data)
        return retval
    
basemgr = BasePluginManager.get_instance()
basemgr.reg_plugins(PLUGINS_DIR, load_on_reg=True)
x = basemgr.get_plugin_data('WEBSTUFF')
print x
