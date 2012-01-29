'''
Created on 29.01.2012

@author: bronikkk
'''

import os
from os import sys

from tiparser  import TIParser

class Importer(object):
    def __init__(self):
        self.imported_files = []

    def find_module(self, name, paths):
        for path in paths:
            filename = os.path.join(path, name) + '.py'
            if os.path.exists(filename):
                return filename
        return None

    def process_name(self, name, filename):
        paths = [os.path.dirname(filename)]
        paths.extend(sys.path)
        return self.find_module(name, paths)

    def import_files(self, mainfile, names):
        for name in names:
            if name == '__main__':
                filename   = os.path.abspath(mainfile)
                searchname = name
            else:
                filename   = os.path.abspath(self.process_name(name, mainfile))
                searchname = filename
            if searchname and searchname not in self.imported_files:
                self.imported_files.append(searchname)
                imported_tree = TIParser(filename)
                imported_tree.walk() 
