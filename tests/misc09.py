import gobject

a = [1]

def foo(x, y):
    a.append(3.14)
    return False

gobject.timeout_add(100, foo, 'abc', 3j, priority=100)
