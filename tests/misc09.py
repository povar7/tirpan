import gobject

a = [1]

def foo():
    global a
    a.append(3.14)
    return False

gobject.timeout_add(100, foo, priority=100)
