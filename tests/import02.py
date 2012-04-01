from sys import argv
from sys import path as mama
from sys import getsizeof

def foo():
    return argv

def bar():
    return mama

x = foo()
y = bar()
z = getsizeof('abc')
