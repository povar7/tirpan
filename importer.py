'''
Created on 29.01.2012

@author: bronikkk
'''

import ast

import os
from os import sys

import __main__

from tiparser  import TIParser
from typegraph import VarTypeGraphNode, ModuleTypeGraphNode, DependencyType

class Importer(object):
    def __init__(self):
        self.imported_files = {}

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

    def import_files(self, mainfile, aliases):
        for alias in aliases:
            name = alias.name
            if name == '__main__':
                filename   = os.path.abspath(mainfile)
                searchname = name
            else:
                filename   = os.path.abspath(self.process_name(name, mainfile))
                searchname = filename
            if not searchname:
                return
            if searchname in self.imported_files:
                imported_tree = self.imported_files[searchname].ast
            else:
                parser = TIParser(filename)
                imported_tree = parser.ast
                module = ModuleTypeGraphNode(imported_tree, filename, __main__.current_scope)
                imported_tree.link = module
                for node in ast.walk(imported_tree):
                    node.filelink = module 
                self.imported_files[searchname] = imported_tree.link 
                parser.walk()
            if __main__.current_scope:
                var_name = alias.asname if alias.asname else alias.name
                alias.link = __main__.current_scope.findOrAdd(var_name)
                imported_tree.link.addDependency(DependencyType.Assign, alias.link)
