import os
import sys

if hasattr(sys, "frozen"):
    ROOT_DIR = os.path.abspath(
                   os.path.dirname(unicode(sys.executable,
                                           sys.getfilesystemencoding())))
else:
    ROOT_DIR = os.path.abspath(
                   os.path.dirname(unicode(__file__,
                                           sys.getfilesystemencoding())))

PLUGINS_DIR = os.path.join(ROOT_DIR, "plugins")

DIR_FOR_BUILTIN05  = os.path.join(ROOT_DIR, "import03")
PATH_FOR_BUILTIN08 = os.path.join(ROOT_DIR, "builtin08.py")

X = 'x'
Y = 'y'

WEBSTUFF_PLUGIN_ID = 'system webstuff'
WEBSTUFF_PYTHON_FN = 'webstuff.py'
WEBSTUFF_PYTHON_DR = os.path.join(PLUGINS_DIR, 'webstuff')

FANCHART_PLUGIN_ID = 'fanchartview'
FANCHART_PYTHON_FN = 'fanchartview.py'

REPORT_KEY = 'FamilySheet'
REPORT_MENU_NAME = 'Family Sheet...'

VERSION       = "3.3.0"
VERSION_TUPLE = (3, 3, 0)

if os.environ.has_key('GRAMPSHOME'):
    USER_HOME = os.environ['GRAMPSHOME'] 
    HOME_DIR = os.path.join(USER_HOME, 'gramps')
elif os.environ.has_key('USERPROFILE'):
    USER_HOME = os.environ['USERPROFILE'] 
    if os.environ.has_key('APPDATA'):
        HOME_DIR = os.path.join(os.environ['APPDATA'], 'gramps')
    else:
        HOME_DIR = os.path.join(USER_HOME, 'gramps')
else:
    USER_HOME = os.environ['HOME']
    HOME_DIR = os.path.join(USER_HOME, '.gramps')

# Conversion of USER_HOME to unicode was needed to have better
# support for non ASCII path names in Windows for the Gramps database.
USER_HOME = unicode(USER_HOME, sys.getfilesystemencoding())
HOME_DIR = unicode(HOME_DIR, sys.getfilesystemencoding())

IMAGE_DIR     = os.path.join(ROOT_DIR, "images")
VERSION_DIR   = os.path.join(HOME_DIR,
                             "gramps%s%s" % (VERSION_TUPLE[0],
                                             VERSION_TUPLE[1]))
USER_PLUGINS  = os.path.join(VERSION_DIR, "plugins")

CONST_PYTHON_FN = os.path.basename('../tests/const.py')

PATH_FOR_MISC34_2 = os.path.join(ROOT_DIR, "misc34_2.py")

if sys.platform == "win32":
    if sys.prefix == os.path.dirname(os.getcwd()):
        PREFIXDIR = sys.prefix
        SYSCONFDIR = os.path.join(sys.prefix, "etc")
elif  sys.platform == "darwin" and sys.prefix != sys.exec_prefix:
    PREFIXDIR = sys.prefix
    SYSCONFDIR = os.path.join(sys.prefix, "etc")
else:
    PREFIXDIR = "/usr/local"
    SYSCONFDIR = "${prefix}/etc"

LINUX = ["Linux", "linux", "linux2"]
MACOS = ["Darwin", "darwin"]
WINDOWS = ["Windows", "win32"]

URL_WIKISTRING  = "http://gramps-project.org/wiki/index.php?title="
URL_MANUAL_PAGE = "Gramps_3.3_Wiki_Manual"
