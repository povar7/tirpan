import const

class A:
    pass

def func(obj, **kwargs):
    for prop in kwargs:
        setattr(obj, prop, kwargs[prop])

a = A()
func(a, foo=const.X, bar=const.Y, xxx=True)
x = a.foo
print x
y = a.bar
print y
z = a.xxx
print z
