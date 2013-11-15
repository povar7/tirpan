class A(object):
    def __init__(self):
        self._data = []

    def _get_data(self):
        return self._data

    def _set_data(self, data):
        self._data = data

    data = property(_get_data, _set_data)

a = A()
a.data += [1, 3.14, 'abc']
x = a.data
print x
