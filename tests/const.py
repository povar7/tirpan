import os
import sys

if hasattr(sys, "frozen"):
    ROOT_DIR = os.path.abspath(os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding())))
else:
    ROOT_DIR = os.path.abspath(os.path.dirname(unicode(__file__, sys.getfilesystemencoding())))

PLUGINS_DIR = os.path.join(ROOT_DIR, "plugins")

TESTS_DIR = os.path.join(ROOT_DIR, "tests")

DIR_FOR_BUILTIN05 = os.path.join(ROOT_DIR, "import03")
