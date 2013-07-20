def foo():
    for i in [(1, 'abc'), (3.14, u'abc')]:
        yield i

for (a, b) in foo():
    print a, b
