def foo(x, y, z, *args):
    args[0].append(3j)
    z.append(3j)

def bar(x, *args):
    return foo(x, *args)

x = 3.14
y = ['abc']
z = [u'abc']
bar(1, x, y, z)
print y
print z

