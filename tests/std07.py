def foo():
    for i in [(1, 'str'), (3.14, u'str')]:
        yield i

for (a, b) in foo():
    print a, b
