'''
Created on 29.01.2012

@author: bronikkk
'''

import ast

import os
from os import sys

import __main__

from tiparser  import TIParser
from typegraph import UsualVarTypeGraphNode, UsualModuleTypeGraphNode, ExternModuleTypeGraphNode, DependencyType

class QuasiAlias(object):
    def __init__(self, name):
        self.name   = name
        self.asname = None

class Importer(object):
    def __init__(self):
        self.imported_files   = {}
        self.standard_modules = {}

    def add_module(self, scope, name):
        if not name in self.standard_modules:
            module = ExternModuleTypeGraphNode(name, scope)
            self.standard_modules[name] = module
        return self.standard_modules[name]

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

    def import_files(self, mainfile, aliases, from_aliases = None):
        for alias in aliases:
            name = alias.name
            if name in self.standard_modules:
                module = self.standard_modules[name]
            else:
                if name == '__main__':
                    filename   = os.path.abspath(mainfile)
                    searchname = name
                else:
                    try: 
                        filename = os.path.abspath(self.process_name(name, mainfile))
                    except AttributeError:
                        filename = None
                    if filename is None:
                        from errorprinter import ImportStmtError
                        __main__.error_printer.printError(ImportStmtError(name))
                        return
                    searchname = filename
                if searchname in self.imported_files:
                    imported_tree = self.imported_files[searchname].ast
                    module = imported_tree.link 
                else:
                    parser = TIParser(filename)
                    imported_tree = parser.ast
                    module = UsualModuleTypeGraphNode(imported_tree, filename, __main__.current_scope)
                    imported_tree.link = module
                    for node in ast.walk(imported_tree):
                        node.filelink = module 
                    self.imported_files[searchname] = imported_tree.link 
                    parser.walk()
            if from_aliases is None:
                var_name = alias.asname if alias.asname else alias.name
                alias.link = __main__.current_scope.findOrAdd(var_name)
                module.addDependency(DependencyType.Assign, alias.link)
            else:
                for from_alias in from_aliases:
                    var_name  = from_alias.name  
                    var_alias = from_alias.asname if from_alias.asname else var_name
                    var = module.scope.find(var_name)
                    try:
                        alias = UsualVarTypeGraphNode(var_alias)
                        __main__.current_scope.add(alias)
                        var.addDependency(DependencyType.Assign, alias)
                    except AttributeError:
                        from errorprinter import ImportFromStmtError
                        __main__.error_printer.printError(ImportFromStmtError(var_name, module.name))
