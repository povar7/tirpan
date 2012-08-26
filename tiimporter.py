'''
Created on 29.01.2012

@author: bronikkk
'''

import ast

import os
from os import sys

import __main__

from builtin   import import_standard_module
from tiparser  import TIParser
from typegraph import UsualVarTypeGraphNode, UsualModuleTypeGraphNode, ExternModuleTypeGraphNode, DependencyType

def get_init_name(name):
    return os.path.join(name, '__init__')

def get_names_from_alias_name(name):
    if name is None:
        name    = '.'
    parts       = name.split('.')
    number      = len(parts)
    index       = 1
    current     = parts[0]
    result      = []
    while index < number:
        result.append((False, current))
        current = os.path.join(current, parts[index])
        index  += 1
    result.append((True, current))
    return result

class QuasiAlias(object):
    def __init__(self, name):
        self.name   = name
        self.asname = None

class Importer(object):
    def __init__(self):
        self.imported_files   = {}
        self.standard_modules = {}
        self.ident_table      = {}
        self.total_idents     = 0

    def put_ident(self, name):
        self.ident_table[self.total_idents] = name
        res = self.total_idents
        self.total_idents += 1
        return res          

    def get_ident(self, num):
        return self.ident_table[num]

    def add_module(self, scope, name):
        if not name in self.standard_modules:
            self.standard_modules[name] = ExternModuleTypeGraphNode(name, scope)

    def find_module(self, name, paths):
        for path in paths:
            canonical = os.path.join(path, name)
            if os.path.isdir(canonical):
                filename = os.path.join(canonical, '__init__.py')
            else:
                filename = canonical + '.py'
            if os.path.exists(filename):
                return filename
        return None

    def process_name(self, name, filename):
        paths = [os.path.dirname(filename)]
        paths.extend(sys.path)
        return self.find_module(name, paths)

    def import_files_extended(self, mainfile, alias, name, terminal, from_aliases):
        main_module = False
        if name in self.standard_modules:
            module = self.standard_modules[name]
            import_standard_module(module, self)
        else:
            if name == '__main__':
                filename     = os.path.abspath(mainfile)
                searchname   = name
                main_module  = True
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
                fileno = self.put_ident(module)
                for node in ast.walk(imported_tree):
                    node.fileno = fileno
                self.imported_files[searchname] = imported_tree.link 
                parser.walk(main_module)
        if from_aliases is None:
            var_name = alias.asname if alias.asname else name
            alias.link = __main__.current_scope.findOrAdd(var_name)
            module.addDependency(DependencyType.Assign, alias.link)
        elif terminal:
            if len(from_aliases) == 1 and from_aliases[0].name == '*':
                from_aliases = [QuasiAlias(key) for key in module.scope.variables.keys() if key != '__all__']
            for from_alias in from_aliases:
                old_var_name = from_alias.name  
                new_var_name = from_alias.asname if from_alias.asname else old_var_name
                old_var      = module.scope.find(old_var_name)
                try:
                    new_var = UsualVarTypeGraphNode(new_var_name)
                    __main__.current_scope.add(new_var)
                    old_var.addDependency(DependencyType.Assign, new_var)
                except AttributeError:
                    from errorprinter import ImportFromStmtError
                    __main__.error_printer.printError(ImportFromStmtError(old_var_name, module.name))

    def import_files(self, mainfile, aliases, from_aliases = None):
        for alias in aliases:
            for terminal, name in get_names_from_alias_name(alias.name): 
                self.import_files_extended(mainfile, alias, name, terminal, from_aliases)
