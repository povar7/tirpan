import re

import const

pymod = re.compile(r"^(.*)\.py$")
match = pymod.match(const.WEBSTUFF_PYTHON_FN)
x = match.groups()[0]
print x

import sys

sys.path.insert(0, const.WEBSTUFF_PYTHON_DR)
y = sys.path
print y
module = __import__(x)
sys.path.pop(0)
print module
