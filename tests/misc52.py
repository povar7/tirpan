import os

class A:
    def __init__(self, filename = None):
        self._filename = filename
        
    def _checkfilename(self):
        os.path.basename(self._filename)
        self._filename = self._filename + '.htm'
        os.path.basename(self._filename)

a = A()
a._checkfilename()
