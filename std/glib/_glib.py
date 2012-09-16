quasi_timeout_add =                                       \
'def timeout_add(interval, callback, *args, **kwargs):\n' \
'    callback(*args)'

functions = [                                             \
            ]

stubs     = [                                             \
                ['timeout_add', quasi_timeout_add]        \
            ]

variables = [                                             \
            ]

modules   = [                                             \
            ]

objects   = [                                             \
            ]

def get_all():
    return (functions, stubs, variables, modules, objects)
