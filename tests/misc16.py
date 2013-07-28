def foo(raw):
    data   = None
    data   = raw
    retval = []
    if data:
        try:
            try:
                iter(data)
                retval.extend(data)
            except AttributeError:
                pass
        except:
            pass
    return retval

x = foo([1, 3.14])
print x
y = foo(1)
print y
