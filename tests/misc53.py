import os

class A:
    def __init__(self, filename = None):
        self._filename = filename
        
    def _checkfilename(self):
        flag  = True
        first = True
        while flag:
            os.path.basename(self._filename)
            if first:
                first = False
                self._filename = None
            else:
                flag = False

a = A('abc')
a._checkfilename()
