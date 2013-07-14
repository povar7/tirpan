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

REPORT_KEY = 'FamilySheet'
REPORT_MENU_NAME = 'Family Sheet...'

VERSION_TUPLE = (3, 3, 0)
USER_HOME     = os.environ['HOME']
HOME_DIR      = os.path.join(USER_HOME, '.gramps')
VERSION_DIR   = os.path.join(HOME_DIR,
                             "gramps%s%s" % (VERSION_TUPLE[0],
                                             VERSION_TUPLE[1]))
USER_PLUGINS  = os.path.join(VERSION_DIR, "plugins")

CONST_PYTHON_FN = os.path.basename('../tests/const.py')
