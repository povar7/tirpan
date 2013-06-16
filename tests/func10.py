def foo(x, y = 1, *args, **kwargs):
    return kwargs

x = foo(3, 6, 2.0, 'abc', foo  = 10  , bar  = 1.0)
y = foo(3, 6, 2.0, 'abc', mama = 3.14, papa = 7  )
