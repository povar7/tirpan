import gettext

import const

REPORT = 0

def make_environment(**kwargs):
    res = {'register' : register,
           'REPORT'   : REPORT}
    res.update(kwargs)
    return res

x = []
y = []

def register(ptype, **kwargs):
    x.append(ptype)
    y.append(kwargs['name'])

def pgettext(message):
    return unicode(message)

_ = pgettext

def get_addon_translation(filename):
    return gettext.translation(filename, None, None, None, True)

local_gettext = get_addon_translation(const.PATH_FOR_MISC34_2).gettext 
execfile(const.PATH_FOR_MISC34_2, make_environment(_=local_gettext), {})

print x
print y
