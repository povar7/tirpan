import sys

_names = sys.builtin_module_names

if 'posix' in _names:
    import posixpath as path
elif 'nt' in _names:
    import ntpath as path
elif 'os2' in _names:
    import os2emxpath as path

x = path
print x
