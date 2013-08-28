import gettext
import sys

import const

def make_environment(**kwargs):
    return kwargs

def foo(filename):
    local_gettext = 1
    local_gettext = 3.14
    execfile(filename.encode(sys.getfilesystemencoding()),
             make_environment(_=local_gettext),
             {})

foo(const.PATH_FOR_BUILTIN08)
