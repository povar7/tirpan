from sys import argv
from sys import path as mama

def foo():
    return argv

def bar():
    return mama

x = foo()
y = bar()
