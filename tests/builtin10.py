import re

import const

pymod = re.compile(r"^(.*)\.py$")
match = pymod.match(const.WEBSTUFF_PYTHON_FN)
x = match.groups()[0]
print x
