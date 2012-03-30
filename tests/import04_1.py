from os.path import exists

def foo(filename):
    return exists(filename)

x = foo('some_file')
